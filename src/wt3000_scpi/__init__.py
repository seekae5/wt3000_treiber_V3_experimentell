# =============================================================================
# Datei: src/wt3000_scpi/__init__.py
# NEU (Punkt 4, src-Layout): Paketwurzel des WT3000-Treibers.
#
# Hintergrund (ANALYSE.md 2.1 / Fundstellen Abschnitt 5): Unter 'Build/' lag
# eine vollstaendige Zweitkopie von 9 der 14 Module, die sich von der Wurzel nur
# durch relative Importe unterschied und die neuere Haelfte des Projekts
# (wt3000_common, wt3000_rangeio, wt3000_ranging, stage5b) gar nicht enthielt.
# Statt zwei Staende zu pflegen, ist jetzt die Wurzel selbst das Paket. Der
# Klon unter 'Build/' ist damit ersatzlos zu loeschen - er kann aus diesem
# Projektbestand heraus nicht geloescht werden, weil er hier nicht vorliegt.
#
# SCHICHTUNG (Importrichtung ausnahmslos nach unten, azyklisch):
#   UEBERARBEITET (ROADMAP M1-2): Layer 0 ist ein eigenes Modul geworden.
#   Layer 0    wt3000_transport Protocol 'Transport', TmctlTransport,
#                               FakeTransport, WTConfig - importiert nichts
#                               aus dem Paket
#   Layer 1    wt3000_core      Sitzung (WTSession), Fehlerklassen - kennt kein
#                               einziges WT3000-Kommando
#   Layer 1    wt3000_common    geraeteunabhaengige Querschnittsregeln
#   Layer 2    wt3000_numeric   ':NUMeric'-Knoten und Messwertbloecke
#              wt3000_rangeio   ':INPut'-Bereichsknoten
#              wt3000_input     uebrige ':INPut'-Stellgroessen
#   Layer 3    wt3000_itemspec  Ablauf um die Item-Tabelle
#              wt3000_ranging   Ablauf um die Messbereiche
#              wt3000_measure   Messschleife und CSV
#   Layer 4    stage2..stage5b  ausfuehrbare Stufenskripte
#
# Aufruf der Stufenskripte nach der Umstellung:
#     python -m wt3000_scpi.stage2_read_numeric
#     python -m wt3000_scpi.stage5b_range_probe
#
# Dieses Modul importiert BEWUSST nichts aus wt3000_core: der Transport laedt
# 'tmctl.dll' erst bei Instanziierung, aber schon der Modulimport soll auf
# einem Rechner ohne Geraet nichts voraussetzen. Wer die Fachmodule braucht,
# importiert sie einzeln:
#     from wt3000_scpi.wt3000_ranging import RangePlan, RangeSpec
# =============================================================================

from __future__ import annotations

__all__ = ["__version__", "MODULES"]

__version__ = "0.3.0"

# Die Fachmodule des Pakets, in Schichtreihenfolge. Dient der Dokumentation und
# dem Importtest in tests/test_package_layout.py.
MODULES: tuple[str, ...] = (
    # NEU (M1-2): Layer 0.
    "wt3000_transport",
    "wt3000_core",
    "wt3000_common",
    "wt3000_numeric",
    "wt3000_rangeio",
    "wt3000_input",
    "wt3000_itemspec",
    "wt3000_ranging",
    "wt3000_measure",
)
