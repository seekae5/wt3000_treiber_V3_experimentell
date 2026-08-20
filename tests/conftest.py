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

import importlib.util
import logging
import sys
from pathlib import Path

import pytest

# Ohne Installation lauffaehig: src/ in den Suchpfad legen. Nach
# 'pip install -e .' ist die Zeile wirkungslos, aber nicht schaedlich.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


# ---------------------------------------------------------------------------
# Sicherung: kein Geraetezugriff aus der Testsuite
# ---------------------------------------------------------------------------
#
# Die Zusage im Kopf dieser Datei war bisher nur eine Absichtserklaerung. Eine
# Zeit lang lag unter tests/ ein Skript, das eine echte TMCTL-Verbindung
# aufbaute und einen Messbereich schrieb (heute tools/hardware/). Es enthielt
# keine Testfunktion und blieb deshalb folgenlos - eine spaeter ergaenzte
# Testfunktion oder ein Aufruf auf Modulebene haette pytest aber unbemerkt an
# das eingemessene Geraet schreiben lassen.
#
# 'TmctlTransport' ist das einzige Tor, durch das eine echte Verbindung
# entsteht: WT3000.connect() und WT3000.from_config() gehen ebenfalls
# hindurch. Der Konstruktor wird deshalb hier stillgelegt.
#
# Bewusst auf MODULEBENE und nicht als Fixture: conftest.py wird vor dem
# Einsammeln der Testmodule importiert. Nur so greift die Sperre auch bei einem
# Geraeteaufruf auf Modulebene, der schon beim Import liefe - also genau in dem
# Fall, den eine Fixture zu spaet erwischen wuerde.
#
# Nicht betroffen: 'issubclass(TmctlTransport, Transport)' in
# test_fake_transport.py - der Protokollvertrag haengt an write/read/query/
# set_timeout/close, nicht am Konstruktor. Ebenso das monkeypatch auf
# wt3000_device.TmctlTransport in test_device_facade.py: dort wird der Name
# ersetzt, der echte Konstruktor also gar nicht erreicht.
from wt3000_scpi.wt3000_transport import FakeTransport, TmctlTransport  # noqa: E402


def _kein_geraetezugriff(self, *args, **kwargs):
    # UEBERARBEITET: Die Meldung nannte als einzige Ursache "Skript liegt unter
    # tests/" und schickte damit in die Irre, sobald sie aus einem Skript kam,
    # das laengst unter tools/hardware/ liegt. Ausgeloest wird die Sperre
    # naemlich nicht vom Ablageort, sondern davon, DASS diese Datei importiert
    # wurde - ein einziges 'from tests.conftest import ...' genuegt. Genau das
    # ist bei tools/hardware/probe_current_range.py passiert, durch eine
    # automatische Import-Ergaenzung der Entwicklungsumgebung.
    raise RuntimeError(
        "TmctlTransport() ist stillgelegt, weil tests/conftest.py importiert "
        "wurde: die Testsuite laeuft ohne Geraet und ohne tmctl.dll.\n"
        "  - In Tests: 'FakeTransport' benutzen "
        "(wt3000_scpi.wt3000_transport).\n"
        "  - In einem Geraeteskript unter tools/hardware/: pruefen, ob eine "
        "Zeile 'from tests...' oder 'import conftest' im Modulkopf steht - "
        "meist von der Entwicklungsumgebung automatisch ergaenzt. Aus tests/ "
        "darf ein Geraeteskript NICHTS importieren.\n"
        "  - Ein Skript, das wirklich mit dem Geraet spricht, gehoert nach "
        "tools/hardware/ und nicht unter tests/."
    )


#: Der echte Konstruktor, bevor er stillgelegt wird.
#
# NEU (Schritt 5 aus MarkDowns/PLAN_AUFRUFKETTE.md, Befund A-04): Die
# Fehlerwege IM Konstruktor - fehlende Bitness, fehlende abhaengige DLL,
# Nicht-Windows - sind nur pruefbar, wenn man ihn tatsaechlich betritt. Genau
# EIN Testmodul darf das (test_transport_fehlerpfade.py), und es kommt dabei
# nie bis zu 'TmcInitialize': 'ct.WinDLL' wird vorher ersetzt, sodass der Lauf
# im Ladeteil endet. Eine Verbindung entsteht also auch dort nicht.
ECHTER_TMCTL_KONSTRUKTOR = TmctlTransport.__init__

TmctlTransport.__init__ = _kein_geraetezugriff


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


# ---------------------------------------------------------------------------
# Stufen- und Geraeteskripte vollstaendig durchspielen
# NEU (Schritt 0c aus MarkDowns/PLAN_AUFRUFKETTE.md, Befund A-13)
# ---------------------------------------------------------------------------
#
# Die Vorrichtung stammt aus test_stage5b_write_probe.py. Sie hat dort gezeigt,
# dass ein main() vollstaendig gegen FakeTransport laufen kann - und war damit
# lange der einzige Weg, ein Stufenskript ueberhaupt zu pruefen: von den fuenf
# Stufen war genau eine abgedeckt, und die vier ungeprueften waren die, die
# schreiben.
#
# Sie steht ab hier hier, weil sie inzwischen von drei Testmodulen gebraucht
# wird. Voraussetzung dafuer war Schritt 0b: Stufe 2 und 3 fuehrten
# 'output_dir()' als Aufruf INNERHALB von main() statt als Modulkonstante, und
# damit trug das Rezept fuer sie nicht - es waere ein anderer Name zu ersetzen
# gewesen.


