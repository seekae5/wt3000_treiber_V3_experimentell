# =============================================================================
# Datei: stage4_measure.py
# Layer 4 - Stufe 4: Messschleife mit HOLD-Snapshot, Zeitstempel, CSV und
#                    sauberer Abbruchbehandlung.
#
# Geschrieben werden AUSSCHLIESSLICH: Item-Tabelle, NUMber, :NUMeric:HOLD.
# Ranges, Wiring, Filter, Skalierung, Update-Rate und Frequenzmessquelle
# bleiben unangetastet. Der Ausgangszustand wird am Ende wiederhergestellt.
# =============================================================================

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

# UEBERARBEITET (Punkt 4, src-Layout): paketrelative Importe.
# Start ab jetzt ueber 'python -m wt3000_scpi.stage4_measure' - ein direkter
# Aufruf der Datei kann relative Importe nicht aufloesen.
from .wt3000_common import output_dir, setup_logging  # UEBERARBEITET (F-08)
from .wt3000_core import (
    TmctlTransport,
    WTConfig,
    WTError,
    WTSession,
    config_file_in_use,
)
from .wt3000_itemspec import (
    apply_item_table,
    build_item_table,
    probe_extra_items,
    probe_item_write_capability,  # UEBERARBEITET (F-09)
    restore_item_table,
    save_backup_bundle,
    verify_item_table,
)
from .wt3000_measure import (
    build_standard_profile,
    run_measurement_loop,
    write_metadata,
)
# UEBERARBEITET (ROADMAP M4-2): CsvRecorder heisst CsvSink und wohnt jetzt bei
# den uebrigen Ausgabeformaten.
from .wt3000_sinks import CsvSink
from .wt3000_numeric import ItemTable, NumericItem

# ---------------------------------------------------------------------------
# Laufparameter - hier anpassen
# ---------------------------------------------------------------------------

# Abtastintervall. Sollte mindestens :RATE? entsprechen (aktuell 1.00E+00 s);
# schnelleres Abfragen liefert nur Wiederholungen desselben Datensatzes.
SAMPLE_INTERVAL_S: float = 1.0

# None = laeuft bis Strg+C. Sonst Abbruch beim jeweils ersten erreichten Limit.
MAX_SAMPLES: int | None = 60
MAX_DURATION_S: float | None = None

# HOLD als Zeitstempel-Anker: friert den Datensatz vor dem Lesen ein.
# False spart ein Set-Kommando pro Zyklus, macht den Zeitstempel aber unschaerfer.
USE_HOLD: bool = True

# :STATus:CONDition? je Sample mitschreiben (FOV, PLLE, Overrange, Peak Over).
RECORD_CONDITION: bool = True

# Alle n Samples eine Statuszeile ins Log. 0 = keine.
LOG_EVERY: int = 10

# Fuer deutsches Excel auf ";" setzen. Der Dezimalpunkt bleibt bewusst "." -
# sonst ist die Datei fuer jedes andere Auswertewerkzeug unbrauchbar.
CSV_DELIMITER: str = ","

# Zielverzeichnis fuer CSV, Metadaten, Backup und Protokoll.
# UEBERARBEITET: Ablage an der Projektwurzel statt an 'Path.cwd()'.
# Bis hierher hing das am Arbeitsverzeichnis - ein Start aus einem
# Unterverzeichnis (Entwicklungsumgebungen tun das standardmaessig) legte
# ein zweites gleichnamiges Verzeichnis dort an. Siehe
# wt3000_common.output_dir().
OUTPUT_DIR: Path = output_dir("messungen")

# Freitext, landet in der Metadatendatei.
RUN_COMMENT: str = ""


# UEBERARBEITET (F-08, siehe AENDERUNGEN_2026-08-18.md): setup_logging() lag in
# allen fuenf Stufenskripten als byteweise identische Kopie. Es gibt sie jetzt
# nur noch einmal, in wt3000_common.py; hier wird sie importiert.


