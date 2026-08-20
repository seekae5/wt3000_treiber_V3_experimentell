# =============================================================================
# Datei: tools/hardware/probe_voltage_range.py
#
# GERAETESKRIPT. Baut eine echte Verbindung auf und SCHREIBT einen Messbereich.
#
# Liegt bewusst nicht unter tests/: die Testsuite laeuft ohne Geraet und ohne
# tmctl.dll, und tests/conftest.py setzt das aktiv durch. Aufruf:
#
#     python tools/hardware/probe_voltage_range.py
#
# (verlangt ein installiertes Paket - 'pip install -e .' - oder PYTHONPATH=src)
#
# Zweck: offener Punkt M0-1 der ROADMAP. Sendet EINEN Wert ueber
# RangeAccess.set_range() (wt3000_rangeio.py) an ein unkritisches Element und
# liest ihn zurueck. Beantwortet Befund B-01 damit noch nicht abschliessend -
# dafuer muessten mehrere Schreibweisen nacheinander probiert werden (siehe
# stage5b_range_probe.py als Vorbild). Dies ist der einfache erste Schritt:
# EIN Wert, EIN Element, mit Sicherung und Rueckstellung.
#
# Sicherheitsmassnahmen (UEBERARBEITET, Schritt 2 aus
# MarkDowns/PLAN_AUFRUFKETTE.md, Befund A-02):
#   - Element 4 (Direkteingang, unkritisch fuer diese Probe)
#   - Ausgangswert wird vor dem Schreiben gelesen und im 'finally' wieder
#     gesetzt - also auch bei einem Timeout beim Ruecklesen und bei Strg+C.
#     Bis Schritt 2 stand die Rueckstellung ungeschuetzt hinter dem Ruecklesen;
#     die Zusage galt nur auf dem glatten Weg.
#   - Fehlerqueue wird geprueft, NACHDEM zurueckgestellt wurde
#   - Scheitert die Rueckstellung selbst, nennt die Fehlermeldung den Sollwert,
#     der am Geraet von Hand einzustellen ist
#
# Das Urteil faellt maschinell: der zurueckgelesene Wert wird mit dem gesendeten
# verglichen, und main() liefert 1, wenn das Geraet ihn nicht uebernommen hat.
# Vorher gingen beide Werte nur ins Protokoll und der Rueckgabewert war immer 0 -
# der Beleg fuer M0-1 musste von Hand aus der Datei gelesen werden.
#
# REMOTE steht als Modulkonstante USE_REMOTE im Skript, nicht in der
# Konfiguration. Begruendung an der Konstante selbst.
# =============================================================================

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from wt3000_scpi.wt3000_common import output_dir, setup_logging
from wt3000_scpi.wt3000_core import (
    TmctlTransport,
    WTConfig,
    WTError,
    WTSession,
    config_file_in_use,
)
from wt3000_scpi.wt3000_rangeio import (
    Quantity,
    RangeAccess,
    RangeValue,
    ranges_match,
)

# ---------------------------------------------------------------------------
# Laufparameter
# ---------------------------------------------------------------------------

ELEMENT: int = 4
TEST_VALUE: float = 1000.0

#: Fernsteuerung waehrend der Probe. Bewusst NICHT aus 'config.use_remote':
#
# M0-1 fragt nach der SYNTAX, M0-3 nach der NOTWENDIGKEIT von REMOTE. Haengt
# dieses Skript an der Konfiguration, entscheidet eine Umgebungsvariable oder
# eine Zeile in 'wt3000.json' ueber den Versuchsaufbau - ohne im Protokoll
# aufzutauchen. Ein fehlgeschlagener Rueckleseversuch waere dann keiner der
# beiden Ursachen mehr zuzuordnen, und genau diese Trennung ist der Zweck des
# Skripts.
#
# 'True' und nicht 'False', weil REMOTE ON der Zustand ist, in dem ein
# Schreibzugriff am sichersten angenommen wird. Schlaegt der Rueckleseabgleich
# TROTZDEM fehl, liegt es an der Syntax - das ist die Aussage, die gebraucht
# wird. Den Gegenversuch ohne REMOTE fuehrt stage5b_range_probe.py, das genau
# dafuer gebaut ist.
USE_REMOTE: bool = True

# UEBERARBEITET: Ablage an der Projektwurzel statt an 'Path.cwd()'.
# Bis hierher hing das am Arbeitsverzeichnis - ein Start aus einem
# Unterverzeichnis (Entwicklungsumgebungen tun das standardmaessig) legte
# ein zweites gleichnamiges Verzeichnis dort an. Siehe
# wt3000_common.output_dir().
OUTPUT_DIR: Path = output_dir("konfiguration")


