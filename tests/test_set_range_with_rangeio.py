# =============================================================================
# Datei: test_set_range_with_rangeio_and_rangeprobe.py
# Layer 4 - Testskript zu ROADMAP.md, Punkt M0-1.
#
# Zweck: EINEN Wert ueber RangeAccess.set_range() (wt3000_rangeio.py) an ein
# unkritisches Element senden und zuruecklesen. Klaert die Vorfrage aus B-01
# (wt3000_rangeio sendet reine NRf-Form wie '1000', wt3000_input haengt eine
# Einheit an wie '1000V') noch nicht abschliessend - dafuer muessten mehrere
# Formen nacheinander probiert werden (siehe stage5b_range_probe.py als
# Vorbild). Dieses Skript ist bewusst der einfache erste Schritt: EIN Wert,
# EIN Element, mit Sicherung und Rueckstellung.
#
# Sicherheitsmassnahmen wie in stage5b_range_probe.py:
#   - Element 4 (Direkteingang, unkritisch fuer diesen Test)
#   - Ausgangswert wird vor dem Schreiben gelesen und danach zurueckgesetzt
#   - Fehlerqueue wird am Ende geprueft
# =============================================================================

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from wt3000_scpi.wt3000_common import setup_logging
from wt3000_scpi.wt3000_core import TmctlTransport, WTConfig, WTError, WTSession
from wt3000_scpi.wt3000_rangeio import Quantity, RangeAccess

# ---------------------------------------------------------------------------
# Laufparameter
# ---------------------------------------------------------------------------

ELEMENT: int = 4
TEST_VALUE: float = 1000.0

OUTPUT_DIR: Path = Path.cwd() / "konfiguration"


def main() -> int:
    """Einen Wert per rangeio setzen und zuruecklesen. Rueckgabe: 0 = ok."""
    config = WTConfig()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = OUTPUT_DIR / f"wt3000_test_set_range_{timestamp}.txt"

    setup_logging(log_file)
    log = logging.getLogger("wt3000.test_set_range")
    log.info("Protokolldatei: %s", log_file)

    try:
        with TmctlTransport(config) as transport:
            session = WTSession(transport, config, read_only=False)
            access = RangeAccess(session, allow_changes=True)

            original = access.get_range(Quantity.VOLTAGE, ELEMENT)
            log.info("Ausgangswert Element %d: %s", ELEMENT, original.describe(Quantity.VOLTAGE))

            command = access.set_range(Quantity.VOLTAGE, ELEMENT, TEST_VALUE)
            log.info("Gesendet: %s", command)

            readback = access.get_range(Quantity.VOLTAGE, ELEMENT)
            log.info("Zurueckgelesen: %s", readback.describe(Quantity.VOLTAGE))

            # Ausgangswert wiederherstellen, bevor die Fehlerqueue geprueft wird.
            access.set_range(Quantity.VOLTAGE, ELEMENT, original.value, sensor=original.sensor)
            session.assert_no_error("Testschreibprobe rangeio")

    except WTError as error:
        log.error("Abbruch: %s", error)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
