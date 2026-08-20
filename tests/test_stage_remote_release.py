# =============================================================================
# Datei: tests/test_stage_remote_release.py
# NEU (Schritt 1 aus MarkDowns/PLAN_AUFRUFKETTE.md, Befund A-01): Stufe 3 und
# Stufe 4 geben das Bedienfeld frei, egal wie der Lauf ausgegangen ist.
#
# Der Befund A-01: in beiden Skripten stand 'session.disable_remote()' als
# letzte Anweisung IM RUMPF des 'finally', hinter dem try/except, das die
# Wiederherstellung klammert - und dieses except fing nur 'WTError'. Verliess
# eine andere Ausnahme die Wiederherstellung, wurde 'disable_remote()'
# uebersprungen. Sie lief dann aus dem 'with TmctlTransport(...)' heraus, der
# Transport wurde geschlossen, und ':COMMunicate:REMote OFF' war danach nicht
# mehr moeglich: das Bedienfeld blieb gesperrt, der Anwender musste am Geraet
# LOCAL druecken.
#
# Stufe 2 hatte die richtige Fassung bereits (F-07, eigenes finally um den
# Nutzteil); dieser Test haelt sie jetzt fuer Stufe 3 und 4 fest. Er ist
# bewusst so formuliert, dass er NICHT prueft, wie der Lauf ausgegangen ist -
# nur, dass REMOTE zurueckgenommen wurde. Genau das ist die Zusage.
#
# Die Vorrichtung unten ist die aus test_stage5b_write_probe.py. Sie gehoert
# nach conftest.py (Schritt 0c des Plans, Befund A-13); bis dahin steht sie
# hier lokal, mit der einen Erweiterung, die Stufe 3 braucht - siehe
# _ausgabeziel_umlenken().
#
# WAS VOR DER REPARATUR ROT WAR - gemessen, nicht angenommen: von den zehn
# Pruefsaetzen dieser Datei schlugen genau ZWEI fehl, naemlich
# test_remote_wird_auch_bei_nicht_wterror_aus_dem_restore_zurueckgenommen fuer
# Stufe 3 und Stufe 4. Das ist der Befund A-01 in seiner reinen Form: die
# Ausnahme kommt aus der WIEDERHERSTELLUNG.
#
# Die uebrigen acht waren bereits gruen, und das aus einem Grund, der die
# Grenze des alten Fehlers genau beschreibt: kam die Ausnahme aus dem NUTZTEIL,
# lief der finally-Rumpf ja durch und erreichte sein 'disable_remote()' am
# Ende. Nur wenn der Restore-Block SELBST mit etwas anderem als WTError
# abbrach, wurde die Zeile uebersprungen. Diese acht sind deshalb keine
# Nachweise der Reparatur, sondern Absicherungen gegen sie: sie halten fest,
# was die neue Klammer NICHT kaputtmachen darf.
# =============================================================================

from __future__ import annotations

import pytest

from wt3000_scpi import stage3_own_itemtable as stage3
from wt3000_scpi import stage4_measure as stage4
from wt3000_scpi.wt3000_core import WTError
from wt3000_scpi.wt3000_itemspec import build_item_table
from wt3000_scpi.wt3000_measure import build_standard_profile
from wt3000_scpi.wt3000_transport import FakeTransport

REMOTE_ON = ":COMMunicate:REMote ON"
REMOTE_OFF = ":COMMunicate:REMote OFF"


# ---------------------------------------------------------------------------
# Antworttabellen
# ---------------------------------------------------------------------------


def itemtabelle_antwort(specs) -> str:
    """Antwort auf ':NUMeric:NORMal?', die genau die Zieltabelle spiegelt.

    Absicht: Die gesicherte Tabelle ist so lang wie die Zieltabelle. Damit
    liefert probe_extra_items() eine leere Liste (first_index > last_index) und
    die Antworttabelle bleibt ohne die 40+ Eintraege fuer ':ITEM<x>?'. Der
    Ablauf, um den es hier geht, beginnt ohnehin erst danach.

    Gebaut aus der Zielliste des Skripts selbst statt aus einer festen
    Zeichenkette: aendert jemand TARGET_ITEMS oder das Standardprofil, bleibt
    dieser Test gueltig, statt an einer Laengenpruefung zu scheitern.
    """
    tabelle = build_item_table(specs)
    return ";".join([str(tabelle.number)] + [item.argument for item in tabelle.items])