def check_preconditions(session: WTSession) -> None:
    """Voraussetzungen pruefen, ohne etwas zu veraendern."""
    log = logging.getLogger("wt3000.stage4")

    header = session.query(":COMMunicate:HEADer?")
    if header.strip() != "0":
        raise WTError(f":COMMunicate:HEADer ist {header!r}, erwartet '0'")

    fmt = session.query(":NUMeric:FORMat?")
    if not fmt.upper().startswith("FLO"):
        raise WTError(f":NUMeric:FORMat ist {fmt!r}, erwartet 'FLO'")

    rate = float(session.query(":RATE?"))
    if SAMPLE_INTERVAL_S < rate:
        log.warning(
            "Abtastintervall %.3f s liegt unter :RATE = %.3f s - "
            "es werden Wiederholungen desselben Datensatzes aufgezeichnet",
            SAMPLE_INTERVAL_S,
            rate,
        )

    condition = int(session.query(":STATus:CONDition?"))
    if condition & (1 << 4):
        log.warning("Condition Bit 4 (FOV): Frequenzmessung im Fehler")
    if condition & (1 << 7):
        log.warning("Condition Bit 7 (PLLE): kein Signal an der PLL-Quelle")
    if condition & 0x0F00:
        log.warning("Condition: Overrange an mindestens einem Element")
    if condition & (1 << 15):
        log.warning("Condition Bit 15 (POV): Peak Over an mindestens einem Eingang")


