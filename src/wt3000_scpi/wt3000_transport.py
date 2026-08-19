# =============================================================================
# Datei: wt3000_transport.py
# NEU (ROADMAP M1-2): Layer 0 - Transport.
#
# Hintergrund. Bis hierher war 'TmctlTransport' fest in 'wt3000_core' verdrahtet:
# 'ctypes.WinDLL' und 'os.add_dll_directory' machten den Treiber auf Windows
# festgenagelt, und 'WTSession' liess sich ohne Geraet gar nicht pruefen - die
# Testsuite setzte erst eine Ebene darueber mit 'FakeSession' an. Damit blieben
# genau die Regeln ungetestet, die WTSession selbst durchsetzt: Query-Regeln,
# Blockdaten-Zusammenbau, Fehlerqueue, Nur-Lesen-Sperre.
#
# Dieses Modul ist die unterste Schicht und importiert deshalb NICHTS aus dem
# Paket. Alles, was ein Transport zum Arbeiten braucht - Verbindungsparameter
# und die Fehlerklassen, die er selbst wirft - liegt hier. 'wt3000_core'
# reicht diese Namen unveraendert weiter, damit bestehende Importe der Form
#     from .wt3000_core import WTConfig, TmctlError
# wortgleich weiterfunktionieren.
#
# Inhalt:
#   Transport        typing.Protocol - der Vertrag, den WTSession voraussetzt
#   TmctlTransport   Yokogawa-TMCTL-DLL ueber Ethernet (aus wt3000_core hierher
#                    verschoben, inhaltlich unveraendert)
#   FakeTransport    beantwortet Kommandos aus einer Tabelle, merkt sich
#                    Geschriebenes, bildet Blockdaten und Fehlerqueue nach
#   float_block()    Hilfsfunktion: Messwerte in einen '#4NNNN'-Block giessen
#
# Bewusst NICHT gebaut, aber als Fuge offengelassen (siehe unten):
#   SocketTransport (VXI-11 / Raw-Socket), VisaTransport (pyvisa).
# =============================================================================

from __future__ import annotations

import ctypes as ct
import logging
import os
import struct
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Protocol, runtime_checkable

# UEBERARBEITET (M1-2): aus wt3000_core hierher verschoben - beides sind
# Eigenschaften des Transports, nicht der Protokollschicht.
# TMCTL-Konstante fuer Ethernet-Transport (aus tmctl.h)
TM_CTL_ETHER: int = 4

# Maximale Laenge einer Programmnachricht inkl. Terminator (Handbuch Kap. 5).
MAX_PROGRAM_MESSAGE_BYTES: int = 1024


# ---------------------------------------------------------------------------
# Verbindungsparameter
# UEBERARBEITET (M1-2): aus wt3000_core hierher verschoben. Ein Transport muss
# ohne die Protokollschicht konstruierbar sein, sonst zeigt der Import nach oben.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WTConfig:
    """Verbindungs- und Laufzeitparameter. Hier zentral anpassen."""

    dll_path: str = r"C:\Users\Persystems\PycharmProjects\WT3000_SCPI\tmctl8020\dll\tmctl64.dll"
    ip: str = "192.168.10.20"
    user: str = "TEST"
    password: str = "1"
    # ZU VERIFIZIEREN: Einheit von TmcSetTimeout (ms angenommen).
    timeout_ms: int = 5000
    drain_timeout_ms: int = 500
    read_buffer_size: int = 64 * 1024
    # ZU VERIFIZIEREN: Ob das Geraet Set-Kommandos ueber Ethernet auch ohne
    # ':COMMunicate:REMote ON' annimmt. Falls Schreibzugriffe abgelehnt werden,
    # hier auf True setzen. Wird dann beim Beenden zwingend wieder abgeschaltet.
    # Offener Punkt der ROADMAP: M0-3.
    use_remote: bool = True


# ---------------------------------------------------------------------------
# Fehlerklassen des Transports
# UEBERARBEITET (M1-2): aus wt3000_core hierher verschoben. Diese drei Klassen
# wirft der Transport selbst; die sitzungsnahen Klassen (DeviceError,
# ReadOnlyViolation) bleiben in wt3000_core. 'wt3000_core' importiert sie hier
# und exportiert sie unveraendert weiter - die Klassenidentitaet bleibt also
# erhalten, 'except WTError' faengt weiterhin alles.
# ---------------------------------------------------------------------------


