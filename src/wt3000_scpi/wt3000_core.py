# =============================================================================
# Datei: wt3000_core.py
# Layer 1 - Protokollschicht: Query-Regeln, Blockdaten, Fehlerqueue,
#           Nur-Lesen-Sperre, Fernsteuerung.
#
# Layer 0 liegt in 'wt3000_transport.py': Transport-Protocol, TmctlTransport,
# WTConfig und die Transport-Fehlerklassen. Diese Namen werden hier
# unveraendert weiter-exportiert - Importe der Form
#     from .wt3000_core import WTConfig, TmctlTransport, WTError
# funktionieren also wortgleich, und weil es dieselben Klassenobjekte sind,
# faengt 'except WTError' weiterhin alles.
# =============================================================================

from __future__ import annotations

import logging

# Importrichtung nach unten: Layer 1 zieht sich Layer 0 herein. 'Transport' ist
# der Vertrag, den WTSession voraussetzt; die uebrigen Namen werden nur
# durchgereicht (siehe __all__).
from .wt3000_transport import (
    MAX_PROGRAM_MESSAGE_BYTES,
    TM_CTL_ETHER,
    ProtocolError,
    TmctlError,
    TmctlTransport,
    Transport,
    WTConfig,
    WTError,
)

# Haelt fest, dass die durchgereichten Namen zur Schnittstelle dieses Moduls
# gehoeren - und haelt Linter davon ab, die scheinbar ungenutzten Importe oben
# zu entfernen.
__all__ = [
    # weitergereicht aus wt3000_transport (Layer 0)
    "MAX_PROGRAM_MESSAGE_BYTES",
    "TM_CTL_ETHER",
    "ProtocolError",
    "TmctlError",
    "TmctlTransport",
    "Transport",
    "WTConfig",
    "WTError",
    # hier beheimatet (Layer 1)
    "MAX_BLOCK_READS",
    "DeviceError",
    "ReadOnlyViolation",
    "WTSession",
]


# ---------------------------------------------------------------------------
# Konstanten und Exceptions der Sitzungsschicht
#
# WTError, TmctlError und ProtocolError entstehen im Transport und wohnen
# deshalb in wt3000_transport. Die beiden Klassen hier entstehen erst in dieser
# Schicht.
# ---------------------------------------------------------------------------

# Grenze der Nachlese-Schleife in _assemble_block(). Zweimal gebraucht: als
# Schleifengrenze und - mit der Puffergroesse multipliziert - als groesste
# Nutzlast, die sich ueberhaupt zusammensetzen laesst.
MAX_BLOCK_READS: int = 64


class DeviceError(WTError):
    """Das Geraet hat einen Eintrag in die Fehlerqueue gelegt."""


class ReadOnlyViolation(WTError):
    """In einer Nur-Lesen-Session wurde ein schreibendes Kommando versucht."""


# ---------------------------------------------------------------------------
# Layer 1 - Session / Plumbing
# ---------------------------------------------------------------------------