def main() -> int:
    """Einen Wert per rangeio setzen und zuruecklesen. Rueckgabe: 0 = ok."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = OUTPUT_DIR / f"wt3000_probe_voltage_range_{timestamp}.txt"

    setup_logging(log_file)
    log = logging.getLogger("wt3000.probe_voltage_range")
    log.info("Protokolldatei: %s", log_file)

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
            access = RangeAccess(session, allow_changes=True)

            if USE_REMOTE:
                session.enable_remote()
            log.info(
                "Fernsteuerung: %s (Modulkonstante, nicht aus der Konfiguration)",
                "ON" if USE_REMOTE else "OFF",
            )

            try:
                original = access.get_range(Quantity.VOLTAGE, ELEMENT)
                log.info(
                    "Ausgangswert Element %d: %s", ELEMENT, original.describe(Quantity.VOLTAGE)
                )

                # UEBERARBEITET (Schritt 2 aus MarkDowns/PLAN_AUFRUFKETTE.md,
                # Befund A-02): try/finally um den Schreibteil. Vorher lagen
                # zwischen dem Schreiben des Testwerts und der Rueckstellung ein
                # Query und zwei Protokollausgaben, ohne jede Absicherung - jede
                # Ausnahme dort, und ein Strg+C an jeder Stelle, liess TEST_VALUE
                # auf einem eingemessenen Geraet stehen. Der Dateikopf sagte die
                # Rueckstellung trotzdem zu.
                try:
                    command = access.set_range(Quantity.VOLTAGE, ELEMENT, TEST_VALUE)
                    log.info("Gesendet: %s", command)

                    readback = access.get_range(Quantity.VOLTAGE, ELEMENT)
                    log.info("Zurueckgelesen: %s", readback.describe(Quantity.VOLTAGE))

                    # UEBERARBEITET (Befund A-02): das Urteil faellt hier, nicht
                    # beim Lesen des Protokolls. Vorher gingen beide Werte nur ins
                    # Log und main() lieferte auch dann 0, wenn das Geraet den Wert
                    # gar nicht uebernommen hatte - der Beleg fuer M0-1 musste von
                    # Hand aus der Datei gezogen werden.
                    #
                    # ranges_match() und nicht values_match(): es vergleicht die
                    # Eingangsart mit. 10 A direkt und 10 V am Sensoreingang sind
                    # nicht derselbe Zustand, auch bei gleichem Zahlenwert.
                    erwartet = RangeValue(TEST_VALUE, sensor=False)
                    if ranges_match(erwartet, readback):
                        log.info(
                            "BELEG M0-1: Wert uebernommen - '%s' ist gueltige Syntax",
                            command,
                        )
                    else:
                        log.error(
                            "BELEG M0-1: gesendet %s, zurueckgelesen %s - NICHT uebernommen",
                            erwartet.describe(Quantity.VOLTAGE),
                            readback.describe(Quantity.VOLTAGE),
                        )
                        exit_code = 1

                finally:
                    # Auch bei Strg+C zwischen Schreiben und Ruecklesen. Ein
                    # Fehlschlag HIER wird protokolliert und nicht geworfen: sonst
                    # verdraengte er die urspruengliche Ausnahme. Dieselbe Haltung
                    # wie in Stufe 3 und 4 bei restore_item_table(). Die Meldung
                    # nennt den Wert, den jemand am Geraet von Hand zuruecksetzen
                    # muss - das ist die wichtigste Zeile, wenn es schiefgeht.
                    try:
                        zurueck = access.set_range(
                            Quantity.VOLTAGE, ELEMENT, original.value, sensor=original.sensor
                        )
                        log.info("Ausgangswert wiederhergestellt: %s", zurueck)
                    except WTError as error:
                        log.error(
                            "RUECKSTELLUNG FEHLGESCHLAGEN: %s - Element %d steht "
                            "moeglicherweise noch auf dem Testwert. Sollwert: %s",
                            error,
                            ELEMENT,
                            original.describe(Quantity.VOLTAGE),
                        )
                        exit_code = 1

                # Die Fehlerqueue deckt den GANZEN Vorgang ab, Rueckstellung
                # eingeschlossen - deshalb steht sie hinter dem finally und nicht
                # darin. Bricht der Nutzteil ab, wird sie nicht mehr erreicht: dann
                # traegt die Ausnahme selbst die Aussage, und ein zusaetzlicher
                # DeviceError wuerde sie nur verdecken.
                session.assert_no_error("Schreibprobe rangeio")

            finally:
                session.disable_remote()

    except WTError as error:
        log.error("Abbruch: %s", error)
        return 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