def stage3_antworten() -> dict[str, str]:
    """Alles, was Stufe 3 bis zum Schreibversuch abfragt."""
    return {
        ":COMMUNICATE:HEADER": "0",
        ":NUMERIC:FORMAT": "FLOAT",
        ":INPUT:WIRING": "V3A3,P1W2",
        ":STATUS:CONDITION": "0",
        ":NUMERIC:NORMAL": itemtabelle_antwort(stage3.TARGET_ITEMS),
    }


def stage4_antworten() -> dict[str, str]:
    """Dasselbe fuer Stufe 4 - sie prueft ':RATE?' statt der Verdrahtung."""
    return {
        ":COMMUNICATE:HEADER": "0",
        ":NUMERIC:FORMAT": "FLOAT",
        ":RATE": "1.0",
        ":STATUS:CONDITION": "0",
        ":NUMERIC:NORMAL": itemtabelle_antwort(build_standard_profile()),
    }


# ---------------------------------------------------------------------------
# Vorrichtung
# ---------------------------------------------------------------------------


def _ausgabeziel_umlenken(monkeypatch, modul, tmp_path) -> None:
    """Protokoll und Backup ins tmp-Verzeichnis lenken.

    Hier schlaegt Befund A-10 durch: Stufe 4 hat eine Modulkonstante
    OUTPUT_DIR, Stufe 3 ruft output_dir() innerhalb von main() auf. Es sind
    also zwei verschiedene Namen zu ersetzen. Ohne diese Umlenkung schriebe
    Stufe 3 ihr Backup-JSON in die Projektwurzel - der Testlauf hinterliesse
    Dateien im Arbeitsbaum.

    Schritt 0b des Plans vereinheitlicht das auf die Konstante; diese Funktion
    faellt dann auf die eine Zeile zusammen, die test_stage5b_write_probe.py
    schon hat.
    """
    if hasattr(modul, "OUTPUT_DIR"):
        monkeypatch.setattr(modul, "OUTPUT_DIR", tmp_path)
    else:
        monkeypatch.setattr(modul, "output_dir", lambda *_a, **_k: tmp_path)


@pytest.fixture
def stufenlauf(monkeypatch, tmp_path):
    """main() eines Stufenskripts gegen FakeTransport fahren."""

    def _vorbereiten(modul, responses: dict[str, str]) -> FakeTransport:
        # use_remote ausdruecklich ueber die Umgebung setzen, nicht der
        # 'wt3000.json' der Projektwurzel ueberlassen: stuende dort einmal
        # 'use_remote: false', ginge gar kein REMOTE hinaus und dieser Test
        # waere still bedeutungslos, statt rot zu werden. Die Umgebung hat in
        # der Aufloesungskette Vorrang vor der Datei.
        monkeypatch.setenv("WT3000_IP", "10.0.0.5")
        monkeypatch.setenv("WT3000_USE_REMOTE", "1")

        transport = FakeTransport(responses)
        monkeypatch.setattr(modul, "TmctlTransport", lambda _config: transport)
        # setup_logging() setzt die Handler des Root-Loggers neu und raeumte
        # damit mitten im Lauf pytests Log-Mitschnitt ab - dieselbe Begruendung
        # wie in test_stage5b_write_probe.py.
        monkeypatch.setattr(modul, "setup_logging", lambda _pfad: None)
        _ausgabeziel_umlenken(monkeypatch, modul, tmp_path)
        return transport

    return _vorbereiten


def _wirft(exception: BaseException):
    """Ersatz fuer einen Layer-3-Schritt, der ausschliesslich scheitert."""

    def _ersatz(*_args, **_kwargs):
        raise exception

    return _ersatz


STUFEN = [
    pytest.param(stage3, stage3_antworten, id="stage3"),
    pytest.param(stage4, stage4_antworten, id="stage4"),
]


# ---------------------------------------------------------------------------
# Der Kern von A-01
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("modul, antworten", STUFEN)
def test_remote_wird_auch_bei_nicht_wterror_aus_dem_restore_zurueckgenommen(
    stufenlauf, monkeypatch, modul, antworten
):
    """Reproduktion 7.1 der Analyse, als Pruefsatz.

    Der Nutzteil bricht mit WTError ab (regulaerer Weg, wird gefangen), die
    Wiederherstellung im finally dann mit einem KeyError - also mit etwas, das
    'except WTError' nicht faengt. Vor der Reparatur endete main() an dieser
    Stelle, ohne REMote OFF gesendet zu haben.
    """
    transport = stufenlauf(modul, antworten())
    monkeypatch.setattr(modul, "probe_item_write_capability", _wirft(WTError("Abbruch")))
    monkeypatch.setattr(modul, "restore_item_table", _wirft(KeyError("Nicht-WTError")))

    with pytest.raises(KeyError):
        modul.main()

    assert REMOTE_ON in transport.written, "Vorbedingung: REMOTE war ueberhaupt eingeschaltet"
    assert REMOTE_OFF in transport.written, (
        "Das Bedienfeld bleibt gesperrt zurueck - disable_remote() gehoert in ein "
        "eigenes finally, nicht hinter das try/except der Wiederherstellung"
    )


