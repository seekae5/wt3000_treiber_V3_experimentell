# =============================================================================
# Datei: tests/test_config_resolution.py
# NEU (P-7, siehe PLAN_BEFUNDE_2026-08-19.md): die Auflaesungskette der
# Verbindungsparameter.
#
# Befund BF-M2: in WTConfig standen eine feste Labor-IP, Benutzername und
# Passwort sowie ein DLL-Pfad aus dem Benutzerverzeichnis eines bestimmten
# Rechners. Auf jedem zweiten Rechner war der Treiber nur durch
# Quelltextaenderung benutzbar.
#
# Geprueft wird die RANGFOLGE - sie ist die eigentliche Zusage:
#   Parameter > Umgebungsvariable > Konfigurationsdatei > Voreinstellung
# =============================================================================

from __future__ import annotations

import json

import pytest

from wt3000_scpi.wt3000_core import WTConfig, WTError
from wt3000_scpi.wt3000_transport import CONFIG_FILE_NAME, resolve_dll_path

ALLE_VARIABLEN = (
    "WT3000_IP",
    "WT3000_DLL_PATH",
    "WT3000_USER",
    "WT3000_PASSWORD",
    "WT3000_TIMEOUT_MS",
    "WT3000_USE_REMOTE",
    "WT3000_CONFIG",
)


@pytest.fixture(autouse=True)
def saubere_umgebung(monkeypatch, tmp_path):
    """Keine WT3000_*-Variable und keine Datei aus der echten Umgebung.

    Ohne das haengt das Ergebnis davon ab, was auf dem Rechner des Pruefenden
    gesetzt ist - genau die Abhaengigkeit, die P-7 beseitigen soll.
    """
    for name in ALLE_VARIABLEN:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.chdir(tmp_path)  # './wt3000.json' zeigt ins Leere
    monkeypatch.setenv("HOME", str(tmp_path))  # '~/wt3000.json' ebenso


def datei_anlegen(tmp_path, **werte) -> None:
    (tmp_path / CONFIG_FILE_NAME).write_text(json.dumps(werte), encoding="utf-8")


# ---------------------------------------------------------------------------
# Die Voreinstellung ist neutral
# ---------------------------------------------------------------------------


def test_voreinstellung_traegt_keine_zugangsdaten():
    """Der Kern von BF-M2: nichts Rechnerspezifisches mehr im Quelltext."""
    config = WTConfig()
    assert config.ip == ""
    assert config.user == ""
    assert config.password == ""
    assert config.dll_path == "tmctl64.dll"  # blosser Name, kein Pfad


def test_ohne_jede_quelle_bleibt_es_bei_der_voreinstellung():
    assert WTConfig.from_environment() == WTConfig()


# ---------------------------------------------------------------------------
# Die einzelnen Stufen
# ---------------------------------------------------------------------------


def test_umgebungsvariable_wird_uebernommen(monkeypatch):
    monkeypatch.setenv("WT3000_IP", "10.0.0.5")
    assert WTConfig.from_environment().ip == "10.0.0.5"


def test_konfigurationsdatei_wird_uebernommen(tmp_path):
    datei_anlegen(tmp_path, ip="192.168.1.7", user="LABOR")
    config = WTConfig.from_environment()
    assert config.ip == "192.168.1.7"
    assert config.user == "LABOR"


def test_parameter_schlaegt_umgebung(monkeypatch):
    monkeypatch.setenv("WT3000_IP", "10.0.0.5")
    assert WTConfig.from_environment(ip="10.0.0.9").ip == "10.0.0.9"


def test_umgebung_schlaegt_datei(monkeypatch, tmp_path):
    datei_anlegen(tmp_path, ip="192.168.1.7")
    monkeypatch.setenv("WT3000_IP", "10.0.0.5")
    assert WTConfig.from_environment().ip == "10.0.0.5"


def test_datei_schlaegt_voreinstellung(tmp_path):
    datei_anlegen(tmp_path, timeout_ms=9000)
    assert WTConfig.from_environment().timeout_ms == 9000


def test_die_stufen_mischen_sich_feldweise(monkeypatch, tmp_path):
    """Jedes Feld wird einzeln aufgeloest, nicht die Konfiguration als Ganzes."""
    datei_anlegen(tmp_path, ip="192.168.1.7", user="LABOR", timeout_ms=9000)
    monkeypatch.setenv("WT3000_USER", "AUS_UMGEBUNG")

    config = WTConfig.from_environment(timeout_ms=1234)
    assert config.ip == "192.168.1.7"          # aus der Datei
    assert config.user == "AUS_UMGEBUNG"       # aus der Umgebung
    assert config.timeout_ms == 1234           # als Parameter
    assert config.drain_timeout_ms == 500      # Voreinstellung


def test_none_als_parameter_zaehlt_nicht_als_angabe(monkeypatch):
    """Damit connect(ip=None) die Umgebung nicht ueberschreibt."""
    monkeypatch.setenv("WT3000_IP", "10.0.0.5")
    assert WTConfig.from_environment(ip=None).ip == "10.0.0.5"


