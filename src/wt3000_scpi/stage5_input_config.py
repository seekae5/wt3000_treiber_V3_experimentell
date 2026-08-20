# =============================================================================
# Datei: stage5_input_config.py
# Layer 4 - Stufe 5: Eingangskonfiguration erfassen und dokumentieren.
#
# Dieses Skript SCHREIBT NICHTS. Es oeffnet die Sitzung mit read_only=True und
# das Konfigurationsobjekt mit allow_changes=False - zwei unabhaengige Sperren.
# Zweck: den eingemessenen Ist-Zustand als JSON sichern, bevor jemals ein
# Schreibversuch am realen Geraet stattfindet.
# =============================================================================

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

# UEBERARBEITET (Punkt 4, src-Layout): paketrelative Importe.
# Start ab jetzt ueber 'python -m wt3000_scpi.stage5_input_config' - ein direkter
# Aufruf der Datei kann relative Importe nicht aufloesen.
from .wt3000_common import output_dir, setup_logging  # UEBERARBEITET (F-08)
from .wt3000_core import (
    TmctlTransport,
    WTConfig,
    WTError,
    WTSession,
    config_file_in_use,
)
from .wt3000_input import InputConfig, InputSnapshot

# Zielverzeichnis fuer Snapshot und Protokoll.
# UEBERARBEITET: Ablage an der Projektwurzel statt an 'Path.cwd()'.
# Bis hierher hing das am Arbeitsverzeichnis - ein Start aus einem
# Unterverzeichnis (Entwicklungsumgebungen tun das standardmaessig) legte
# ein zweites gleichnamiges Verzeichnis dort an. Siehe
# wt3000_common.output_dir().
OUTPUT_DIR: Path = output_dir("konfiguration")


# UEBERARBEITET (F-08, siehe AENDERUNGEN_2026-08-18.md): setup_logging() lag in
# allen fuenf Stufenskripten als byteweise identische Kopie. Es gibt sie jetzt
# nur noch einmal, in wt3000_common.py; hier wird sie importiert.


def main() -> int:
    """Stufe 5 ausfuehren. Rueckgabewert 0 = erfolgreich."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    log_file = OUTPUT_DIR / f"wt3000_stage5_{timestamp}.txt"
    snapshot_file = OUTPUT_DIR / f"wt3000_inputconfig_{timestamp}.json"
    dump_file = OUTPUT_DIR / f"wt3000_inputdump_{timestamp}.txt"

    setup_logging(log_file)
    log = logging.getLogger("wt3000.stage5")
    log.info("Protokolldatei: %s", log_file)
    log.info("Stufe 5 - Eingangskonfiguration erfassen (nur Lesen)")

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
            # read_only=True: jedes Nicht-Query-Kommando wirft ReadOnlyViolation.
            # Deshalb wird hier auch KEIN ':COMMunicate:REMote ON' gesendet.
            session = WTSession(transport, config, read_only=True)
            if config.use_remote:
                log.warning(
                    "use_remote=True wird in Stufe 5 ignoriert - "
                    "REMote ON waere ein Schreibkommando"
                )

            cfg = InputConfig(session, allow_changes=False)

            snapshot = InputSnapshot.capture(cfg)
            snapshot.log_summary()

            log.info("Wiring-Units:")
            for unit in cfg.get_wiring_units():
                log.info(
                    "  %-6s %-5s -> Elemente %s",
                    unit.name or "(unbenannt)",
                    unit.pattern,
                    ", ".join(str(e) for e in unit.elements),
                )

            snapshot.save(snapshot_file)
            dump_file.write_text(snapshot.raw_dump, encoding="utf-8")
            log.info("Rohabzug von ':INPut?' gesichert nach %s", dump_file)

            # Gegenprobe: laden, erneut erfassen, vergleichen. Damit ist
            # nachgewiesen, dass Serialisierung und Parser verlustfrei sind.
            reloaded = InputSnapshot.load(snapshot_file)
            problems = reloaded.diff(InputSnapshot.capture(cfg))
            if problems:
                for problem in problems:
                    log.error("Gegenprobe: %s", problem)
                raise WTError("Snapshot und Geraetezustand weichen voneinander ab")
            log.info("Gegenprobe erfolgreich: Snapshot bildet den Ist-Zustand exakt ab")

            session.assert_no_error("Konfigurationserfassung")

    except WTError as error:
        log.error("Abbruch: %s", error)
        return 1

    log.info("=" * 78)
    log.info("Snapshot:  %s", snapshot_file)
    log.info("Rohabzug:  %s", dump_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
