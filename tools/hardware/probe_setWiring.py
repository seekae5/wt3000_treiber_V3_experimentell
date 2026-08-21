# =============================================================================
# Datei: tools/hardware/probe_setWiring.py
#
# GERAETESKRIPT. Baut eine echte Verbindung auf und SCHREIBT die Verdrahtung.
#
# Liegt bewusst nicht unter tests/: die Testsuite laeuft ohne Geraet und ohne
# tmctl.dll, und tests/conftest.py setzt das aktiv durch. Aufruf:
#
#     python tools/hardware/probe_setWiring.py
#
# (verlangt ein installiertes Paket - 'pip install -e .' - oder PYTHONPATH=src)
#
# WICHTIG - NICHTS AUS tests/ IMPORTIEREN. tests/conftest.py legt beim Import
# 'TmctlTransport' still; ein einziges 'from tests.conftest import ...' laesst
# dieses Skript deshalb mit
#     RuntimeError: TmctlTransport() aus der Testsuite heraus
# abbrechen. Genau das stand hier: 'from tests.conftest import access' hatte
# den lokalen Namen 'access' gegen die gleichnamige pytest-Fixture in
# tests/conftest.py aufgeloest (dieselbe Ursache, die in
# probe_current_range.py dokumentiert ist).
#
# ANDERES SCHLOSS ALS DIE BEREICHSPROBEN: RangeAccess (wt3000_rangeio.py)
# fasst WIRing bewusst nicht an - siehe Modulkopf dort ("NICHT angetastet
# werden ... WIRing"). Die Verdrahtung liegt in InputConfig
# (wt3000_input.py) und ist zusaetzlich zu allow_changes ueber die Gruppe
# GROUP_WIRING gesperrt (Default-Schutz, siehe DEFAULT_PROTECTED). Freigabe
# nur befristet ueber den Kontextmanager unlocked(). GROUP_CFACTOR wird mit
# freigegeben, weil das Anwendungshandbuch Verdrahtung und Crest-Faktor als
# zusammengehoerendes Paar dokumentiert (docs/ANWENDUNGSHANDBUCH.md, "Ver-
# drahtung und Crest-Faktor") - dieses Skript setzt den Crest-Faktor selbst
# nicht an, gibt die Gruppe aber im selben Atemzug frei wie das Handbuch.
#
# InputConfig.set_wiring() liest im Gegensatz zu RangeAccess.set_range()
# SELBST zurueck und prueft die Fehlerqueue (wt3000_input._write_scalar) -
# ein Abweichen wirft VerificationError, bevor die Methode zurueckkehrt. Das
# Urteil "uebernommen/nicht uebernommen" faellt hier also bereits in der
# Bibliothek; dieses Skript protokolliert das Ergebnis zusaetzlich in
# Klartext, statt es nur an den Rueckgabewert von main() zu delegieren.
#
# Sicherheitsmassnahmen (Vorbild: probe_voltage_range.py):
#   - Ausgangsverdrahtung wird vor dem Schreiben gelesen und im 'finally'
#     wieder gesetzt - also auch bei einer Ausnahme beim Ruecklesen und bei
#     Strg+C.
#   - Die Gruppensperre wird nur fuer die Dauer des jeweiligen Schreibaufrufs
#     freigegeben (with ... unlocked(...):), nicht fuer das ganze Skript.
#   - Scheitert die Rueckstellung selbst, nennt die Fehlermeldung die
#     Verdrahtung, die am Geraet von Hand einzustellen ist.
#
# REMOTE steht als Modulkonstante USE_REMOTE im Skript, nicht in der
# Konfiguration. Begruendung an der Konstante selbst (siehe
# probe_voltage_range.py).
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
from wt3000_scpi.wt3000_input import GROUP_CFACTOR, GROUP_WIRING, InputConfig, Wiring

# ---------------------------------------------------------------------------
# Laufparameter
# ---------------------------------------------------------------------------

#: Verdrahtungsmuster fuer die Probe, in Elementreihenfolge. V3A3 allein
# belegt SigmaA = Elemente 1-3 (3P3W/3V3A) und laesst Element 4 unberuehrt -
# derselbe Aufbau, den der urspruengliche Entwurf dieses Skripts vorsah.
TEST_WIRING: tuple[Wiring, ...] = (Wiring.V3A3,)