def geraeteskript(name: str):
    """Ein Skript aus tools/hardware/ als Modul laden.

    Die beiden Geraeteskripte sind keine Paketmodule; ohne diesen Umweg sind
    sie aus der Suite heraus nicht erreichbar ('testpaths = ["tests"]', kein
    tools/__init__.py).

    Geladen wird ueber den DATEIPFAD und ausdruecklich NICHT ueber einen
    sys.path-Eintrag. Ein solcher Eintrag waere genau der Weg, ueber den eine
    automatische Import-Ergaenzung der Entwicklungsumgebung einmal
    'from tests.conftest import ...' in probe_current_range.py geschrieben hat -
    was die Sperre oben ausloeste und das Skript am Geraet unbrauchbar machte
    (siehe dessen Dateikopf). Hier entsteht kein Importweg, der das kann.

    Jeder Aufruf liefert ein FRISCHES Modulobjekt: die Tests setzen darin
    Modulkonstanten um, und ein geteiltes Objekt truege sie weiter.
    """
    pfad = Path(__file__).resolve().parents[1] / "tools" / "hardware" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"geraeteskript_{name}", pfad)
    assert spec is not None and spec.loader is not None, pfad
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


@pytest.fixture
def stufenlauf(monkeypatch, tmp_path):
    """main() eines Stufen- oder Geraeteskripts gegen FakeTransport fahren.

    Drei Ersetzungen im Modulnamensraum - mehr braucht es nicht:

      TmctlTransport   der einzige Weg zu einer echten Verbindung. Ersetzt wird
                       der Name IM MODUL, nicht global: der Konstruktor ist
                       oben stillgelegt, und daran soll sich auch diese
                       Vorrichtung nicht vorbeimogeln.
      OUTPUT_DIR       sonst landen Protokoll, Backup und Messdaten im
                       Arbeitsbaum - jeder Testlauf hinterliesse Dateien.
      setup_logging    setzt die Handler des Root-Loggers neu und raeumte damit
                       mitten im Testlauf pytests Log-Mitschnitt ab; alles nach
                       dem Aufruf fehlte dann in 'caplog.records'. Nachgestellt
                       und bestaetigt. Geprueft wird meist der Ablauf, nicht die
                       Protokolleinrichtung.

    'logging_stilllegen=False' laesst setup_logging() laufen - gebraucht fuer
    genau die Pruefsaetze, bei denen es auf die REIHENFOLGE ankommt: ob eine
    Meldung vor oder nach der Einrichtung des Protokolls entsteht (Befund
    A-08). Mit stillgelegtem setup_logging waere das nicht pruefbar, weil
    caplog unabhaengig davon mitschneidet - der Pruefsatz waere auch dann gruen,
    wenn die Meldung neben die Protokolldatei fiele. Er muss deshalb die DATEI
    lesen. Die Handler werden danach zurueckgesetzt; ohne das Schliessen des
    FileHandlers bliebe unter Windows ein Handle auf tmp_path offen.

    'use_remote' geht ausdruecklich ueber die Umgebung und nicht ueber die
    'wt3000.json' der Projektwurzel: stuende dort einmal 'use_remote: false',
    liefe ein Test, der die Ruecknahme der Fernsteuerung prueft, still ins
    Leere, statt rot zu werden. Die Umgebung hat in der Aufloesungskette
    Vorrang vor der Datei.
    """
    wurzel = logging.getLogger()
    handler_vorher = list(wurzel.handlers)
    level_vorher = wurzel.level

    def _vorbereiten(
        modul,
        responses: dict,
        *,
        ip: str = "10.0.0.5",
        use_remote: bool = True,
        logging_stilllegen: bool = True,
    ) -> FakeTransport:
        monkeypatch.setenv("WT3000_IP", ip)
        monkeypatch.setenv("WT3000_USE_REMOTE", "1" if use_remote else "0")

        transport = FakeTransport(responses)
        monkeypatch.setattr(modul, "TmctlTransport", lambda _config: transport)
        monkeypatch.setattr(modul, "OUTPUT_DIR", tmp_path)
        if logging_stilllegen:
            monkeypatch.setattr(modul, "setup_logging", lambda _pfad: None)
        return transport

    yield _vorbereiten

    for handler in list(wurzel.handlers):
        if handler not in handler_vorher:
            handler.close()
            wurzel.removeHandler(handler)
    for handler in handler_vorher:
        if handler not in wurzel.handlers:
            wurzel.addHandler(handler)
    wurzel.setLevel(level_vorher)