@pytest.mark.parametrize("modul, antworten", STUFEN)
def test_remote_wird_auch_bei_strg_c_zurueckgenommen(stufenlauf, monkeypatch, modul, antworten):
    """KeyboardInterrupt aus dem Nutzteil - der Fall, der am Geraet vorkommt.

    ABSICHERUNG, kein Nachweis: dieser Pruefsatz war auch vor der Reparatur
    gruen (siehe Dateikopf). Er steht hier, weil KeyboardInterrupt von
    BaseException erbt und nicht von Exception - eine spaetere Umarbeitung, die
    die Klammer durch ein 'except Exception' ersetzt, wuerde ihn rot faerben.
    Genau davor soll er schuetzen.
    """
    transport = stufenlauf(modul, antworten())
    monkeypatch.setattr(modul, "probe_item_write_capability", _wirft(KeyboardInterrupt()))

    with pytest.raises(KeyboardInterrupt):
        modul.main()

    assert REMOTE_OFF in transport.written


@pytest.mark.parametrize("modul, antworten", STUFEN)
def test_remote_wird_vor_dem_sichern_des_backups_zurueckgenommen(
    stufenlauf, monkeypatch, modul, antworten
):
    """Abbruch, bevor 'backup' ueberhaupt steht.

    ABSICHERUNG, kein Nachweis: auch dieser Pruefsatz war vor der Reparatur
    gruen. Bricht der Lauf schon in check_preconditions() ab, ist 'backup' noch
    None, der Wiederherstellungszweig wird uebersprungen - und die alte Fassung
    erreichte ihr 'disable_remote()' am Ende des finally-Rumpfes deshalb noch.

    Er gehoert trotzdem dazu: er deckt den Pfad ab, auf dem gar kein Restore
    stattfindet, und haelt fest, dass die neue Klammer auch dann greift. Das
    ist die Zusage, die von der Frage unabhaengig sein soll, wie weit der Lauf
    gekommen ist.
    """
    transport = stufenlauf(modul, antworten())
    monkeypatch.setattr(modul, "check_preconditions", _wirft(KeyError("Nicht-WTError")))

    with pytest.raises(KeyError):
        modul.main()

    assert REMOTE_OFF in transport.written


# ---------------------------------------------------------------------------
# Gegenprobe: der glatte Weg darf sich nicht veraendert haben
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("modul, antworten", STUFEN)
def test_regulaerer_wterror_gibt_weiterhin_rueckgabewert_1(
    stufenlauf, monkeypatch, modul, antworten
):
    """Ein WTError bleibt gefangen und wird zum Rueckgabewert - wie bisher.

    Ohne diesen Pruefsatz koennte die Reparatur den except-Zweig unbemerkt
    umgehen und jeden Fehler zur Ausnahme machen. Geprueft wird beides: der
    Rueckgabewert und dass REMOTE trotzdem zurueckgenommen wurde.
    """
    transport = stufenlauf(modul, antworten())
    monkeypatch.setattr(modul, "probe_item_write_capability", _wirft(WTError("Abbruch")))
    monkeypatch.setattr(modul, "restore_item_table", lambda *_a, **_k: 0)
    monkeypatch.setattr(modul, "verify_item_table", lambda *_a, **_k: [])

    assert modul.main() == 1
    assert REMOTE_OFF in transport.written


@pytest.mark.parametrize("modul, antworten", STUFEN)
def test_disable_remote_wird_genau_einmal_gesendet(stufenlauf, monkeypatch, modul, antworten):
    """Die Klammer darf sich nicht mit einem zweiten finally ueberlappen.

    'disable_remote()' ist zwar idempotent (WTSession._remote_active), aber ein
    doppelter Aufruf waere ein Hinweis darauf, dass die Reparatur eine zweite
    Klammer eingezogen hat statt die vorhandene zu verschieben.
    """
    transport = stufenlauf(modul, antworten())
    monkeypatch.setattr(modul, "probe_item_write_capability", _wirft(WTError("Abbruch")))
    monkeypatch.setattr(modul, "restore_item_table", lambda *_a, **_k: 0)
    monkeypatch.setattr(modul, "verify_item_table", lambda *_a, **_k: [])

    modul.main()

    assert transport.written.count(REMOTE_OFF) == 1
