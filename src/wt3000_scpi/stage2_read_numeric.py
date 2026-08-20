# =============================================================================
# Datei: stage2_read_numeric.py
# Layer 4 - Stufe 2: Messwerte gegen die VORHANDENE Item-Tabelle lesen.
#
# Diese Stufe veraendert die Item-Tabelle NICHT. Sie sichert sie, liest
# mehrfach Werte und stellt beim Beenden sicher, dass die Tabelle unveraendert
# ist. Ranges, Wiring und Filter werden nicht angefasst.
# =============================================================================

from __future__ import annotations

import logging
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

# UEBERARBEITET (Punkt 4, src-Layout): paketrelative Importe.
# Start ab jetzt ueber 'python -m wt3000_scpi.stage2_read_numeric' - ein direkter
# Aufruf der Datei kann relative Importe nicht aufloesen.
from .wt3000_common import output_dir, setup_logging  # UEBERARBEITET (F-08)
from .wt3000_core import TmctlTransport, WTConfig, WTError, WTSession
from .wt3000_numeric import ItemTable, ValueStatus, read_numeric_values

# Anzahl der Lesedurchlaeufe.
READ_CYCLES: int = 3

# Pollingabstand. Sollte mindestens dem :RATE?-Wert entsprechen; schnelleres
# Abfragen liefert nur Wiederholungen. Aktuell gemessen: 1.00E+00 s.
POLL_INTERVAL_S: float = 1.0

# Auf True setzen, um den Schreibpfad der Wiederherstellung bewusst einmal
# durchlaufen zu lassen: schreibt alle Items mit ihren EIGENEN Werten zurueck.
# Damit laesst sich pruefen, ob das Geraet die Kurzform-Funktionsnamen aus der
# Antwort (z.B. 'UTHDG', 'LAMB') auch als Eingabe akzeptiert.
EXERCISE_RESTORE_WRITE: bool = False

# Zielverzeichnis fuer Protokoll und Sicherung.
#
# UEBERARBEITET (Schritt 0b aus MarkDowns/PLAN_AUFRUFKETTE.md, Befund A-10):
# stand bis hierher als 'ziel = output_dir()' INNERHALB von main(). Fuenf der
# sieben ausfuehrbaren Skripte fuehrten die Modulkonstante, zwei den Aufruf -
# derselbe Zweck in zwei Fassungen. Vereinheitlicht wurde auf die Konstante,
# und zwar nicht wegen der Mehrheit, sondern weil sie ERSETZBAR ist: ein
# 'monkeypatch.setattr(modul, "OUTPUT_DIR", tmp_path)' trifft genau einen
# Namen, waehrend ein Ersetzen von 'output_dir' die Funktion fuer jeden
# weiteren Aufruf im selben Modul mitveraendern wuerde. Genau daran haengt es,
# dass main() im Test vollstaendig durchspielbar ist (Befund A-13).
#
# ZU BEACHTEN - der Import tut damit etwas: output_dir() laeuft ueber
# find_project_root(), das vom Arbeitsverzeichnis aus aufwaerts 'exists()' auf
# drei Marker prueft. Das ist ein LESENDER Dateisystemzugriff beim blossen
# Import. Er ist zugelassen und in tests/test_package_layout.py als Grenze
# festgehalten: 'test_import_legt_keine_datei_an' verlangt, dass beim Import
# nichts ENTSTEHT - kein mkdir, keine Protokolldatei, kein Backup.
#
# Aufgeloest wird die Fuge in Schritt 8: sobald main() ein 'output_dir'
# entgegennimmt, ist diese Konstante nur noch der Vorgabewert.
OUTPUT_DIR: Path = output_dir()


# UEBERARBEITET (F-08, siehe AENDERUNGEN_2026-08-18.md): setup_logging() lag in
# allen fuenf Stufenskripten als byteweise identische Kopie. Es gibt sie jetzt
# nur noch einmal, in wt3000_common.py; hier wird sie importiert.


def check_preconditions(session: WTSession) -> None:
    """Voraussetzungen pruefen, ohne etwas zu veraendern."""
    log = logging.getLogger("wt3000.stage2")

    header = session.query(":COMMunicate:HEADer?")
    if header.strip() != "0":
        raise WTError(
            f":COMMunicate:HEADer ist {header!r}, erwartet '0'. "
            "Mit Headern schlaegt das Parsen der Item-Tabelle fehl."
        )

    fmt = session.query(":NUMeric:FORMat?")
    if not fmt.upper().startswith("FLO"):
        raise WTError(
            f":NUMeric:FORMat ist {fmt!r}, erwartet 'FLO'. "
            "Dieses Skript liest ausschliesslich Binaerbloecke."
        )

    rate = session.query(":RATE?")
    log.info("Datenaktualisierungsintervall: %s s (Polling: %.2f s)", rate, POLL_INTERVAL_S)

    condition = session.query(":STATus:CONDition?")
    bits = int(condition)
    if bits & (1 << 4):
        log.warning("Condition-Register Bit 4 (FOV): Frequenzmessung im Fehler")
    if bits & (1 << 7):
        log.warning("Condition-Register Bit 7 (PLLE): kein Signal an der PLL-Quelle")
    if bits & 0x0F00:
        log.warning("Condition-Register: Overrange an mindestens einem Element")

    hold = session.query(":NUMeric:HOLD?")
    log.info("NUMeric:HOLD = %s (in Stufe 2 nicht genutzt)", hold)