class WTError(Exception):
    """Basisklasse fuer alle Fehler dieses Treibers."""


class TmctlError(WTError):
    """Eine TMCTL-Funktion hat einen Fehlercode != 0 zurueckgegeben."""

    def __init__(self, function: str, code: int, detail: str = "") -> None:
        self.function = function
        self.code = code
        suffix = f" ({detail})" if detail else ""
        super().__init__(f"{function} fehlgeschlagen, TMCTL-Fehlercode 0x{code:08X}{suffix}")


class ProtocolError(WTError):
    """Verstoss gegen die Protokollregeln aus Kapitel 5 des Handbuchs."""


# ---------------------------------------------------------------------------
# NEU (M1-2): der Vertrag
# ---------------------------------------------------------------------------


@runtime_checkable
class Transport(Protocol):
    """Was 'WTSession' von einem Transport voraussetzt - und sonst nichts.

    Bewusst klein gehalten: fuenf Methoden, keine Kenntnis eines einzigen
    WT3000-Kommandos. Wer diese fuenf Methoden anbietet, kann eine WTSession
    tragen - ohne von einer Basisklasse zu erben (strukturelle Typisierung).

    Regeln, auf die sich WTSession verlaesst:
      * write()  haengt KEINEN Terminator an - das erledigt die Gegenstelle
      * read()   liefert genau einen Lesevorgang; dass die Antwort damit
                 vollstaendig ist, ist NICHT zugesichert. Der Zusammenbau von
                 Blockdaten passiert in WTSession._assemble_block()
      * query()  ist write() gefolgt von read()
      * jeder Fehler auf der Leitung kommt als TmctlError heraus, damit die
        Aufrufer oben nur eine Fehlerklasse abfangen muessen
    """

    def write(self, command: str) -> None: ...

    def read(self) -> bytes: ...

    def query(self, command: str) -> bytes: ...

    def set_timeout(self, timeout_ms: int) -> None: ...

    def close(self) -> None: ...


# ---------------------------------------------------------------------------
# TMCTL-Transport
# UEBERARBEITET (M1-2): unveraendert aus wt3000_core hierher verschoben.
# Einzige inhaltliche Aenderung: der Docstring nennt jetzt das Protocol.
# ---------------------------------------------------------------------------