class WTSession:
    """Protokollschicht: Query-Regeln, Blockdaten, Fehlerqueue.

    Nimmt ein 'Transport'-Protocol entgegen, keine konkrete Klasse. Damit
    laeuft dieselbe Sitzung geraetefrei auf 'FakeTransport' - und spaeter auf
    einem Socket- oder VISA-Transport, ohne dass hier eine Zeile faellt.

    OFFEN (ROADMAP M3-1) - VOR der Umsetzung zu entscheiden, nicht waehrend:
    Diese Klasse ist NICHT threadsicher, und im ganzen Paket gibt es kein
    einziges Lock. write() und query() sind ein Schreib-Lese-Paar auf EINER
    Verbindung; laufen zwei davon nebenlaeufig, bekommt der eine Aufrufer die
    Antwort des anderen - und zwar stillschweigend, weil beide Antworten fuer
    sich plausibel aussehen. Sobald M3-1 die Messschleife in einen
    Hintergrund-Thread legt, ist genau das der Normalfall: der Thread liest im
    Takt, waehrend der Aufrufer weiterhin wt.input, wt.ranges oder
    log_condition() benutzen darf. Zwei gangbare Wege:

      (a) ein threading.RLock hier, gelegt um write/query/query_raw/
          query_block. Er muss query_block() GANZ umschliessen, denn
          _assemble_block() liest ueber self._transport.read() nach - sonst
          liest der zweite Aufrufer mitten in einen fremden Block hinein.
          Ebenfalls betroffen: set_timeout() in drain_after_failure(), das
          gemeinsamen Transportzustand veraendert.
      (b) die ausdrueckliche Zusage 'waehrend einer laufenden Measurement
          gehoert die Sitzung dem Thread' - dann muss die Fassade jeden
          anderen Zugriff ablehnen, solange is_running gilt.

    Weg (a) ist die kleinere Aenderung, Weg (b) die ehrlichere: ein Lock macht
    einen Fremdzugriff mitten in der Messreihe zwar sicher, aber nicht
    sinnvoll - er verschiebt den naechsten Takt.
    """

    def __init__(self, transport: Transport, config: WTConfig, read_only: bool = False) -> None:
        self._log = logging.getLogger("wt3000.session")
        self._transport = transport
        self._config = config
        self._read_only = read_only
        self._remote_active = False

    # -- Fernsteuerung ------------------------------------------------------

    def enable_remote(self) -> None:
        """Fernsteuerung einschalten (REMOTE-LED an, Tasten ausser LOCAL gesperrt)."""
        self.write(":COMMunicate:REMote ON")
        self._remote_active = True
        self._log.info("Fernsteuerung eingeschaltet")

    def disable_remote(self) -> None:
        """Fernsteuerung abschalten. Gibt das Bedienfeld frei."""
        if not self._remote_active:
            return
        try:
            self.write(":COMMunicate:REMote OFF")
            self._log.info("Fernsteuerung abgeschaltet")
        except WTError as exc:
            self._log.warning("REMote OFF fehlgeschlagen: %s", exc)
        finally:
            self._remote_active = False

    # -- Kern ---------------------------------------------------------------

    def write(self, command: str) -> None:
        """Set-Kommando senden (kein Query)."""
        self._validate(command, expect_query=False)
        self._transport.write(command)

    def query(self, command: str) -> str:
        """Genau einen Query absetzen und die Antwort als Text zurueckgeben."""
        self._validate(command, expect_query=True)
        return self.decode(self._transport.query(command))

    def query_raw(self, command: str) -> bytes:
        """Wie query(), liefert aber die unveraenderten Rohbytes."""
        self._validate(command, expect_query=True)
        return self._transport.query(command)

    def query_block(self, command: str) -> bytes:
        """Query absetzen, dessen Antwort ein <Block data> mit '#n'-Header ist.

        Liest so lange nach, bis die im Header angekuendigte Nutzlast
        vollstaendig vorliegt. Damit ist es egal, ob TmcReceive den Block in
        einem Stueck liefert oder an einem 0x0A-Byte innerhalb der Binaerdaten
        abbricht (ZU VERIFIZIEREN, welches Verhalten tatsaechlich vorliegt).
        """
        raw = self.query_raw(command)
        return self._assemble_block(raw)

    def _assemble_block(self, raw: bytes) -> bytes:
        """'#4NNNN<daten>' auswerten und die Nutzlast vollstaendig einsammeln.

        Zusage: JEDER Formfehler einer Blockantwort verlaesst diese Methode als
        ProtocolError, nie als nackter ValueError. Aufrufer behandeln
        pflichtgemaess nur WTError - die Stufenskripte tun genau das.
        """
        if not raw.startswith(b"#"):
            raise ProtocolError(
                f"Kein Blockheader in der Antwort (erste Bytes: {raw[:16]!r}). "
                "Steht :NUMeric:FORMat wirklich auf FLOat?"
            )
        try:
            digit_count = int(raw[1:2])
        except ValueError as exc:
            raise ProtocolError(f"Ungueltiger Blockheader: {raw[:8]!r}") from exc
        if digit_count == 0:
            raise ProtocolError("Block mit unbestimmter Laenge ('#0') wird nicht unterstuetzt")

        header_length = 2 + digit_count

        # Abgeschnittener Kopf: ohne diese Pruefung liefert der Schnitt unten
        # stillschweigend zu wenige oder gar keine Bytes, und int() bricht mit
        # einem ValueError ab, den niemand faengt.
        if len(raw) < header_length:
            raise ProtocolError(
                f"Blockheader abgeschnitten: angekuendigt sind {digit_count} "
                f"Laengenziffern, die Antwort hat aber nur {len(raw)} Bytes "
                f"({raw[:16]!r})"
            )

        # Dieselbe Absicherung wie oben fuer die Ziffernanzahl.
        try:
            payload_length = int(raw[2:header_length])
        except ValueError as exc:
            raise ProtocolError(
                f"Laengenfeld des Blockheaders ist keine Zahl: "
                f"{raw[2:header_length]!r} (Kopf: {raw[:header_length]!r})"
            ) from exc

        # Unplausible Laengen abfangen, BEVOR die Nachlese-Schleife laeuft:
        #
        #   negativ   'payload[:payload_length]' schneidet am Ende statt am
        #             Anfang und die Schleife laeuft gar nicht erst an - heraus
        #             kaeme stillschweigend ein zu kurzer Block, der wie ein
        #             Ergebnis aussieht.
        #   zu gross  die Schleife liest ins Leere und meldet am Ende einen
        #             Abbruch nach n Lesevorgaengen. Das deutet auf eine
        #             langsame Verbindung statt auf den kaputten Kopf.
        max_payload = MAX_BLOCK_READS * self._config.read_buffer_size
        if not 0 <= payload_length <= max_payload:
            raise ProtocolError(
                f"Unplausible Nutzlastlaenge im Blockheader: {payload_length} Bytes "
                f"(Kopf: {raw[:header_length]!r}). Zulaessig sind 0 bis {max_payload} "
                f"Bytes - mehr liesse sich in {MAX_BLOCK_READS} Lesevorgaengen "
                "ohnehin nicht einsammeln."
            )

        payload = raw[header_length:]

        reads = 1
        while len(payload) < payload_length:
            payload += self._transport.read()
            reads += 1
            if reads > MAX_BLOCK_READS:
                raise ProtocolError(
                    f"Blockdaten nach {MAX_BLOCK_READS} Lesevorgaengen immer noch "
                    f"unvollstaendig ({len(payload)} von {payload_length} Bytes)"
                )
        if reads > 1:
            self._log.info("Blockdaten in %d Lesevorgaengen zusammengesetzt", reads)

        return payload[:payload_length]

    def _validate(self, command: str, expect_query: bool) -> None:
        """Protokollregeln pruefen, bevor die Nachricht das Geraet erreicht."""
        stripped = command.strip()
        is_query = stripped.endswith("?")

        if self._read_only and not is_query:
            raise ReadOnlyViolation(
                f"Nur-Lesen-Session: '{command}' ist kein Query und wird nicht gesendet"
            )
        if expect_query and not is_query:
            raise ProtocolError(f"'{command}' ist kein Query, wurde aber als solcher aufgerufen")
        if not expect_query and is_query:
            raise ProtocolError(f"'{command}' ist ein Query, wurde aber als write() aufgerufen")
        # Handbuch Kap. 5: genau ein Query pro Programmnachricht.
        if stripped.count("?") > 1:
            raise ProtocolError(f"Mehr als ein Query in einer Nachricht: '{command}'")

    @staticmethod
    def decode(raw: bytes) -> str:
        """Rohbytes in Text wandeln und Terminator entfernen."""
        return raw.decode("ascii", errors="replace").strip("\r\n\0 ")

    # -- Fehlerqueue --------------------------------------------------------

    def drain_after_failure(self) -> None:
        """Nach einem fehlgeschlagenen Query eine verspaetete Antwort abraeumen."""
        try:
            self._transport.set_timeout(self._config.drain_timeout_ms)
            leftover = self._transport.read()
            if leftover:
                self._log.warning("Nachlaufende Antwort verworfen: %r", leftover[:80])
        except TmctlError:
            pass  # Erwarteter Fall: nichts mehr da.
        finally:
            self._transport.set_timeout(self._config.timeout_ms)

    def read_error_queue(self, max_entries: int = 20) -> list[str]:
        """Fehlerqueue leeren. Hinweis: :STATus:ERRor? entfernt den Eintrag."""
        entries: list[str] = []
        for _ in range(max_entries):
            answer = self.query(":STATus:ERRor?")
            entries.append(answer)
            if answer.split(",", 1)[0].strip().lstrip("+") == "0":
                break
        return entries

    def assert_no_error(self, context: str) -> None:
        """Fehlerqueue pruefen und bei Eintraegen eine DeviceError werfen."""
        entries = self.read_error_queue()
        problems = [e for e in entries if e.split(",", 1)[0].strip().lstrip("+") != "0"]
        if problems:
            raise DeviceError(f"Geraetefehler nach '{context}': {problems}")