def test_leere_umgebungsvariable_zaehlt_nicht_als_angabe(monkeypatch, tmp_path):
    """WT3000_IP= (leer) soll die Datei nicht verdraengen."""
    datei_anlegen(tmp_path, ip="192.168.1.7")
    monkeypatch.setenv("WT3000_IP", "")
    assert WTConfig.from_environment().ip == "192.168.1.7"


# ---------------------------------------------------------------------------
# Typen und Fehlerfaelle
# ---------------------------------------------------------------------------


def test_zahlen_und_wahrheitswerte_werden_gewandelt(monkeypatch):
    monkeypatch.setenv("WT3000_TIMEOUT_MS", "1500")
    monkeypatch.setenv("WT3000_USE_REMOTE", "off")
    config = WTConfig.from_environment()
    assert config.timeout_ms == 1500 and isinstance(config.timeout_ms, int)
    assert config.use_remote is False


@pytest.mark.parametrize("text,erwartet", [("1", True), ("true", True), ("ja", True),
                                           ("0", False), ("nein", False), ("", None)])
def test_wahrheitswerte_aus_der_umgebung(monkeypatch, text, erwartet):
    monkeypatch.setenv("WT3000_USE_REMOTE", text)
    config = WTConfig.from_environment()
    # Leerer Text zaehlt nicht als Angabe - dann gilt die Voreinstellung True.
    assert config.use_remote is (WTConfig().use_remote if erwartet is None else erwartet)


def test_unbrauchbare_zahl_bricht_verstaendlich_ab(monkeypatch):
    monkeypatch.setenv("WT3000_TIMEOUT_MS", "bald")
    with pytest.raises(WTError, match="timeout_ms"):
        WTConfig.from_environment()


def test_ausdruecklich_benannte_datei_muss_existieren(tmp_path):
    """Ein Tippfehler im Pfad darf nicht still zur Voreinstellung fuehren."""
    with pytest.raises(WTError, match="nicht gefunden"):
        WTConfig.from_environment(config_file=tmp_path / "gibtsnicht.json")


def test_kaputte_datei_bricht_verstaendlich_ab(tmp_path):
    (tmp_path / CONFIG_FILE_NAME).write_text("{kein json", encoding="utf-8")
    with pytest.raises(WTError, match="nicht lesbar"):
        WTConfig.from_environment()


def test_kommentarschluessel_werden_stillschweigend_uebergangen(tmp_path, caplog):
    """JSON kennt keine Kommentare - '_'-Schluessel sind der Ersatz.

    Damit laesst sich 'wt3000.example.json' mit Erklaertext ausliefern, ohne
    dass eine Kopie davon bei jedem Start eine Warnung ausloest.
    """
    datei_anlegen(tmp_path, _hinweis="Vorlage, bitte anpassen", ip="10.0.0.5")
    with caplog.at_level("WARNING"):
        config = WTConfig.from_environment()
    assert config.ip == "10.0.0.5"
    assert not [r for r in caplog.records if "uebergangen" in r.getMessage()]


def test_unbekannte_schluessel_werden_uebergangen_und_gemeldet(tmp_path, caplog):
    datei_anlegen(tmp_path, ip="10.0.0.5", tippfehler="egal")
    with caplog.at_level("WARNING"):
        config = WTConfig.from_environment()
    assert config.ip == "10.0.0.5"
    assert any("tippfehler" in r.getMessage() for r in caplog.records)


# ---------------------------------------------------------------------------
# DLL-Aufloesung
# ---------------------------------------------------------------------------


def test_blosser_dateiname_wird_durchgereicht():
    """Windows sucht dann selbst in PATH - der Weg fuer eine installierte TMCTL."""
    assert resolve_dll_path("tmctl64.dll") == "tmctl64.dll"


def test_vorhandener_pfad_wird_angenommen(tmp_path):
    dll = tmp_path / "tmctl64.dll"
    dll.write_bytes(b"")
    assert resolve_dll_path(str(dll)) == dll


def test_fehlender_pfad_nennt_die_wege_zur_abhilfe(tmp_path):
    with pytest.raises(WTError) as fehler:
        resolve_dll_path(str(tmp_path / "weg" / "tmctl64.dll"))
    meldung = str(fehler.value)
    assert "WT3000_DLL_PATH" in meldung and CONFIG_FILE_NAME in meldung


# ---------------------------------------------------------------------------
# Hilfsmittel
# ---------------------------------------------------------------------------


def test_with_values_ueberschreibt_nur_das_angegebene():
    config = WTConfig.from_environment(ip="10.0.0.5")
    assert config.with_values(ip=None, user="X") == WTConfig(ip="10.0.0.5", user="X")


def test_describe_zeigt_kein_passwort():
    config = WTConfig(ip="10.0.0.5", user="TEST", password="geheim")
    assert "geheim" not in config.describe()
    assert "10.0.0.5" in config.describe()