class TmctlTransport:
    """Transportschicht ueber die Yokogawa-TMCTL-DLL.

    Erfuellt das 'Transport'-Protocol. Kennt keinerlei WT3000-Kommandos, nur
    write/read/query/set_timeout/close.

    Windows-gebunden: 'ctypes.WinDLL' existiert auf anderen Betriebssystemen
    nicht. Der Import dieses Moduls ist davon nicht betroffen - erst die
    Instanziierung laedt die DLL. Genau deshalb kann die Testsuite dieses Modul
    importieren und trotzdem geraetefrei laufen.
    """

    def __init__(self, config: WTConfig) -> None:
        self._log = logging.getLogger("wt3000.transport")
        self._config = config
        self._device_id = ct.c_int(0)
        self._open = False

        dll_path = Path(config.dll_path)
        if not dll_path.is_file():
            raise WTError(f"TMCTL-DLL nicht gefunden: {dll_path}")

        # Abhaengige DLLs liegen ueblicherweise im selben Verzeichnis.
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(str(dll_path.parent))

        self._tm = ct.WinDLL(str(dll_path))
        self._declare_prototypes()
        self._initialize()

    # -- Setup --------------------------------------------------------------

    def _declare_prototypes(self) -> None:
        """Signaturen der genutzten TMCTL-Funktionen festlegen."""
        tm = self._tm
        tm.TmcInitialize.argtypes = [ct.c_int, ct.c_char_p, ct.POINTER(ct.c_int)]
        tm.TmcInitialize.restype = ct.c_int
        tm.TmcSend.argtypes = [ct.c_int, ct.c_char_p]
        tm.TmcSend.restype = ct.c_int
        tm.TmcReceive.argtypes = [ct.c_int, ct.c_char_p, ct.c_int, ct.POINTER(ct.c_int)]
        tm.TmcReceive.restype = ct.c_int
        tm.TmcSetTimeout.argtypes = [ct.c_int, ct.c_int]
        tm.TmcSetTimeout.restype = ct.c_int
        tm.TmcFinish.argtypes = [ct.c_int]
        tm.TmcFinish.restype = ct.c_int

    def _initialize(self) -> None:
        """Verbindung aufbauen. Adressstring hat das Format 'ip,user,password'."""
        cfg = self._config
        address = f"{cfg.ip},{cfg.user},{cfg.password}".encode("ascii")
        self._check(
            self._tm.TmcInitialize(TM_CTL_ETHER, address, ct.byref(self._device_id)),
            "TmcInitialize",
            f"Adresse={cfg.ip}",
        )
        self._open = True
        self._log.info("Verbindung aufgebaut, Device-ID %d", self._device_id.value)
        self.set_timeout(cfg.timeout_ms)

    @staticmethod
    def _check(rc: int, function: str, detail: str = "") -> None:
        """Jeden TMCTL-Rueckgabewert pruefen, Fehlercode hexadezimal melden."""
        if rc != 0:
            raise TmctlError(function, rc, detail)

    # -- Basisoperationen ---------------------------------------------------

    def set_timeout(self, timeout_ms: int) -> None:
        """Kommunikationstimeout setzen (Einheit ZU VERIFIZIEREN)."""
        self._check(self._tm.TmcSetTimeout(self._device_id, timeout_ms), "TmcSetTimeout")

    def write(self, command: str) -> None:
        """Programmnachricht senden.

        Es wird bewusst KEIN Terminator angehaengt: TMCTL setzt ihn selbst
        (verifiziert mit '*IDN?').
        ZU VERIFIZIEREN: Verhalten bei mit ';' verketteten Kommandos.
        """
        payload = command.encode("ascii")
        if len(payload) + 1 > MAX_PROGRAM_MESSAGE_BYTES:
            raise ProtocolError(
                f"Programmnachricht zu lang ({len(payload)} Bytes), "
                f"Limit inkl. Terminator {MAX_PROGRAM_MESSAGE_BYTES} Bytes"
            )
        self._log.debug("TX: %r", command)
        self._check(self._tm.TmcSend(self._device_id, payload), "TmcSend", command)

    def read(self) -> bytes:
        """Einen Lesevorgang ausfuehren und die Rohbytes zurueckgeben."""
        size = self._config.read_buffer_size
        buffer = ct.create_string_buffer(size)
        received = ct.c_int(0)
        self._check(
            self._tm.TmcReceive(self._device_id, buffer, size, ct.byref(received)),
            "TmcReceive",
        )
        data = buffer.raw[: received.value]
        if received.value >= size:
            self._log.warning(
                "Lesepuffer (%d Bytes) vollstaendig gefuellt - Antwort evtl. unvollstaendig", size
            )
        self._log.debug("RX: %d Bytes", len(data))
        return data

    def query(self, command: str) -> bytes:
        """Query senden und einen Lesevorgang ausfuehren."""
        self.write(command)
        return self.read()

    def close(self) -> None:
        """Verbindung schliessen. Mehrfachaufruf ist unschaedlich."""
        if not self._open:
            return
        self._open = False
        rc = self._tm.TmcFinish(self._device_id)
        if rc != 0:
            self._log.warning("TmcFinish meldete Fehlercode 0x%08X", rc)
        else:
            self._log.info("Verbindung geschlossen")

    # -- Context Manager ----------------------------------------------------

    def __enter__(self) -> "TmctlTransport":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()


# ---------------------------------------------------------------------------
# NEU (M1-2): Ersatzgeraet fuer die Testsuite
# ---------------------------------------------------------------------------

# Was in der Antworttabelle stehen darf. Ein Callable bekommt das Kommando in
# Originalschreibweise und liefert die Antwort; eine Liste wird Aufruf fuer
# Aufruf abgearbeitet (der letzte Eintrag bleibt danach stehen). Damit lassen
# sich Messreihen mit wechselnden Werten hinterlegen, ohne einen Zaehler von
# Hand zu fuehren.
FakeReply = bytes | str
FakeEntry = FakeReply | Callable[[str], FakeReply] | list[FakeReply]


