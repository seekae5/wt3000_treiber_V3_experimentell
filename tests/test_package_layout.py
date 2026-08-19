# =============================================================================
# Datei: tests/test_package_layout.py
# NEU (Punkt 4, src-Layout): haelt fest, was die Umstellung garantieren soll.
#
# Der Klon unter 'Build/' entstand, weil das Packaging-Skelett und die
# Arbeitskopie getrennt gepflegt wurden. Diese Tests sichern die Eigenschaften
# ab, die dabei auseinandergelaufen sind: dass alle Module importierbar sind,
# dass kein Modul mehr absolut auf ein Geschwistermodul zugreift, und dass die
# Importrichtung nach unten zeigt.
# =============================================================================

from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest

import wt3000_scpi

PACKAGE_DIR = Path(wt3000_scpi.__file__).parent

# Erlaubte Importe je Modul - die Schichtung aus dem Kopf von __init__.py.
LAYERS: dict[str, set[str]] = {
    # NEU (ROADMAP M1-2): 'wt3000_transport' ist die neue unterste Schicht und
    # darf aus dem Paket gar nichts importieren - sonst zeigt Layer 0 nach oben
    # und der Zweck des Protocols (geraetefreie Testbarkeit) ist dahin.
    "wt3000_transport": set(),
    # UEBERARBEITET (M1-2): war set(), solange der Transport hier drinlag.
    "wt3000_core": {"wt3000_transport"},
    "wt3000_common": {"wt3000_core"},
    "wt3000_numeric": {"wt3000_core"},
    "wt3000_rangeio": {"wt3000_core", "wt3000_common"},
    "wt3000_input": {"wt3000_core", "wt3000_common"},
    "wt3000_itemspec": {"wt3000_core", "wt3000_common", "wt3000_numeric"},
    "wt3000_ranging": {"wt3000_core", "wt3000_common", "wt3000_rangeio"},
    "wt3000_measure": {
        "wt3000_core",
        "wt3000_common",
        "wt3000_numeric",
        "wt3000_itemspec",
    },
    # NEU (ROADMAP M1-1): die Fassade ist Layer 4 und darf deshalb aus allen
    # Schichten darunter importieren - aber aus keinem Stufenskript und aus
    # keinem zweiten Layer-4-Modul. Genau das haelt dieser Eintrag fest: die
    # Fassade buendelt die Fachmodule, sie ergaenzt sie nicht um eigene
    # Geraetekenntnis.
    "wt3000_device": {
        "wt3000_transport",
        "wt3000_core",
        "wt3000_common",
        "wt3000_numeric",
        "wt3000_rangeio",
        "wt3000_input",
        "wt3000_itemspec",
        "wt3000_ranging",
        "wt3000_measure",
    },
}


def modul_dateien() -> list[Path]:
    return sorted(p for p in PACKAGE_DIR.glob("*.py") if p.name != "__init__.py")


@pytest.mark.parametrize("name", wt3000_scpi.MODULES)
def test_jedes_fachmodul_ist_importierbar(name):
    """Importieren darf keine tmctl.dll und kein Geraet voraussetzen."""
    importlib.import_module(f"wt3000_scpi.{name}")


@pytest.mark.parametrize("pfad", modul_dateien(), ids=lambda p: p.stem)
def test_kein_absoluter_geschwisterimport(pfad):
    """Genau der Unterschied, der Wurzel und Build/-Klon getrennt hat."""
    baum = ast.parse(pfad.read_text(encoding="utf-8"))
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.ImportFrom) and knoten.level == 0:
            assert not (knoten.module or "").startswith("wt3000_"), (
                f"{pfad.name}: 'from {knoten.module} import ...' muss relativ sein"
            )
        if isinstance(knoten, ast.Import):
            for alias in knoten.names:
                assert not alias.name.startswith("wt3000_"), (
                    f"{pfad.name}: 'import {alias.name}' muss relativ sein"
                )


@pytest.mark.parametrize("name", sorted(LAYERS))
def test_importrichtung_zeigt_nach_unten(name):
    quelle = (PACKAGE_DIR / f"{name}.py").read_text(encoding="utf-8")
    genutzt = {
        knoten.module
        for knoten in ast.walk(ast.parse(quelle))
        if isinstance(knoten, ast.ImportFrom)
        and knoten.level == 1
        and knoten.module is not None
    }
    unerlaubt = genutzt - LAYERS[name]
    assert not unerlaubt, f"{name} importiert aus einer hoeheren Schicht: {unerlaubt}"


def test_stufenskripte_fuehren_beim_import_nichts_aus():
    """Layer 4 darf erst ueber main() aktiv werden, nicht beim Import."""
    for name in ("stage2_read_numeric", "stage3_own_itemtable", "stage4_measure",
                 "stage5_input_config", "stage5b_range_probe"):
        modul = importlib.import_module(f"wt3000_scpi.{name}")
        assert callable(modul.main)


# ---------------------------------------------------------------------------
# Die Suite bleibt geraetefrei
# ---------------------------------------------------------------------------


def test_testsuite_kann_keine_geraeteverbindung_oeffnen():
    """Belegt die Sperre aus tests/conftest.py.

    Der Kopf von conftest.py sagt zu, dass die Suite ohne Geraet und ohne
    tmctl.dll laeuft. Diese Zusage war lange nur Absicht: unter tests/ lag ein
    Skript, das eine echte Verbindung aufbaute und einen Messbereich schrieb.
    Seit es nach tools/hardware/ umgezogen ist, sichert conftest.py die Zusage
    aktiv ab - dieser Test haelt fest, dass die Sperre auch wirklich greift.
    """
    from wt3000_scpi.wt3000_transport import TmctlTransport, WTConfig

    with pytest.raises(RuntimeError, match="ohne Geraet"):
        TmctlTransport(WTConfig())


def test_die_sperre_laesst_den_protokollvertrag_unberuehrt():
    """Der stillgelegte Konstruktor darf die Typpruefung nicht beschaedigen.

    'issubclass(TmctlTransport, Transport)' in test_fake_transport.py haengt an
    write/read/query/set_timeout/close - nicht am Konstruktor.
    """
    from wt3000_scpi.wt3000_transport import TmctlTransport, Transport

    assert issubclass(TmctlTransport, Transport)
