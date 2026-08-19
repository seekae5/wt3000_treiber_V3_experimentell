# P-6 — Geräteskript aus der Testsuite, Sicherung dagegen eingebaut

**Datum:** 2026-08-19
**Bezug:** [PLAN_BEFUNDE_2026-08-19.md](PLAN_BEFUNDE_2026-08-19.md) P-6 · Befund Z-2
**Stand vorher:** 204 Tests grün · **Stand nachher:** 206 Tests grün, `pyflakes` ohne Meldung

Die Verschiebung selbst (`tests/test_set_range_with_rangeio.py` →
`tools/hardware/probe_voltage_range.py`) lag bereits im Arbeitsverzeichnis vor.
Geprüft und **beibehalten**; nachgezogen wurden der Dateikopf und die im Plan
vorgesehene Sicherung.

---

## 1 — Prüfung der vorgefundenen Verschiebung

| | |
|---|---|
| Inhalt | `diff` gegen HEAD: unverändert — reine Verschiebung plus Umbenennung |
| Referenzen auf den alten Pfad | keine |
| Skript lauffähig | Import läuft, `main()` vorhanden |
| pytest-Umfang | sammelt weiter nur aus `tests/` (`testpaths`), `tools/` ist draußen |
| `.DS_Store` | von `.gitignore:21` bereits abgedeckt |

Der Name `probe_voltage_range.py` ist besser als der im Plan vorgeschlagene
`probe_set_range.py`: er sagt, *was* geprobt wird, und `probe_*` grenzt sauber
gegen `test_*` ab.

---

## 2 — Dateikopf nachgezogen

Der Kopf trug einen Namen, den die Datei nie hatte
(`test_set_range_with_rangeio_and_rangeprobe.py`), und bezeichnete sich als
„Testskript". Jetzt steht dort der tatsächliche Pfad und die Warnung zuerst:

> `GERAETESKRIPT. Baut eine echte Verbindung auf und SCHREIBT einen Messbereich.`

Dazu der Aufrufweg samt Hinweis auf `pip install -e .` bzw. `PYTHONPATH=src`
und die Begründung, warum die Datei nicht unter `tests/` liegt.

Drei Bezeichner, die noch „test" hießen, sind mitgezogen: Protokolldateiname
(`wt3000_probe_voltage_range_*.txt`), Logger-Name und der Kontexttext der
Fehlerqueue-Prüfung.

---

## 3 — Die Sicherung

`tests/conftest.py` sagt im Kopf zu: *„Die gesamte Suite laeuft OHNE Geraet und
ohne tmctl.dll."* Das war bisher eine Absichtserklärung ohne Durchsetzung.

**Was jetzt greift:** `TmctlTransport.__init__` wird in `conftest.py` auf
Modulebene stillgelegt und meldet stattdessen einen `RuntimeError`, der den Weg
weist (FakeTransport für Tests, `tools/hardware/` für Geräteskripte).

`TmctlTransport` ist das einzige Tor, durch das eine echte Verbindung entsteht —
`WT3000.connect()` und `from_config()` gehen ebenfalls hindurch. Ein Verbot nur
dieser beiden hätte den direkten Weg offen gelassen.

**Warum auf Modulebene und nicht als Fixture:** `conftest.py` wird importiert,
*bevor* pytest die Testmodule einsammelt. Nur so greift die Sperre auch bei
einem Geräteaufruf auf Modulebene — der liefe schon beim Import, also zu einem
Zeitpunkt, den eine Fixture nicht mehr erwischt. Genau dieser Fall war die
Falle aus Befund Z-2.

**Gegenprobe durchgeführt.** Eine Wegwerfdatei mit
`VERBINDUNG = TmctlTransport(WTConfig())` auf Modulebene unter `tests/` abgelegt:

```
ERROR collecting tests/test_zzz_probe_der_sperre.py
E   RuntimeError: TmctlTransport() aus der Testsuite heraus: diese Suite laeuft
    ohne Geraet und ohne tmctl.dll. Fuer Tests 'FakeTransport' benutzen ...
!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!
```

pytest bricht ab, bevor ein einziger Test läuft — das Gerät wird nicht berührt,
und die Meldung nennt Datei und Abhilfe. Die Datei ist wieder entfernt.

**Zwei neue Tests** in [tests/test_package_layout.py](tests/test_package_layout.py):

| Test | prüft |
|---|---|
| `test_testsuite_kann_keine_geraeteverbindung_oeffnen` | die Sperre greift |
| `test_die_sperre_laesst_den_protokollvertrag_unberuehrt` | `issubclass(TmctlTransport, Transport)` funktioniert weiter — der Vertrag hängt an `write`/`read`/`query`/`set_timeout`/`close`, nicht am Konstruktor |

**Nicht betroffen** und deshalb geprüft: der `issubclass`-Test in
`test_fake_transport.py` und das `monkeypatch` auf
`wt3000_device.TmctlTransport` in `test_device_facade.py` — dort wird der Name
ersetzt, der echte Konstruktor also gar nicht erreicht.

---

## 4 — Verworfen: ein zweiter Prüfweg

Der Plan sah ergänzend einen AST-Scanner vor, der `tests/` durchgeht und
anschlägt, sobald eine Testdatei `TmctlTransport` instanziiert. Er war gebaut und
lief — und hat sofort den Test erwischt, der die Sperre belegt und dafür
`TmctlTransport(WTConfig())` aufrufen **muss**.

Eine Ausnahmeliste hätte den Scanner am Leben gehalten, aber er trägt ohnehin
kaum etwas bei: die Sperre in `conftest.py` fängt denselben Fall früher ab, und
pytest nennt beim Collection-Fehler Datei und Zeile von sich aus. Zwei
Mechanismen für eine Regel, von denen einer eine Ausnahmeliste braucht, sind
schlechter als einer ohne. Der Scanner ist wieder entfernt.

---

## 5 — Stand von Paket B

| Nr. | | Status |
|---|---|---|
| P-5 | Schreibprobe in Stufe 5b zum Laufzeitparameter | offen |
| P-6 | Geräteskript aus `tests/`, Sicherung dagegen | ✅ umgesetzt |
