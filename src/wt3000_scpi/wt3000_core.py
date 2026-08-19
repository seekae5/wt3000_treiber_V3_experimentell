# =============================================================================
# Datei: wt3000_core.py
# Layer 1 (Session/Plumbing)
#
# UEBERARBEITET (ROADMAP M1-2): Layer 0 ist ausgezogen. Transport-Protocol,
# WTConfig, TmctlTransport und die Transport-Fehlerklassen liegen jetzt in
# 'wt3000_transport.py'. Dieses Modul haelt nur noch die Protokollschicht:
# Query-Regeln, Blockdaten, Fehlerqueue, Nur-Lesen-Sperre, Fernsteuerung.
#
# Die verschobenen Namen werden hier unveraendert weiter-exportiert. Bestehende
# Importe der Form
#     from .wt3000_core import WTConfig, TmctlTransport, WTError
# funktionieren wortgleich weiter, und weil es dieselben Klassenobjekte sind,
# faengt 'except WTError' weiterhin alles. Die auskommentierten Originale der
# verschobenen Bloecke stehen am Dateiende unter 'VERSCHOBEN (M1-2)'.
# =============================================================================

from __future__ import annotations

# UEBERARBEITET (M1-2): 'ctypes', 'os' und 'Path' wurden nur von TmctlTransport
# gebraucht und sind mit ihm nach wt3000_transport gewandert, 'dataclass' nur
# von WTConfig. 'TracebackType' ebenso - WTSession ist kein Context Manager.
# import ctypes as ct
import logging
# import os
# from dataclasses import dataclass
# from pathlib import Path
# from types import TracebackType

# NEU (M1-2): Layer 1 zieht sich Layer 0 herein - Importrichtung nach unten.
# 'Transport' ist der Vertrag, den WTSession voraussetzt; die uebrigen Namen
# werden nur durchgereicht (siehe __all__ weiter unten).
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

# NEU (M1-2): macht sichtbar, dass die durchgereichten Namen Teil der
# Schnittstelle dieses Moduls bleiben - und haelt Linter davon ab, die
# scheinbar ungenutzten Importe oben zu entfernen.
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
    "MAX_BLOCK_READS",  # NEU (P-4)
    "DeviceError",
    "ReadOnlyViolation",
    "WTSession",
]


# ---------------------------------------------------------------------------
# Exceptions der Sitzungsschicht
# UEBERARBEITET (M1-2): WTError, TmctlError und ProtocolError sind nach
# wt3000_transport gewandert - sie entstehen im Transport. Die beiden
# folgenden Klassen entstehen erst hier und bleiben deshalb hier.
# ---------------------------------------------------------------------------