#: Fernsteuerung waehrend der Probe. Bewusst NICHT aus 'config.use_remote' -
# Begruendung siehe probe_voltage_range.py.
USE_REMOTE: bool = True

# Ablage an der Projektwurzel statt an 'Path.cwd()' - siehe
# wt3000_common.output_dir().
OUTPUT_DIR: Path = output_dir("konfiguration")


def main() -> int:
    """Verdrahtung setzen und zuruecklesen. Rueckgabe: 0 = ok."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = OUTPUT_DIR / f"wt3000_probe_set_wiring_{timestamp}.txt"

    setup_logging(log_file)
    log = logging.getLogger("wt3000.probe_set_wiring")
    log.info("Protokolldatei: %s", log_file)

    exit_code = 0

    try:
        log.info("Konfigurationsdatei: %s", config_file_in_use() or "<keine, Voreinstellungen>")
        config = WTConfig.from_environment()
        log.info("Verbindung: %s", config.describe())

        with TmctlTransport(config) as transport:
            session = WTSession(transport, config, read_only=False)
            input_cfg = InputConfig(session, allow_changes=True)

            if USE_REMOTE:
                session.enable_remote()
            log.info(
                "Fernsteuerung: %s (Modulkonstante, nicht aus der Konfiguration)",
                "ON" if USE_REMOTE else "OFF",
            )

            try:
                original = input_cfg.get_wiring()
                log.info("Ausgangsverdrahtung: %s", ",".join(original))

                # try/finally um den Schreibteil, wie in probe_voltage_range.py:
                # eine Ausnahme zwischen dem Setzen des Testwerts und der
                # Rueckstellung darf die Verdrahtung nicht auf dem Testwert
                # stehen lassen.
                try:
                    gesendet = ",".join(p.value for p in TEST_WIRING)
                    with input_cfg.unlocked(GROUP_WIRING, GROUP_CFACTOR):
                        input_cfg.set_wiring(TEST_WIRING)
                    log.info("Gesendet: :INPut:WIRing %s", gesendet)

                    readback = input_cfg.get_wiring()
                    log.info("Zurueckgelesen: %s", ",".join(readback))

                    # set_wiring() hat bereits selbst verglichen und wirft bei
                    # Abweichung VerificationError (siehe Modulkopf) - dieser
                    # Codepfad wird also nur erreicht, wenn das Geraet den Wert
                    # tatsaechlich uebernommen hat. Das Protokoll haelt den
                    # Beleg trotzdem in Klartext fest, statt ihn nur an den
                    # Rueckgabewert von main() zu delegieren.
                    log.info(
                        "BELEG: Verdrahtung uebernommen - '%s' ist gueltige Syntax",
                        gesendet,
                    )

                finally:
                    # Auch bei Strg+C zwischen Schreiben und Ruecklesen. Ein
                    # Fehlschlag HIER wird protokolliert und nicht geworfen: sonst
                    # verdraengte er die urspruengliche Ausnahme. Die Meldung
                    # nennt die Verdrahtung, die jemand am Geraet von Hand
                    # zuruecksetzen muss - das ist die wichtigste Zeile, wenn es
                    # schiefgeht.
                    try:
                        with input_cfg.unlocked(GROUP_WIRING, GROUP_CFACTOR):
                            input_cfg.set_wiring(original)
                        log.info(
                            "Ausgangsverdrahtung wiederhergestellt: %s", ",".join(original)
                        )
                    except WTError as error:
                        log.error(
                            "RUECKSTELLUNG FEHLGESCHLAGEN: %s - Verdrahtung steht "
                            "moeglicherweise noch auf dem Testwert. Sollwert: %s",
                            error,
                            ",".join(original),
                        )
                        exit_code = 1

                # Die Fehlerqueue deckt den GANZEN Vorgang ab, Rueckstellung
                # eingeschlossen - deshalb steht sie hinter dem finally und nicht
                # darin. Bricht der Nutzteil ab, wird sie nicht mehr erreicht: dann
                # traegt die Ausnahme selbst die Aussage.
                session.assert_no_error("Schreibprobe Verdrahtung")

            finally:
                session.disable_remote()

    except WTError as error:
        log.error("Abbruch: %s", error)
        return 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