# UEBERARBEITET (F-06, siehe AENDERUNGEN_2026-08-18.md): log_reading() bekommt
# die Sitzung jetzt als Parameter - wie read_and_log() in Stufe 3. Vorher lief
# der Zugriff ueber das modulweite '_SESSION', das erst in main() gesetzt wurde:
# jeder Aufruf ausserhalb von main() (Import, Test, Wiederverwendung als
# Bibliothek) traf auf None und lief in einen AttributeError auf None statt in
# eine verstaendliche Fehlermeldung. Die Hilfsfunktion read_numeric_values_for() und
# die Modulvariable _SESSION sind damit ersatzlos entfallen.
def log_reading(session: WTSession, table: ItemTable, cycle: int) -> Counter:
    """Einen Lesedurchlauf ausgeben und die Statusverteilung zurueckgeben."""
    log = logging.getLogger("wt3000.stage2")
    values = read_numeric_values(session, expected_count=len(table.items))

    log.info("-" * 78)
    log.info("Lesedurchlauf %d", cycle)
    log.info("%-4s %-14s %-10s %s", "Idx", "Name", "Status", "Wert")

    statistics: Counter = Counter()
    for item, value in zip(table.items, values):
        statistics[value.status] += 1
        log.info("%-4d %-14s %-10s %s", item.index, item.key, value.status.value, value)
    return statistics


def main() -> int:
    """Stufe 2 ausfuehren. Rueckgabewert 0 = erfolgreich."""
    # UEBERARBEITET (P-7): Verbindungsparameter aus der Auflaesungskette -
    # WT3000_*-Umgebungsvariablen oder 'wt3000.json'. Siehe README.
    config = WTConfig.from_environment()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = OUTPUT_DIR / f"wt3000_stage2_{timestamp}.txt"
    backup_file = OUTPUT_DIR / f"wt3000_itemtable_backup_{timestamp}.json"
    setup_logging(log_file)
    log = logging.getLogger("wt3000.stage2")
    log.info("Protokolldatei: %s", log_file)
    log.info("Ausgabeverzeichnis: %s", OUTPUT_DIR)
    log.info("Stufe 2 - Messwerte gegen die vorhandene Item-Tabelle lesen (FLOat)")

    backup: ItemTable | None = None
    session: WTSession | None = None

    try:
        with TmctlTransport(config) as transport:
            session = WTSession(transport, config, read_only=False)

            if config.use_remote:
                session.enable_remote()

            # UEBERARBEITET (F-07, siehe AENDERUNGEN_2026-08-18.md): try/finally
            # um den Nutzteil, damit ':COMMunicate:REMote OFF' garantiert faellt.
            # Vorher schaltete nur die zweite (Wiederherstellungs-)Sitzung die
            # Fernsteuerung wieder ab. Brach der Lauf ab, bevor 'backup' gesetzt
            # war, wurde diese zweite Sitzung nie geoeffnet - das Geraet blieb
            # mit gesperrtem Bedienfeld zurueck. Stufe 3 und 4 machen es an
            # dieser Stelle bereits so.
            try:
                check_preconditions(session)

                # 1) Bestehende Tabelle sichern - als Erstes, vor allem anderen.
                backup = ItemTable.read_from_device(session)
                backup.save(backup_file)
                log.info("Gesicherte Items:")
                for item in backup.items:
                    log.info("  ITEM%-3d %-20s -> %s", item.index, item.argument, item.key)

                # 2) Messwerte lesen.
                for cycle in range(1, READ_CYCLES + 1):
                    statistics = log_reading(session, backup, cycle)
                    log.info(
                        "Statusverteilung: OK=%d, NO_DATA=%d, OVERRANGE=%d",
                        statistics[ValueStatus.OK],
                        statistics[ValueStatus.NO_DATA],
                        statistics[ValueStatus.OVERRANGE],
                    )
                    if cycle < READ_CYCLES:
                        time.sleep(POLL_INTERVAL_S)

                session.assert_no_error("Messwertabfrage")

            finally:
                session.disable_remote()

    except WTError as exc:
        log.error("Abbruch: %s", exc)
        log.error("Backup der Item-Tabelle liegt unter: %s", backup_file)
        return 1

    finally:
        # 3) Wiederherstellung. Die Verbindung ist an dieser Stelle bereits
        #    geschlossen, daher wird eine zweite kurze Sitzung geoeffnet.
        if backup is not None:
            try:
                with TmctlTransport(config) as transport:
                    restore_session = WTSession(transport, config, read_only=False)
                    if config.use_remote:
                        restore_session.enable_remote()
                    try:
                        backup.restore_to_device(restore_session, force=EXERCISE_RESTORE_WRITE)
                    finally:
                        restore_session.disable_remote()
            except WTError as exc:
                logging.getLogger("wt3000.stage2").error(
                    "Wiederherstellung fehlgeschlagen: %s - Backup: %s", exc, backup_file
                )

    log.info("=" * 78)
    log.info("Stufe 2 beendet. Item-Tabelle gesichert unter %s", backup_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