# UEBERARBEITET (P-4, siehe PLAN_BEFUNDE_2026-08-19.md): war eine nackte 64 in
# der Nachlese-Schleife von _assemble_block(). Der Wert wird jetzt an zwei
# Stellen gebraucht - fuer die Schleifengrenze und, mit der Puffergroesse
# multipliziert, fuer die groesste Nutzlast, die ueberhaupt zusammengesetzt
# werden kann.
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

    UEBERARBEITET (M1-2): nimmt jetzt ein 'Transport'-Protocol statt der
    konkreten Klasse 'TmctlTransport'. Damit laesst sich dieselbe Sitzung mit
    'FakeTransport' geraetefrei betreiben - und spaeter mit einem Socket- oder
    VISA-Transport, ohne dass hier eine Zeile faellt.
    """

    # UEBERARBEITET (M1-2): Signatur war
    #   def __init__(self, transport: TmctlTransport, config: WTConfig,
    #                read_only: bool = False) -> None:
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

        UEBERARBEITET (P-4, siehe PLAN_BEFUNDE_2026-08-19.md): Der Kopf wird
        jetzt vollstaendig geprueft. Bisher war nur die Ziffernanzahl
        abgesichert; die Umwandlung des Laengenfelds stand ungeschuetzt und
        konnte einen nackten ValueError herauslassen - etwa bei einer nach dem
        Kopf abgerissenen Antwort ('#4') oder einem nichtnumerischen Feld.
        Aufrufer, die pflichtgemaess nur WTError behandeln, liefen dann daran
        vorbei; genau die Stufenskripte tun das.

        Ab jetzt gilt: jeder Formfehler einer Blockantwort verlaesst diese
        Methode als ProtocolError.
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

        # UEBERARBEITET (P-4): abgeschnittener Kopf. Ohne diese Pruefung liefert
        # der Schnitt unten stillschweigend zu wenige oder gar keine Bytes, und
        # int() bricht mit einem ValueError ab, den niemand faengt.
        if len(raw) < header_length:
            raise ProtocolError(
                f"Blockheader abgeschnitten: angekuendigt sind {digit_count} "
                f"Laengenziffern, die Antwort hat aber nur {len(raw)} Bytes "
                f"({raw[:16]!r})"
            )

        # UEBERARBEITET (P-4): dieselbe Absicherung wie oben fuer die
        # Ziffernanzahl - Meldung nach demselben Muster, mit den ersten Bytes.
        try:
            payload_length = int(raw[2:header_length])
        except ValueError as exc:
            raise ProtocolError(
                f"Laengenfeld des Blockheaders ist keine Zahl: "
                f"{raw[2:header_length]!r} (Kopf: {raw[:header_length]!r})"
            ) from exc

        # UEBERARBEITET (P-4): unplausible Laengen abfangen, BEVOR die
        # Nachlese-Schleife laeuft.
        #
        # Negativ: 'payload[:payload_length]' wuerde am Ende schneiden statt am
        # Anfang - die Schleife laeuft gar nicht erst an, und heraus kaeme
        # stillschweigend ein zu kurzer Block. Das ist der unangenehmere der
        # beiden Faelle, weil er wie ein Ergebnis aussieht.
        #
        # Zu gross: die Schleife wuerde 64-mal ins Leere lesen und dann
        # 'nach 64 Lesevorgaengen immer noch unvollstaendig' melden - eine
        # Meldung, die auf eine langsame Verbindung deutet statt auf den
        # kaputten Kopf, der die eigentliche Ursache ist.
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


# ===========================================================================
# VERSCHOBEN (M1-2) - Originalfassung des Layer-0-Blocks
#
# Projektkonvention: entfernter Code wird auskommentiert, nicht geloescht.
# Der folgende Block stand bis M1-2 an dieser Stelle (zwischen den
# Fehlerklassen und WTSession) und liegt jetzt wortgleich - bis auf einen
# erweiterten Docstring - in 'wt3000_transport.py'. Er ist hier nur noch
# Beleg der Herkunft; Aenderungen gehoeren ausschliesslich in das neue Modul.
# Beim naechsten Aufraeumen ersatzlos zu loeschen.
# ===========================================================================
#
# # Layer 0 - Transport
# # ---------------------------------------------------------------------------
#
#
# class TmctlTransport:
#     """Transportschicht ueber die Yokogawa-TMCTL-DLL.
#
#     Kennt keinerlei WT3000-Kommandos, nur write/read/query/close.
#     """
#
#     def __init__(self, config: WTConfig) -> None:
#         self._log = logging.getLogger("wt3000.transport")
#         self._config = config
#         self._device_id = ct.c_int(0)
#         self._open = False
#
#         dll_path = Path(config.dll_path)
#         if not dll_path.is_file():
#             raise WTError(f"TMCTL-DLL nicht gefunden: {dll_path}")
#
#         # Abhaengige DLLs liegen ueblicherweise im selben Verzeichnis.
#         if hasattr(os, "add_dll_directory"):
#             os.add_dll_directory(str(dll_path.parent))
#
#         self._tm = ct.WinDLL(str(dll_path))
#         self._declare_prototypes()
#         self._initialize()
#
#     # -- Setup --------------------------------------------------------------
#
#     def _declare_prototypes(self) -> None:
#         """Signaturen der genutzten TMCTL-Funktionen festlegen."""
#         tm = self._tm
#         tm.TmcInitialize.argtypes = [ct.c_int, ct.c_char_p, ct.POINTER(ct.c_int)]
#         tm.TmcInitialize.restype = ct.c_int
#         tm.TmcSend.argtypes = [ct.c_int, ct.c_char_p]
#         tm.TmcSend.restype = ct.c_int
#         tm.TmcReceive.argtypes = [ct.c_int, ct.c_char_p, ct.c_int, ct.POINTER(ct.c_int)]
#         tm.TmcReceive.restype = ct.c_int
#         tm.TmcSetTimeout.argtypes = [ct.c_int, ct.c_int]
#         tm.TmcSetTimeout.restype = ct.c_int
#         tm.TmcFinish.argtypes = [ct.c_int]
#         tm.TmcFinish.restype = ct.c_int
#
#     def _initialize(self) -> None:
#         """Verbindung aufbauen. Adressstring hat das Format 'ip,user,password'."""
#         cfg = self._config
#         address = f"{cfg.ip},{cfg.user},{cfg.password}".encode("ascii")
#         self._check(
#             self._tm.TmcInitialize(TM_CTL_ETHER, address, ct.byref(self._device_id)),
#             "TmcInitialize",
#             f"Adresse={cfg.ip}",
#         )
#         self._open = True
#         self._log.info("Verbindung aufgebaut, Device-ID %d", self._device_id.value)
#         self.set_timeout(cfg.timeout_ms)
#
#     @staticmethod
#     def _check(rc: int, function: str, detail: str = "") -> None:
#         """Jeden TMCTL-Rueckgabewert pruefen, Fehlercode hexadezimal melden."""
#         if rc != 0:
#             raise TmctlError(function, rc, detail)
#
#     # -- Basisoperationen ---------------------------------------------------
#
#     def set_timeout(self, timeout_ms: int) -> None:
#         """Kommunikationstimeout setzen (Einheit ZU VERIFIZIEREN)."""
#         self._check(self._tm.TmcSetTimeout(self._device_id, timeout_ms), "TmcSetTimeout")
#
#     def write(self, command: str) -> None:
#         """Programmnachricht senden.
#
#         Es wird bewusst KEIN Terminator angehaengt: TMCTL setzt ihn selbst
#         (verifiziert mit '*IDN?').
#         ZU VERIFIZIEREN: Verhalten bei mit ';' verketteten Kommandos.
#         """
#         payload = command.encode("ascii")
#         if len(payload) + 1 > MAX_PROGRAM_MESSAGE_BYTES:
#             raise ProtocolError(
#                 f"Programmnachricht zu lang ({len(payload)} Bytes), "
#                 f"Limit inkl. Terminator {MAX_PROGRAM_MESSAGE_BYTES} Bytes"
#             )
#         self._log.debug("TX: %r", command)
#         self._check(self._tm.TmcSend(self._device_id, payload), "TmcSend", command)
#
#     def read(self) -> bytes:
#         """Einen Lesevorgang ausfuehren und die Rohbytes zurueckgeben."""
#         size = self._config.read_buffer_size
#         buffer = ct.create_string_buffer(size)
#         received = ct.c_int(0)
#         self._check(
#             self._tm.TmcReceive(self._device_id, buffer, size, ct.byref(received)),
#             "TmcReceive",
#         )
#         data = buffer.raw[: received.value]
#         if received.value >= size:
#             self._log.warning(
#                 "Lesepuffer (%d Bytes) vollstaendig gefuellt - Antwort evtl. unvollstaendig", size
#             )
#         self._log.debug("RX: %d Bytes", len(data))
#         return data
#
#     def query(self, command: str) -> bytes:
#         """Query senden und einen Lesevorgang ausfuehren."""
#         self.write(command)
#         return self.read()
#
#     def close(self) -> None:
#         """Verbindung schliessen. Mehrfachaufruf ist unschaedlich."""
#         if not self._open:
#             return
#         self._open = False
#         rc = self._tm.TmcFinish(self._device_id)
#         if rc != 0:
#             self._log.warning("TmcFinish meldete Fehlercode 0x%08X", rc)
#         else:
#             self._log.info("Verbindung geschlossen")
#
#     # -- Context Manager ----------------------------------------------------
#
#     def __enter__(self) -> "TmctlTransport":
#         return self
#
#     def __exit__(
#         self,
#         exc_type: type[BaseException] | None,
#         exc: BaseException | None,
#         tb: TracebackType | None,
#     ) -> None:
#         self.close()
#
