# =============================================================================
# Datei: tests/conftest.py
# NEU (Punkt 3, TOOLS-1/TOOLS-2): gemeinsame Bausteine der Testsuite.
#
# Die gesamte Suite laeuft OHNE Geraet und ohne tmctl.dll. Wo ein Objekt eine
# WTSession erwartet, tritt FakeSession an ihre Stelle: sie beantwortet Queries
# aus einer Tabelle und merkt sich alles Geschriebene. Damit sind auch die
# Klassen pruefbar, die eine Sitzung nur als Datenquelle benutzen
# (RangeAccess, RangePlan.validate).
# =============================================================================

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ohne Installation lauffaehig: src/ in den Suchpfad legen. Nach
# 'pip install -e .' ist die Zeile wirkungslos, aber nicht schaedlich.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


class FakeSession:
    """Minimalersatz fuer WTSession - beantwortet Queries aus einer Tabelle.

    responses: Abbildung Kommando (ohne '?') -> Antwort. Der Zugriff ist
    unabhaengig von Gross-/Kleinschreibung. Fehlt ein Eintrag, wird ein
    KeyError geworfen statt still etwas zu erfinden: ein Test, der eine nicht
    hinterlegte Abfrage ausloest, soll auffallen.
    """

    def __init__(self, responses: dict[str, str] | None = None) -> None:
        self.responses = {k.upper(): v for k, v in (responses or {}).items()}
        self.written: list[str] = []

    def query(self, command: str) -> str:
        key = command.strip().rstrip("?").upper()
        if key not in self.responses:
            raise KeyError(f"FakeSession hat keine Antwort fuer {command!r}")
        return self.responses[key]

    def write(self, command: str) -> None:
        self.written.append(command)

    def read_error_queue(self) -> list[str]:
        return []

    def assert_no_error(self, context: str = "") -> None:
        return None


# Bereichsantworten des vorliegenden Aufbaus: Elemente 1-3 haengen an externen
# Stromsensoren (10 V), Element 4 direkt (5 A). Genau die Konstellation, an der
# RangeBackup.capture() vor der Korrektur zu RANGEIO-2 abgebrochen ist.
SENSOR_ELEMENTS: tuple[int, ...] = (1, 2, 3)


def range_responses() -> dict[str, str]:
    """Antworttabelle fuer die Bereichsknoten aller vier Elemente."""
    table = {
        ":INPUT:WIRING": "V3A3,P1W2",
        ":INPUT:MODULE": "30,30,30,30",
        ":INPUT:INDEPENDENT": "1",
    }
    for element in (1, 2, 3, 4):
        table[f":INPUT:VOLTAGE:RANGE:ELEMENT{element}"] = "1.000E+03"
        table[f":INPUT:VOLTAGE:AUTO:ELEMENT{element}"] = "0"
        table[f":INPUT:CURRENT:AUTO:ELEMENT{element}"] = "0"
        table[f":INPUT:CURRENT:RANGE:ELEMENT{element}"] = (
            "EXTERNAL,10.00E+00" if element in SENSOR_ELEMENTS else "5.00E+00"
        )
    return table


@pytest.fixture
def fake_session() -> FakeSession:
    """Sitzung mit vollstaendiger Bereichs-Antworttabelle."""
    return FakeSession(range_responses())


@pytest.fixture
def access(fake_session: FakeSession):
    """Schreibfaehiger RangeAccess auf der FakeSession, Wiring V3A3,P1W2."""
    from wt3000_scpi.wt3000_rangeio import RangeAccess

    return RangeAccess(
        fake_session,
        allow_changes=True,
        sigma_members={"SIGMA": (1, 2, 3), "SIGMB": (4,)},
    )


def element_settings(**overrides):
    """ElementSettings des Aufbaus, einzelne Felder ueberschreibbar."""
    from wt3000_scpi.wt3000_input import ElementSettings

    base = dict(
        element=1,
        module=30,
        voltage_range=1000.0,
        voltage_auto=False,
        voltage_mode="RMS",
        current_direct=None,
        current_sensor=10.0,
        current_auto=False,
        current_mode="RMS",
        sensor_ratio=1.0,
        line_filter="OFF",
        frequency_filter=False,
        scaling=False,
        vt_ratio=1.0,
        ct_ratio=1.0,
        power_factor=1.0,
        sync_source="EXTERNAL",
    )
    base.update(overrides)
    return ElementSettings(**base)


def input_snapshot(*elements, **overrides):
    """InputSnapshot mit den uebergebenen Elementen."""
    from wt3000_scpi.wt3000_input import InputSnapshot

    base = dict(
        crest_factor=3,
        wiring=("V3A3", "P1W2"),
        independent=True,
        update_rate_s=1.0,
        elements=tuple(elements) or (element_settings(),),
        raw_dump="",
    )
    base.update(overrides)
    return InputSnapshot(**base)