def main() -> int:
    """Stufe 4 ausfuehren. Rueckgabewert 0 = erfolgreich."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    log_file = OUTPUT_DIR / f"wt3000_stage4_{timestamp}.txt"
    csv_file = OUTPUT_DIR / f"wt3000_measurement_{timestamp}.csv"
    meta_file = OUTPUT_DIR / f"wt3000_measurement_{timestamp}_meta.json"
    backup_file = OUTPUT_DIR / f"wt3000_itemtable_backup_{timestamp}.json"

    setup_logging(log_file)
    log = logging.getLogger("wt3000.stage4")
    log.info("Protokolldatei: %s", log_file)

    specs = build_standard_profile()
    log.info("Stufe 4 - Messschleife (%d Items, Intervall %.3f s)", len(specs), SAMPLE_INTERVAL_S)
    if MAX_SAMPLES is None and MAX_DURATION_S is None:
        log.info("Kein Limit gesetzt - Abbruch mit Strg+C")

    backup: ItemTable | None = None
    tail: list[NumericItem] = []
    exit_code = 0

    try:
        # UEBERARBEITET (Schritt 3 aus MarkDowns/PLAN_AUFRUFKETTE.md, Befund
        # A-08): die Aufloesungskette steht jetzt INNERHALB des try und HINTER
        # setup_logging(). Bis hierher war sie der erste Aufruf von Layer 4 nach
        # Layer 0 - und der einzige, der ausserhalb jeder Absicherung und vor
        # der Einrichtung des Protokolls lag.
        #
        # Sie kann drei WTError werfen: nicht lesbare Datei, kein JSON-Objekt,
        # nicht auswertbarer Feldwert. Eine kaputte 'wt3000.json' - der
        # haeufigste Konfigurationsfehler ueberhaupt - endete deshalb als
        # Traceback statt mit der Zeile "Abbruch: ...", der Rueckgabewert 1 kam
        # aus dem Traceback statt aus dem Skript, und in der Protokolldatei
        # stand nichts, weil es sie noch nicht gab.
        #
        # Die Umstellung kostet nichts: der Name der Protokolldatei haengt nur
        # an OUTPUT_DIR und am Zeitstempel, nicht an der Konfiguration. Die
        # bisherige Reihenfolge war historisch, nicht sachlich.
        #
        # config_file_in_use() steht VOR from_environment(), damit die kaputte
        # Datei auch dann benannt ist, wenn das Lesen scheitert.
        log.info("Konfigurationsdatei: %s", config_file_in_use() or "<keine, Voreinstellungen>")
        config = WTConfig.from_environment()
        log.info("Verbindung: %s", config.describe())

        with TmctlTransport(config) as transport:
            session = WTSession(transport, config, read_only=False)
            if config.use_remote:
                session.enable_remote()

            try:
                try:
                    check_preconditions(session)

                    # 1) Ist-Zustand sichern.
                    backup = ItemTable.read_from_device(session)
                    target = build_item_table(specs)
                    tail = probe_extra_items(
                        session,
                        first_index=len(backup.items) + 1,
                        last_index=len(target.items),
                    )
                    save_backup_bundle(backup_file, backup, tail)

                    # 2) Fail-Fast, dann Tabelle schreiben und verifizieren.
                    probe_item_write_capability(session, target, backup)
                    apply_item_table(session, target)
                    problems = verify_item_table(session, target)
                    if problems:
                        for problem in problems:
                            log.error("Verifikation: %s", problem)
                        raise WTError(
                            f"{len(problems)} Abweichung(en) beim Verifizieren der Tabelle"
                        )

                    # 3) Metadaten sichern, bevor die Messung startet.
                    write_metadata(
                        meta_file,
                        session,
                        target,
                        parameters={
                            "sample_interval_s": SAMPLE_INTERVAL_S,
                            "max_samples": MAX_SAMPLES,
                            "max_duration_s": MAX_DURATION_S,
                            "use_hold": USE_HOLD,
                            "record_condition": RECORD_CONDITION,
                            "csv_file": csv_file.name,
                            "comment": RUN_COMMENT,
                        },
                    )

                    # 4) Messschleife.
                    # UEBERARBEITET (ROADMAP M4-2): Spaltenkopf und Lebenszyklus der
                    # Senke liegen jetzt in der Schleife - hier wird sie nur gebaut.
                    # Ein anderes Ausgabeformat waere an dieser Stelle ein anderer
                    # Klassenname und sonst nichts.
                    log.info("Start der Messung. Abbruch jederzeit mit Strg+C.")
                    stats = run_measurement_loop(
                        session=session,
                        table=target,
                        sink=CsvSink(csv_file, delimiter=CSV_DELIMITER),
                        interval_s=SAMPLE_INTERVAL_S,
                        max_samples=MAX_SAMPLES,
                        max_duration_s=MAX_DURATION_S,
                        use_hold=USE_HOLD,
                        record_condition=RECORD_CONDITION,
                        log_every=LOG_EVERY,
                    )
                    stats.log_summary(SAMPLE_INTERVAL_S)

                    session.assert_no_error("Messschleife")

                except WTError as error:
                    log.error("Abbruch: %s", error)
                    exit_code = 1

                finally:
                    # 5) Ausgangszustand wiederherstellen - in derselben Sitzung.
                    if backup is not None:
                        try:
                            written = restore_item_table(session, backup, tail)
                            log.info("Wiederherstellung abgeschlossen (%d Kommandos)", written)
                            remaining = verify_item_table(session, backup)
                            if remaining:
                                for problem in remaining:
                                    log.error("Restore-Kontrolle: %s", problem)
                                exit_code = 1
                            else:
                                log.info(
                                    "Restore-Kontrolle: Ausgangszustand exakt wiederhergestellt"
                                )
                        except WTError as error:
                            log.error(
                                "Wiederherstellung fehlgeschlagen: %s - Backup: %s",
                                error,
                                backup_file,
                            )
                            exit_code = 1
            finally:
                # UEBERARBEITET (Schritt 1 aus MarkDowns/PLAN_AUFRUFKETTE.md, Befund A-01):
                # eigenes 'finally' um den gesamten Nutzteil. Vorher stand dieser Aufruf
                # im RUMPF des Wiederherstellungs-finally, hinter einem 'except WTError'.
                # Jede andere Ausnahme - ein KeyError aus dem Restore, ein Strg+C -
                # uebersprang ihn und lief aus dem 'with TmctlTransport(...)' heraus: der
                # Transport war dann zu, ':COMMunicate:REMote OFF' nicht mehr moeglich,
                # das Bedienfeld blieb gesperrt. Der Anwender musste am Geraet LOCAL
                # druecken.
                #
                # Das ist die Fassung, die Stufe 2 seit F-07 hat. Sie ist gefahrlos, weil
                # disable_remote() selbst idempotent ist (WTSession._remote_active) und
                # WTError intern abfaengt - der Aufruf kann eine gerade laufende Ausnahme
                # also nicht verdraengen.
                session.disable_remote()

    except WTError as error:
        # UEBERARBEITET (Schritt 3, Befund A-08): "Verbindungsfehler" stimmt
        # nicht mehr - seit die Aufloesungskette in diesem try liegt, faengt
        # dieser Zweig auch eine kaputte 'wt3000.json'. Das ist kein
        # Verbindungsfehler, und die Meldung schickte damit in die Irre.
        # "Abbruch" ist ausserdem das Wort, das die uebrigen fuenf Skripte an
        # dieser Stelle schon benutzten.
        log.error("Abbruch: %s", error)
        if backup is not None:
            log.error("Backup liegt unter: %s", backup_file)
        return 1

    log.info("=" * 78)
    log.info("Messdaten:  %s", csv_file)
    log.info("Metadaten:  %s", meta_file)
    log.info("Backup:     %s", backup_file)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
