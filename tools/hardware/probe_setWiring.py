from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from tools.hardware.probe_voltage_range import OUTPUT_DIR
from wt3000_scpi import Quantity
from wt3000_scpi.wt3000_common import setup_logging
from wt3000_scpi.wt3000_core import (
    TmctlTransport,
    WTConfig,
    WTError,
    WTSession,
    config_file_in_use,
)
from wt3000_scpi.wt3000_input import Wiring

USE_REMOTE: bool=True

def main () -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp =datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = OUTPUT_DIR / f"wt300_wiring setting_{timestamp}.txt"

    setup_logging(log_file)
    log = logging.getLogger("wt3000.wiring_setting")
    log.info("Protokolldatein: %s", log_file)

    exit_code = 0

    try:

        with TmctlTransport(config) as transport:
            sessopm = WTSession(transport, config, read_only=False)
            access = RangeAccess(session, allow_changes=True)

            if USE_REMOTE:
                session.enable_remote()
            log.info(
                "Fernsteuerung: %s (Modulkonstante, nicht aus der Konfig",
                "ON" if USE_REMOTE else "OFF",
            )

            try:
                orginal = access.get_wiring() #hier muss die klasse korrekt aufgerufen werden