# =============================================================================
# Datei: tools/hardware/probe_current_range.py
#
# GERAETESKRIPT. Baut eine echte Verbindung auf und SCHREIBT einen Messbereich.
#
# Gegenstueck zu probe_voltage_range.py, gleicher Aufbau - nur fuer den
# Direktstromeingang statt fuer die Spannung. Liegt bewusst nicht unter tests/:
# die Testsuite laeuft ohne Geraet und ohne tmctl.dll, und tests/conftest.py
# setzt das aktiv durch. Aufruf:
#
#     python tools/hardware/probe_current_range.py
#
# (verlangt ein installiertes Paket - 'pip install -e .' - oder PYTHONPATH=src)
#
# WICHTIG - NICHTS AUS tests/ IMPORTIEREN. tests/conftest.py legt beim Import
# 'TmctlTransport' still; ein einziges 'from tests.conftest import ...' laesst
# dieses Skript deshalb mit
#     RuntimeError: TmctlTransport() aus der Testsuite heraus
# abbrechen, obwohl es an der richtigen Stelle liegt. Genau das ist hier
# einmal passiert: eine automatische Import-Ergaenzung der Entwicklungsumgebung
# hatte den lokalen Namen 'access' (Zeile weiter unten) gegen die
# gleichnamige pytest-Fixture in tests/conftest.py aufgeloest. Die Sperre hat
# also richtig gegriffen - der Import war der Fehler.
#
# Zweck: offener Punkt M0-1 der ROADMAP, dritter Spiegelstrich ("Dasselbe fuer
# den Direktstrom"). Sendet EINEN Wert ueber RangeAccess.set_range()
# (wt3000_rangeio.py) an ein unkritisches Element und liest ihn zurueck.
#
# Sicherheitsmassnahmen wie in probe_voltage_range.py:
#   - Element 4 (Direkteingang, unkritisch fuer diese Probe)
#   - Ausgangswert wird vor dem Schreiben gelesen und danach zurueckgesetzt
#   - Fehlerqueue wird am Ende geprueft
# =============================================================================

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from wt3000_scpi.wt3000_common import output_dir, setup_logging
from wt3000_scpi.wt3000_core import TmctlTransport, WTConfig, WTError, WTSession
from wt3000_scpi.wt3000_rangeio import Quantity, RangeAccess

# ---------------------------------------------------------------------------
# Laufparameter
# ---------------------------------------------------------------------------

ELEMENT: int = 4

#: Strombereich in Ampere.
#
# ZU BEACHTEN: 'RangeAccess.set_range()' prueft NICHT gegen eine
# Bereichstabelle - es formatiert und sendet. Ein Wert, den das Geraet nicht
# als Stufe kennt, geht also hinaus und faellt erst beim Ruecklesen auf.
#
# Gueltige Stufen laut wt3000_input.CURRENT_RANGES:
#   30-A-Element, CF3:  0.5  1.0  2.0  5.0  10.0  20.0  30.0
#   30-A-Element, CF6:  0.25 0.5  1.0  2.5   5.0  10.0  15.0
#    2-A-Element, CF3:  0.005 ... 0.2  0.5  1.0   2.0
#
# 0.5 ist in jeder dieser Tabellen enthalten und trennt damit sauber, worum es
# in M0-1 geht: die PARAMETERSYNTAX. Ein Zwischenwert wie 0.4 wuerde zwei
# Fragen auf einmal stellen - Syntax (M0-1) und Rundungsverhalten (M0-2) - und
# ein abweichender Rueckgabewert liesse sich dann keiner von beiden zuordnen.
TEST_VALUE: float = 0.75

# UEBERARBEITET: Ablage an der Projektwurzel statt an 'Path.cwd()'.
# Bis hierher hing das am Arbeitsverzeichnis - ein Start aus einem
# Unterverzeichnis (Entwicklungsumgebungen tun das standardmaessig) legte
# ein zweites gleichnamiges Verzeichnis dort an. Siehe
# wt3000_common.output_dir().
OUTPUT_DIR: Path = output_dir("konfiguration")


def main() -> int:
    """Einen Wert per rangeio setzen und zuruecklesen. Rueckgabe: 0 = ok."""
    # Verbindungsparameter aus der Auflaesungskette - siehe README.
    config = WTConfig.from_environment()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = OUTPUT_DIR / f"wt3000_probe_current_range_{timestamp}.txt"

    setup_logging(log_file)
    log = logging.getLogger("wt3000.probe_current_range")
    log.info("Protokolldatei: %s", log_file)

    try:
        with TmctlTransport(config) as transport:
            session = WTSession(transport, config, read_only=False)
            access = RangeAccess(session, allow_changes=True)

            original = access.get_range(Quantity.CURRENT, ELEMENT)
            log.info("Ausgangswert Element %d: %s", ELEMENT, original.describe(Quantity.CURRENT))

            command = access.set_range(Quantity.CURRENT, ELEMENT, TEST_VALUE)
            log.info("Gesendet: %s", command)

            readback = access.get_range(Quantity.CURRENT, ELEMENT)
            log.info("Zurueckgelesen: %s", readback.describe(Quantity.CURRENT))

            # Ausgangswert wiederherstellen, bevor die Fehlerqueue geprueft wird.
            access.set_range(Quantity.CURRENT, ELEMENT, original.value, sensor=original.sensor)
            session.assert_no_error("Schreibprobe rangeio current")

    except WTError as error:
        log.error("Abbruch: %s", error)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