def float_block(values: Iterable[float], digits: int = 4) -> bytes:
    """Messwerte in einen '#nNNNN'-Block giessen (IEEE single, MSB first).

    Gegenstueck zu 'wt3000_numeric.parse_float_block()'. Ein 'int' wird als
    rohes 4-Byte-Bitmuster uebernommen - so lassen sich die Sentinel FLOAT_NO_DATA
    (NAN) und FLOAT_OVERRANGE (INF) unveraendert einspeisen, die als IEEE-Zahl
    voellig unauffaellig aussehen.
    """
    payload = b"".join(
        struct.pack(">I", v) if isinstance(v, int) else struct.pack(">f", float(v))
        for v in values
    )
    header = f"#{digits}{len(payload):0{digits}d}".encode("ascii")
    return header + payload


class FakeTransport:
    """Transport ohne Geraet und ohne tmctl.dll - erfuellt das Transport-Protocol.

    Zweck: 'WTSession', 'query_block()', die Item-Tabelle und die gesamte
    Messschleife pruefbar machen. Die bisherige 'FakeSession' aus
    'tests/conftest.py' setzt eine Ebene hoeher an und laesst genau die Regeln
    ungeprueft, die WTSession selbst durchsetzt.

    Verhalten im Einzelnen:

    responses
        Abbildung Kommando -> Antwort, unabhaengig von Gross-/Kleinschreibung
        und vom abschliessenden '?'. Fehlt ein Eintrag, wird ein KeyError
        geworfen statt still etwas zu erfinden: eine nicht hinterlegte Abfrage
        soll auffallen. Das ist bewusst dasselbe Verhalten wie bei FakeSession.

    chunk_size
        Groesse eines einzelnen Lesevorgangs. Ist sie gesetzt, wird jede
        Antwort in mehrere read()-Haeppchen zerlegt - genau der Fall, fuer den
        'WTSession._assemble_block()' die Nachlese-Schleife besitzt. Ohne
        diesen Schalter waere dieser Zweig nie getestet.

    error_queue
        Antworten auf ':STATus:ERRor?'. Sie werden der Reihe nach ausgegeben;
        ist die Liste leer, kommt der Ruhewert '0,"No error"'. Damit laesst
        sich 'assert_no_error()' in beide Richtungen pruefen.

    fail_commands
        Kommandos, die einen TmctlError ausloesen - der simulierte
        Verbindungsabbruch fuer 'drain_after_failure()' und spaeter M3-4.

    written
        Protokoll aller gesendeten Programmnachrichten in Reihenfolge.
    """

    #: Ruhewert der Fehlerqueue, wenn nichts anliegt.
    NO_ERROR: str = '0,"No error"'

    def __init__(
        self,
        responses: dict[str, FakeEntry] | None = None,
        *,
        chunk_size: int | None = None,
        error_queue: Sequence[str] | None = None,
        fail_commands: Iterable[str] = (),
    ) -> None:
        self._log = logging.getLogger("wt3000.transport.fake")
        self.responses: dict[str, FakeEntry] = {
            self._key(k): v for k, v in (responses or {}).items()
        }
        self.written: list[str] = []
        self.timeouts_ms: list[int] = []
        self.closed = False
        self.reads = 0
        self.chunk_size = chunk_size
        self.error_queue: list[str] = list(error_queue or ())
        self.fail_commands: set[str] = {self._key(c) for c in fail_commands}
        # Noch nicht abgeholte Haeppchen der zuletzt beantworteten Abfrage.
        self._pending: list[bytes] = []

    # -- Hilfsmittel --------------------------------------------------------

    @staticmethod
    def _key(command: str) -> str:
        """Kommandos vergleichbar machen: ohne '?', ohne Rand, in Grossschrift."""
        return command.strip().rstrip("?").upper()

    def prime(self, data: bytes | str) -> None:
        """Rohbytes so hinterlegen, dass der naechste read() sie liefert.

        Gebraucht fuer den Fall, den 'drain_after_failure()' abraeumen soll:
        eine verspaetete Antwort, die keiner Abfrage mehr zugeordnet ist.
        """
        self._pending.extend(self._split(self._as_bytes(data)))

    @staticmethod
    def _as_bytes(reply: FakeReply) -> bytes:
        if isinstance(reply, bytes):
            return reply
        # Der Terminator gehoert zum Draht, nicht zur Antwort - WTSession.decode()
        # streift ihn wieder ab. Ihn hier mitzuliefern haelt den Test ehrlich.
        return f"{reply}\r\n".encode("ascii")

    def _split(self, data: bytes) -> list[bytes]:
        """Antwort in Lesevorgaenge zerlegen."""
        if not self.chunk_size or self.chunk_size <= 0:
            return [data]
        return [
            data[i : i + self.chunk_size] for i in range(0, len(data), self.chunk_size)
        ] or [b""]

    def _lookup(self, command: str) -> bytes:
        """Antwort zu einem Kommando bestimmen und in Bytes wandeln."""
        key = self._key(command)

        # Die Fehlerqueue wird nicht aus der Tabelle bedient: sie leert sich
        # beim Lesen, genau wie am Geraet (':STATus:ERRor?' entfernt den Eintrag).
        if key == ":STATUS:ERROR" and key not in self.responses:
            entry = self.error_queue.pop(0) if self.error_queue else self.NO_ERROR
            return self._as_bytes(entry)

        if key not in self.responses:
            raise KeyError(
                f"FakeTransport hat keine Antwort fuer {command!r}. "
                "Eintrag in 'responses' ergaenzen oder den Aufruf pruefen."
            )

        entry = self.responses[key]
        if callable(entry):
            entry = entry(command)
        elif isinstance(entry, list):
            if not entry:
                raise KeyError(f"FakeTransport: Antwortliste fuer {command!r} ist leer")
            # Der letzte Eintrag bleibt stehen, damit eine Messschleife
            # beliebig lange weiterlaufen kann.
            entry = entry.pop(0) if len(entry) > 1 else entry[0]
        return self._as_bytes(entry)

    # -- Transport-Protocol -------------------------------------------------

    def set_timeout(self, timeout_ms: int) -> None:
        """Timeout nur protokollieren - hier gibt es keine Leitung."""
        self.timeouts_ms.append(timeout_ms)

    def write(self, command: str) -> None:
        """Programmnachricht entgegennehmen und merken."""
        if self.closed:
            raise TmctlError("TmcSend", 0x1, "Transport ist geschlossen")
        payload = command.encode("ascii")
        if len(payload) + 1 > MAX_PROGRAM_MESSAGE_BYTES:
            raise ProtocolError(
                f"Programmnachricht zu lang ({len(payload)} Bytes), "
                f"Limit inkl. Terminator {MAX_PROGRAM_MESSAGE_BYTES} Bytes"
            )
        if self._key(command) in self.fail_commands:
            raise TmctlError("TmcSend", 0xDEAD, command)
        self._log.debug("TX: %r", command)
        self.written.append(command)

    def read(self) -> bytes:
        """Einen Lesevorgang liefern.

        Ist nichts vorbereitet, verhaelt sich der FakeTransport wie ein
        schweigendes Geraet: TmctlError statt einer leeren Antwort. Das ist der
        Fall, den 'drain_after_failure()' erwartet und abfaengt.
        """
        self.reads += 1
        if not self._pending:
            raise TmctlError("TmcReceive", 0x2, "nichts zu lesen (simulierter Timeout)")
        return self._pending.pop(0)

    def query(self, command: str) -> bytes:
        """Query senden und den ersten Lesevorgang liefern."""
        self.write(command)
        if self._key(command) in self.fail_commands:
            raise TmctlError("TmcReceive", 0xDEAD, command)
        self._pending.extend(self._split(self._lookup(command)))
        return self.read()

    def close(self) -> None:
        """Verbindung schliessen. Mehrfachaufruf ist unschaedlich."""
        self.closed = True

    # -- Context Manager ----------------------------------------------------

    def __enter__(self) -> "FakeTransport":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()


# ---------------------------------------------------------------------------
# Offene Fugen (ROADMAP M1-2, bewusst nicht gebaut)
# ---------------------------------------------------------------------------
#
# class SocketTransport:
#     """VXI-11 bzw. Raw-Socket ueber Port 10001 - ohne TMCTL-DLL und ohne
#     Windows. Erst bauen, wenn eine Messaufgabe es verlangt; das Protocol
#     oben ist die einzige Stelle, an der es andocken muss."""
#
# class VisaTransport:
#     """pyvisa-Anbindung ('TCPIP::<ip>::INSTR'). Gleiche Begruendung."""
