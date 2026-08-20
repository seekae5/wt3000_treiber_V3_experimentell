# Umsetzungsplan zu ANALYSE_AUFRUFKETTE.md

**Projekt:** `wt3000-scpi 0.3.0`
**Stand:** Quellstand vom 2026-08-20, Commit `7bfd5e7` plus eine unversionierte Änderung
(siehe Abschnitt 1.3), 306 Tests grün (`venv/Scripts/python.exe -m pytest`)
**Grundlage:** [ANALYSE_AUFRUFKETTE.md](ANALYSE_AUFRUFKETTE.md), Befunde A-01 bis A-17
**Zweck:** Aus der Befundliste eine ausführbare Schrittfolge machen — mit begründeter
Reihenfolge, benannten Fundstellen, je Schritt einer Prüfung, die vorher rot ist.

**Abgrenzung:** Dieses Dokument ändert keinen Code. Es legt fest, *was* geändert wird,
*in welcher Reihenfolge* und *woran der Erfolg jeweils abzulesen ist*. Gerätefragen
(M0, H-01…H-07) bleiben außen vor; wo ein Schritt ein Gerät voraussetzt, steht das dabei.

---

## 1 — Ausgangslage

### 1.1 — Was nachgeprüft wurde

Alle Befunde, die dieser Plan anfasst, wurden vor dem Schreiben am Quellstand
nachgesehen. Sie bestehen unverändert:

| Befund | Nachgesehen an | Bestätigt |
|---|---|---|
| A-01 | [stage3_own_itemtable.py:213](../src/wt3000_scpi/stage3_own_itemtable.py#L213), [stage4_measure.py:230](../src/wt3000_scpi/stage4_measure.py#L230) | ja — `session.disable_remote()` steht hinter dem `try/except` im `finally`-Rumpf, nicht in einem eigenen `finally` |
| A-02 | [probe_voltage_range.py:68–79](../tools/hardware/probe_voltage_range.py#L68), [probe_current_range.py:93–104](../tools/hardware/probe_current_range.py#L93) | ja — kein `finally`, kein `enable_remote()`, kein Vergleich `readback` gegen `TEST_VALUE` |
| A-03 | [wt3000_rangeio.py:232, 285–316](../src/wt3000_scpi/wt3000_rangeio.py#L285) | ja — `get_range()`/`set_range()` gehen an `expand_scope()` vorbei |
| A-04 | [wt3000_transport.py:455–459](../src/wt3000_scpi/wt3000_transport.py#L455) | ja, **und einen Fall mehr** — siehe 1.2 |
| A-06 | 6 Stellen laut Analyse | ja, alle sechs unverändert |
| A-07 | [wt3000_measure.py:321–326](../src/wt3000_scpi/wt3000_measure.py#L321) | ja |
| A-08 / A-10 | `main()`-Köpfe aller sieben Skripte | ja — `from_environment()` vor `setup_logging()` und vor jedem `try`; `output_dir()` fünfmal Modulkonstante, zweimal in `main()` |
| A-11 | [test_package_layout.py:24–79](../tests/test_package_layout.py#L24) | ja — `LAYERS` hat 11 Einträge, die fünf Stufenskripte fehlen |
| A-12 | [wt3000_core.py:21–48](../src/wt3000_scpi/wt3000_core.py#L21) | ja — Weiterleitung steht, alle sieben Skripte und die Fassade nutzen sie |
| A-13 | [test_stage5b_write_probe.py:39–54](../tests/test_stage5b_write_probe.py#L39) | ja — Vorrichtung liegt lokal im Testmodul, nicht in `conftest.py` |

Zwei Angaben aus der Analyse sind inzwischen überholt und werden hier korrigiert:

* Der Hinweis auf **gemischte Zeilenenden** trägt nicht mehr. `.gitattributes`
  (Commit `a0b6da2`) normalisiert den Bestand; im Index steht heute **keine** `.py`-Datei
  mehr mit CRLF. Die Arbeitskopie von `probe_current_range.py` ist lokal noch CRLF, wird
  aber beim nächsten Checkout ersetzt. Für diesen Plan heißt das: Dateien dürfen wieder
  mit beliebigen Werkzeugen bearbeitet werden, der Diff bleibt klein.
* Die Testsuite läuft hier unter **`venv/Scripts/python.exe` (3.13.15)**, nicht unter
  `python3.12`. `py -0` kennt keine 3.12. Alle Prüfbefehle in diesem Plan nennen deshalb
  den Interpreter aus `venv/`.

### 1.2 — Ein Fall, den die Analyse bei A-04 nicht nennt

Neben den drei genannten rohen Fehlerwegen und `command.encode("ascii")` gibt es einen
vierten in derselben Klasse:

```python
# wt3000_transport.py, _initialize()
address = f"{cfg.ip},{cfg.user},{cfg.password}".encode("ascii")   # UnicodeEncodeError
```

Ein Passwort mit Umlaut in `wt3000.json` — nicht abwegig — bricht den Verbindungsaufbau
mit `UnicodeEncodeError` ab, also ebenfalls nicht als `WTError`. Der Fall gehört in
Schritt 5 mit hinein und ist dort aufgeführt.

### 1.3 — Eine Änderung, die zurückgenommen gehört

*Nachtrag 2026-08-20:* Diese Änderung war beim Schreiben des Plans unversioniert und ist
inzwischen als Teil von Commit `61ada7d` eingecheckt. An der Sache ändert das nichts —
sie gehört weiterhin zurückgenommen, jetzt eben als eigener Commit statt als Verwerfen
der Arbeitskopie.

`tools/hardware/probe_current_range.py` steht auf

```python
TEST_VALUE: float = 0.75      # vorher: 0.5
```

Der Kommentar unmittelbar darüber führt die gültigen Stufen auf
(`0.005 … 0.2 0.5 1.0 2.0` bzw. `0.25 0.5 1.0 2.5 …`) und begründet ausdrücklich, warum
genau `0.5` gewählt wurde: es ist in *jeder* Tabelle enthalten und trennt damit die
Syntaxfrage (M0-1) von der Rundungsfrage (M0-2). **`0.75` kommt in keiner der drei
Tabellen vor.** Der Lauf stellt damit wieder beide Fragen auf einmal — genau das, was der
Kommentar verhindern soll, und genau die Vermischung, die A-02 dem Skript ohnehin schon
vorwirft.

**Entscheidung für Schritt 2:** `TEST_VALUE` auf `0.5` zurücksetzen. Der Zwischenwert ist
ein eigener, wertvoller Versuch — aber er beantwortet M0-2, nicht M0-1, und gehört
deshalb hinter einen eigenen Schalter (siehe Schritt 2, Ausbaustufe).

---

## 2 — Leitgedanke der Reihenfolge

Die Analyse sortiert nach *Gerätewirkung zu Aufwand*. Das ist die richtige Achse für die
Frage „was ist am schlimmsten", aber nicht für die Frage „womit fange ich an". Dieser
Plan weicht an einer Stelle ab, und zwar aus einem Grund:

> **Die beiden dringendsten Reparaturen (A-01, A-02) sind Fehlerpfad-Reparaturen. Ein
> Fehlerpfad, den man nicht auslösen kann, ist auch nicht prüfbar — und dann ist die
> Reparatur nur eine Behauptung.**

Die Analyse sagt das selbst, bei A-13: A-01 „ließe sich mit derselben Vorrichtung als
Test formulieren". Sie stellt diese Vorrichtung dann aber an Position 8. Damit wären die
Schritte 1 und 2 die einzigen im ganzen Plan, die ohne Nachweis eingebaut würden — und
zwar ausgerechnet die, die auf ein eingemessenes Gerät wirken.

Der Ausweg kostet wenig: der Teil von Schritt 8, der die Vorrichtung tragfähig macht,
ist **A-10** (zwei Zeilen je Skript) und das Heben der drei `monkeypatch`-Zeilen nach
`conftest.py`. Das ist zusammen XS, nicht M. Der teure Teil von Schritt 8 —
**A-09**, `main(config=None)` in sieben Skripten — wird davon nicht berührt und bleibt
hinten.

Daraus ergibt sich die Umsortierung:

| | Analyse | dieser Plan | Begründung |
|---|---|---|---|
| Netz zuerst | Pos. 4 (A-11), Pos. 8 (Vorrichtung) | **Schritt 0** | Kostet zusammen ~40 Zeilen, ist sofort grün und macht die Schritte 1–3 nachweisbar statt behauptbar. |
| A-02 | Pos. 1 | **Schritt 2** | Bleibt die erste inhaltliche Reparatur. Rutscht nur hinter das Netz. |
| A-01 | Pos. 2 | **Schritt 1** | Vor A-02, weil die Vorrichtung aus Schritt 0 ohne Zusatzarbeit trägt (`wt3000_scpi.stage3/4` sind importierbar); A-02 braucht zuerst einen Importweg nach `tools/hardware/` (Schritt 0c). |
| A-09 | Teil von Pos. 8 | **Schritt 8** | Unverändert hinten. Es ist der einzige Schritt mit Schnittstellenänderung. |
| Rest | Pos. 3, 5, 6, 7, 9, 10 | Schritte 3–7, 9, 10 | Reihenfolge der Analyse. |

Jeder Schritt ist einzeln committierbar und lässt die Suite grün zurück.

---

## 3 — Die Schritte

### Schritt 0 — Das Netz aufspannen `XS` · Befunde A-11, A-10, A-13 (Teil)

Drei Teile, ein Commit. Nach diesem Schritt ist jede weitere Änderung an einem
Stufenskript oder Geräteskript maschinell überprüfbar.

#### 0a — `LAYERS` vervollständigen (A-11)

In [test_package_layout.py:24](../tests/test_package_layout.py#L24) fünf Einträge
ergänzen. Die tatsächlichen Importe stehen in Reproduktion 7.7 der Analyse und wurden
nachgesehen — der Test ist beim Anlegen sofort grün:

```python
"stage2_read_numeric":  {"wt3000_core", "wt3000_common", "wt3000_numeric"},
"stage3_own_itemtable": {"wt3000_core", "wt3000_common", "wt3000_numeric",
                         "wt3000_itemspec"},
"stage4_measure":       {"wt3000_core", "wt3000_common", "wt3000_numeric",
                         "wt3000_itemspec", "wt3000_measure", "wt3000_sinks"},
"stage5_input_config":  {"wt3000_core", "wt3000_common", "wt3000_input"},
"stage5b_range_probe":  {"wt3000_core", "wt3000_common", "wt3000_rangeio",
                         "wt3000_ranging"},
```

Dazu ein Kommentarblock im Stil der übrigen Einträge, der festhält, was hier *nicht*
steht und warum: **kein `wt3000_device`** und **kein zweites Stufenskript**. Das ist
dieselbe Regel, die der Eintrag `wt3000_device` schon in Worten führt; sie gilt ab jetzt
in beide Richtungen. Genau diese Regel ist es auch, die Schritt 8 später einhalten muss —
`main(config=None)` darf die Stufen nicht dazu verleiten, sich gegenseitig zu importieren.

*Nebenwirkung, die zu prüfen ist:* `test_importrichtung_zeigt_nach_unten` wird von 11 auf
16 Parametrisierungen wachsen. Die Gesamtzahl der Tests steigt entsprechend; Zahlen in
der Dokumentation werden in Schritt 10 gesammelt nachgezogen, nicht hier einzeln.

#### 0b — `OUTPUT_DIR` vereinheitlichen (A-10)

Stufe 2 und Stufe 3 rufen `output_dir()` innerhalb von `main()` auf, die anderen fünf
Skripte legen eine Modulkonstante an. Vereinheitlicht wird **auf die Konstante**, aus
zwei Gründen:

* Sie ist der Mehrheitsfall (5 : 2) und der, den die Vorrichtung aus
  `test_stage5b_write_probe.py` schon ersetzt.
* Sie ist ersetzbar. `monkeypatch.setattr(modul, "OUTPUT_DIR", tmp_path)` trifft einen
  Namen; `monkeypatch.setattr(modul, "output_dir", …)` träfe eine Funktion, die dann für
  jeden anderen Aufruf im selben Modul mitverändert würde.

Der von der Analyse zu Recht gerügte Nebeneffekt — *„der Import tut etwas"* — wird damit
nicht beseitigt, sondern auf alle sieben ausgedehnt. Das ist bewusst, aber es ist eine
Schuld, die benannt gehört. Deshalb gehört in denselben Commit:

* ein Kommentar an den Konstanten, der festhält, dass `output_dir()` beim Import ein
  `exists()` auf bis zu drei Marker je Verzeichnisebene ausführt, und
* die Aufwertung von `test_stufenskripte_fuehren_beim_import_nichts_aus` von einer
  Absichtserklärung zu einer Prüfung: heute stellt der Test nur fest, dass `main`
  aufrufbar ist. Er sollte zusätzlich belegen, dass beim Import **kein Transport
  entsteht und keine Datei angelegt wird** — der Rest (Pfadauflösung) ist dann die
  ausdrücklich zugelassene Ausnahme statt ein unbemerkter Widerspruch.

Die eigentliche Auflösung dieser Fuge ist Schritt 8: sobald `main()` eine `WTConfig`
entgegennimmt, ist der naheliegende nächste Parameter ein `output_dir`, und die Konstante
wird zum bloßen Vorgabewert. Das steht dort.

*Zweiter Teil von A-10*, der hierher gehört und billig ist: im Protokollkopf **beide**
aufgelösten Pfade ausgeben — woher die Konfiguration kam (`config_search_paths()` bzw.
die gefundene Datei) und wohin die Ausgabe geht (`OUTPUT_DIR`). Das Auseinanderlaufen von
`config_search_paths()` und `find_project_root()` wird damit nicht verhindert, aber im
archivierten Lauf sichtbar. Es setzt Schritt 3 voraus (sonst steht die Zeile wieder vor
`setup_logging()`) — also entweder hier nur die `OUTPUT_DIR`-Zeile und die Herkunft der
Konfiguration in Schritt 3 nachziehen, oder 0b und Schritt 3 zusammenlegen.

#### 0c — Die Vorrichtung nach `conftest.py` heben (A-13, Teil)

Aus [test_stage5b_write_probe.py:39–54](../tests/test_stage5b_write_probe.py#L39) wird
eine Fixture-Fabrik in `tests/conftest.py`:

```python
@pytest.fixture
def stufenlauf(monkeypatch, tmp_path):
    """main() eines Stufen- oder Geraeteskripts gegen FakeTransport fahren."""
    def _vorbereiten(modul, responses) -> FakeTransport:
        transport = FakeTransport(responses)
        monkeypatch.setattr(modul, "TmctlTransport", lambda _config: transport)
        monkeypatch.setattr(modul, "OUTPUT_DIR", tmp_path)
        monkeypatch.setattr(modul, "setup_logging", lambda _pfad: None)
        return transport
    return _vorbereiten
```

Der Docstring von `lauf` in `test_stage5b_write_probe.py` begründet die dritte Zeile
ausführlich (`setup_logging()` räumt die Handler des Root-Loggers ab und würde pytests
`caplog` mitnehmen). Diese Begründung wandert mit — sie ist der Grund, warum die Zeile
nicht weggelassen werden darf, und sie gilt ab jetzt für fünf Testmodule statt für eines.

`test_stage5b_write_probe.py` wird auf die gehobene Fixture umgestellt. Das ist der
Regressionsnachweis für 0c selbst: die vorhandenen Tests müssen unverändert grün bleiben.

**Was 0c zusätzlich braucht, damit Schritt 2 daran hängen kann:** Die beiden Skripte
unter `tools/hardware/` sind keine Paketmodule. `testpaths = ["tests"]` und das Fehlen
eines `tools/__init__.py` machen sie aus der Suite heraus nicht importierbar. Der Weg
dahin ist eine Hilfsfunktion in `conftest.py`:

```python
def geraeteskript(name: str):
    """Ein Skript aus tools/hardware/ als Modul laden - ohne Paket, ohne Installation."""
    pfad = Path(__file__).resolve().parents[1] / "tools" / "hardware" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"geraeteskript_{name}", pfad)
    ...
```

Das lädt über den Dateipfad statt über `sys.path` und vermeidet damit genau die Falle,
vor der der Kopf von `probe_current_range.py` warnt: es entsteht kein Importweg, über
den ein Geräteskript versehentlich `tests.conftest` zurückimportieren könnte. Der Import
selbst ist unbedenklich — beide Skripte berühren `TmctlTransport` erst in `main()`, und
die Stilllegung aus `conftest.py` greift ohnehin auf dem Konstruktor, nicht auf dem
Namen.

**Prüfung Schritt 0:** Suite grün, Testzahl gestiegen (16 statt 11 Layer-Parametrisierungen),
`test_stage5b_write_probe.py` unverändert grün auf der gehobenen Fixture.

**Risiko:** gering. Kein Produktivcode außer den `OUTPUT_DIR`-Zeilen in Stufe 2 und 3.

---

### Schritt 1 — REMOTE in Stufe 3 und 4 garantieren `XS` · Befund A-01 — **umgesetzt 2026-08-20**

> **Stand nach der Umsetzung.** Eingebaut wie unten beschrieben (äußeres `finally` um den
> Nutzteil, Fassung von Stufe 2). Nachweis:
> [tests/test_stage_remote_release.py](../tests/test_stage_remote_release.py), 10 Prüfsätze
> über beide Stufen. **Vor der Reparatur rot waren genau zwei** — der Fall, in dem die
> Ausnahme aus der *Wiederherstellung* kommt; die übrigen acht waren bereits grün und sind
> Absicherungen, keine Nachweise. Der Grund steht im Dateikopf des Testmoduls: kam die
> Ausnahme aus dem Nutzteil, lief der `finally`-Rumpf durch und erreichte sein
> `disable_remote()` noch. Nur ein Abbruch *im Restore-Block* übersprang die Zeile.
>
> Die Testvorrichtung steht vorerst lokal im Testmodul und trägt Stufe 3 und 4 bereits —
> Schritt 0c hebt sie später nach `conftest.py`. Die Fallunterscheidung
> `OUTPUT_DIR`-Konstante gegen `output_dir()`-Aufruf (Befund A-10) musste dafür schon hier
> überbrückt werden; sie steht als `_ausgabeziel_umlenken()` im Testmodul und fällt mit
> Schritt 0b weg. Ohne sie schriebe Stufe 3 ihr Backup-JSON bei jedem Testlauf in die
> Projektwurzel.
>
> Nebenbei: vier Zeilen gingen durch die zusätzliche Einrückung über die 100-Spalten-Grenze
> und wurden umbrochen. `git diff -w` zeigt deshalb 42 statt 182 geänderte Zeilen — die
> eigentliche Änderung ist klein, der Rest ist Einrückung.
>
> Geprüft: 316 Tests grün (vorher 306), `ruff` sauber, `mypy` sauber.

**Orte:** [stage3_own_itemtable.py:192–214](../src/wt3000_scpi/stage3_own_itemtable.py#L192),
[stage4_measure.py:211–231](../src/wt3000_scpi/stage4_measure.py#L211)

**Form der Reparatur.** Nicht das `disable_remote()` verschieben, sondern den Nutzteil
klammern — das ist die Fassung, die Stufe 2 in
[stage2_read_numeric.py:158](../src/wt3000_scpi/stage2_read_numeric.py#L158) bereits
hat, und sie deckt zusätzlich den Fall ab, dass die Ausnahme aus dem *Nutzteil* kommt,
bevor `backup` überhaupt gesetzt ist:

```python
if config.use_remote:
    session.enable_remote()
try:
    try:
        ...Nutzteil...
    except WTError as exc:
        log.error("Abbruch: %s", exc)
        exit_code = 1
    finally:
        if backup is not None:
            ...Wiederherstellung mit ihrem eigenen except WTError...
finally:
    session.disable_remote()          # bedingungslos, auch bei KeyError und Strg+C
```

**Warum das gefahrlos ist.** `disable_remote()`
([wt3000_core.py:127–137](../src/wt3000_scpi/wt3000_core.py#L127)) ist bereits
idempotent (`if not self._remote_active: return`) und fängt `WTError` selbst ab. Es kann
also eine gerade propagierende Ausnahme nicht verdrängen. Ein `except BaseException` wie
in der Fassade ist hier nicht nötig — die Fassade brauchte es, weil sie in einem
Konstruktor sitzt, an dessen halbfertigem Objekt kein `close()` aufrufbar wäre; hier gibt
es die Sitzung als lokale Variable.

**Prüfung (vorher rot).** Pro Stufe ein Test auf der Fixture aus 0c, mit dem Prüfsatz aus
der Analyse — *unabhängig davon, wie der Lauf ausgegangen ist*:

```python
def test_remote_wird_auch_bei_nicht_wterror_zurueckgenommen(stufenlauf, monkeypatch):
    transport = stufenlauf(stage3, geraeteantworten())
    monkeypatch.setattr(stage3, "restore_item_table", _wirft(KeyError("Nicht-WTError")))
    with pytest.raises(KeyError):
        stage3.main()
    assert ":COMMunicate:REMote OFF" in transport.written
```

Der Test muss **vor** der Reparatur laufen und fehlschlagen; das ist der Nachweis, dass
er den richtigen Pfad trifft. Reproduktion 7.1 der Analyse ist die Vorlage.

**Offen gelassen:** Ob die Ausnahme danach als `KeyError` weiterlaufen soll oder ob
Stufe 3/4 sie in einen Rückgabewert 1 wandeln sollen, ist eine eigene Frage. Dieser
Schritt entscheidet sie **nicht** — er stellt nur sicher, dass das Bedienfeld frei ist,
egal wie sie ausgeht. Ein `except BaseException` mit Rückgabewert wäre eine
Verhaltensänderung an der Programmoberfläche und gehört zu Schritt 8.

---

### Schritt 2 — Die Geräteskripte belastbar machen `S` · Befund A-02 — **umgesetzt 2026-08-20**

> **Stand nach der Umsetzung.** Alle vier Teile (2a–2d) eingebaut. Nachweis:
> [tests/test_probe_range_tools.py](../tests/test_probe_range_tools.py), 21 Prüfsätze —
> **alle 21 waren vor der Reparatur rot.** Anders als bei Schritt 1 gibt es hier keine
> reinen Absicherungen: die Skripte waren bis dahin vollständig ungeprüft.
>
> `TEST_VALUE = 0.75` ist damit auch empirisch erledigt: der Prüfsatz
> `test_teststrom_ist_eine_gueltige_bereichsstufe` meldete *„fehlt in 4 von 4
> Bereichstabellen"* — genau die Mehrdeutigkeit, die §1.3 aus dem Kommentar hergeleitet
> hatte. Der Wert steht wieder auf `0.5`, und die Regel ist jetzt maschinell festgehalten
> statt nur kommentiert.
>
> Zwei Dinge kamen beim Bauen dazu, die oben nicht stehen:
>
> * **Die Fehlerqueue-Reihenfolge ist ein eigener Prüfsatz geworden.** `assert_no_error()`
>   muss *nach* dem letzten `:RANGe`-Schreibzugriff kommen, sonst deckt sie die
>   Rückstellung nicht mit ab — und die Rückstellung ist der Schreibzugriff, bei dem ein
>   Fehler am meisten wiegt. Am Syntaxbaum nachgeprüft: Rückstellung endet Zeile 175/200,
>   `assert_no_error` steht auf 182/207.
> * **Der Ladeweg für `tools/hardware/`.** Die Skripte werden über
>   `spec_from_file_location` geladen, nicht über einen `sys.path`-Eintrag. Ein solcher
>   Eintrag wäre genau der Weg, über den eine automatische Import-Ergänzung der
>   Entwicklungsumgebung einmal `from tests.conftest import …` in `probe_current_range.py`
>   geschrieben hat (siehe dessen Dateikopf). Diese Hilfsfunktion gehört mit Schritt 0c
>   nach `conftest.py`.
>
> Die Dateiköpfe beider Skripte sind nachgezogen — sie versprachen eine Rückstellung, die
> nur auf dem glatten Weg galt.
>
> Geprüft: 337 Tests grün (vorher 316), `ruff` sauber, `mypy` sauber (auch auf
> `tools/hardware/`, das die Standardkonfiguration nicht erfasst).

**Orte:** [probe_voltage_range.py](../tools/hardware/probe_voltage_range.py),
[probe_current_range.py](../tools/hardware/probe_current_range.py)

Dies ist der Schritt mit der unmittelbarsten Gerätewirkung: beide Skripte schreiben einen
Messbereich an ein eingemessenes Gerät und haben heute keine Rückstellgarantie. Und sie
sind das Werkzeug für den anstehenden Gerätetermin (M0-1) — sie sollten vorher richtig
sein, nicht nachher.

Vier Änderungen, in dieser Reihenfolge:

**2a — `TEST_VALUE` zurück auf `0.5`** (siehe 1.3). Der Wert `0.75` beantwortet M0-2,
nicht M0-1, und macht das Ergebnis mehrdeutig.

**2b — `try/finally` um den Schreibteil.**

```python
original = access.get_range(Quantity.CURRENT, ELEMENT)
log.info("Ausgangswert Element %d: %s", ELEMENT, original.describe(Quantity.CURRENT))
try:
    command  = access.set_range(Quantity.CURRENT, ELEMENT, TEST_VALUE)
    readback = access.get_range(Quantity.CURRENT, ELEMENT)
    ...protokollieren, vergleichen...
finally:
    # Auch bei Strg+C zwischen Schreiben und Ruecklesen.
    access.set_range(Quantity.CURRENT, ELEMENT, original.value, sensor=original.sensor)
session.assert_no_error("Schreibprobe rangeio current")
```

Wichtig ist die Lage von `assert_no_error()`: **hinter** dem `finally`, nicht darin. Die
Fehlerqueue soll den ganzen Vorgang einschließlich Rückstellung abdecken. Bricht der
Nutzteil ab, wird sie nicht mehr erreicht — das ist richtig so, denn dann trägt die
Ausnahme selbst die Aussage, und ein zusätzlicher `DeviceError` würde sie verdecken.

Zu erwägen und im Kommentar zu begründen: die Rückstellung im `finally` kann ihrerseits
scheitern. Dann verlässt ihre Ausnahme das `finally` und verdrängt die ursprüngliche.
Der Bestand hat für genau diesen Fall ein Muster — Stufe 3/4 protokollieren
*„Wiederherstellung fehlgeschlagen: %s - Backup liegt unter %s"* und lassen den
ursprünglichen Fehler stehen. Dasselbe hier: das `finally` bekommt ein eigenes
`try/except WTError`, das protokolliert statt zu werfen, und die Meldung nennt
`original.describe(...)` — den Wert, den jemand am Gerät von Hand zurückstellen muss.
Das ist die wichtigste Zeile des ganzen Skripts, wenn es schiefgeht.

**2c — Maschinelles Urteil statt Protokolllektüre.**

`ranges_match()` liegt in
[wt3000_rangeio.py:139](../src/wt3000_scpi/wt3000_rangeio.py#L139) bereit und vergleicht
Zahlenwert *und* Eingangsart — für den Sensorbereich ist das der Unterschied, den ein
bloßes `values_match()` nicht sieht:

```python
erwartet = RangeValue(TEST_VALUE, sensor=False)
if ranges_match(erwartet, readback):
    log.info("BELEG M0-1: Wert uebernommen - Syntax '%s' ist gueltig", command)
else:
    log.error("BELEG M0-1: gesendet %s, zurueckgelesen %s - Wert NICHT uebernommen",
              format_nrf(TEST_VALUE), readback.describe(Quantity.CURRENT))
    exit_code = 1
```

Der Rückgabewert von `main()` sagt danach etwas aus. Das ist die eigentliche Aufwertung:
das Skript beantwortet die Frage, für die es gebaut wurde, statt sie nur zu protokollieren.

**2d — REMOTE ausdrücklich entscheiden, nicht stillschweigend weglassen.**

Hier weicht der Plan von der Analyse ab. Sie schlägt vor: *„`enable_remote()` entsprechend
`config.use_remote`"*. Das ist für ein Stufenskript richtig, für ein **Diagnoseskript**
aber falsch — es macht den entscheidenden Versuchsparameter von einer Umgebungsvariablen
abhängig, die im Protokoll nicht auftaucht. Genau der Vorwurf aus A-09 (`use_remote` als
stiller Schalter), an der Stelle, an der er am meisten wiegt.

Stattdessen: eine **Modulkonstante neben `TEST_VALUE`**, unabhängig von `config`, und
eine Protokollzeile, die sie nennt.

```python
#: Fernsteuerung waehrend der Probe. Bewusst NICHT aus config.use_remote:
#  M0-1 fragt nach der Syntax, M0-3 nach der Notwendigkeit von REMOTE. Dieses
#  Skript haelt REMOTE fest auf ON, damit ein abweichender Rueckgabewert
#  eindeutig der Syntax zuzuordnen ist. Den Gegenversuch (ohne REMOTE) fuehrt
#  stage5b_range_probe.py, das genau dafuer gebaut ist.
USE_REMOTE: bool = True
```

`True` und nicht `False`, weil M0-1 die Frage nach der Syntax isolieren soll: REMOTE ON
ist der Zustand, in dem ein Schreibzugriff am sichersten angenommen wird. Schlägt der
Rücklesevergleich *trotzdem* fehl, liegt es an der Syntax — und das ist die Aussage, die
gebraucht wird. Ein `disable_remote()` im äußersten `finally` gehört dazu, mit derselben
Begründung wie Schritt 1.

**Prüfung (vorher rot).** Auf der Fixture aus 0c, über `geraeteskript("probe_current_range")`:

| Test | Prüfsatz |
|---|---|
| Rückstellung bei Abbruch | `get_range` wirft beim Rücklesen → `written` endet auf dem Kommando mit dem **Ausgangswert** |
| Rückstellung im Normalfall | letzter Set-Zugriff trägt den Ausgangswert, nicht `TEST_VALUE` |
| Urteil bei Übernahme | Antworttabelle liefert `0.5` zurück → `main() == 0` |
| Urteil bei Nichtübernahme | Antworttabelle liefert `1.0` zurück → `main() == 1` |
| REMOTE | `:COMMunicate:REMote ON` **und** `OFF` stehen in `written` |

Der vierte Test ist der wichtigste — er ist heute nicht formulierbar, weil `main()` immer
0 zurückgibt.

**Risiko:** gering im Code, aber dies ist der Schritt, dessen Ergebnis am Gerät ankommt.
Beide Skripte sollten nach der Änderung einmal vollständig gegen `FakeTransport` laufen,
bevor sie an ein Gerät gehen.

---

### Schritt 3 — Der Anfang der Kette `XS` · Befund A-08

**Orte:** `main()` in allen sieben ausführbaren Skripten.

Zwei Umstellungen von je zwei Zeilen, überall dieselbe:

```python
def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file  = OUTPUT_DIR / f"wt3000_stageX_{timestamp}.txt"
    setup_logging(log_file)                      # (1) ZUERST
    log = logging.getLogger("wt3000.stageX")
    log.info("Protokolldatei: %s", log_file)

    try:
        config = WTConfig.from_environment()     # (2) INNERHALB des try
        log.info("Konfiguration: %s", config.describe())
        with TmctlTransport(config) as transport:
            ...
```

**Warum das trägt:** Der Protokolldateiname hängt nur an `output_dir()` und am
Zeitstempel, nicht an der Konfiguration. Es gibt also keine Abhängigkeit, die die
Reihenfolge erzwänge — sie ist historisch, nicht sachlich.

**Was der Schritt gewinnt**, in dieser Reihenfolge der Wichtigkeit:

1. Eine kaputte oder unlesbare `wt3000.json` — der häufigste Konfigurationsfehler —
   endet mit der Zeile `Abbruch: …` und Rückgabewert 1 statt mit einem Traceback
   (Reproduktion 7.5).
2. Die Warnung über **unbekannte Schlüssel** aus
   [wt3000_transport.py:280](../src/wt3000_scpi/wt3000_transport.py#L280) landet in der
   Protokolldatei statt über `logging.lastResort` auf stderr (Reproduktion 7.6). Ein
   Tippfehler in der Konfigurationsdatei ist damit im archivierten Lauf wiederfindbar.
3. `config.describe()` im Protokollkopf beantwortet die Frage, gegen welches Gerät
   gemessen wurde. Die Methode existiert und wird von **keinem** Stufenskript aufgerufen.
   Das ist die halbe Antwort auf A-09 für den Preis einer Zeile — die andere Hälfte
   (Parameter statt Prozesszustand) kommt in Schritt 8.

**Nachgesehen, zwei Punkte zu `describe()`**
([wt3000_transport.py:156–159](../src/wt3000_scpi/wt3000_transport.py#L156)):

* Das **Passwort ist bereits ausgenommen** — der Docstring sagt es und der Code hält es
  ein (`ip`, `user`, `dll_path`, sonst nichts). Es wird also keine maskierende Fassung
  gebraucht; die Zeile kann so in ein archiviertes Protokoll.
* Dafür nennt `describe()` **`use_remote` nicht** — und genau das ist der stille
  Schalter aus A-09, der entscheidet, ob das Bedienfeld während des Laufs gesperrt ist.
  `timeout_ms` fehlt ebenfalls. Die Zeile allein beantwortet die Frage also nur halb.

**Daraus folgt für diesen Schritt:** `describe()` um `use_remote` und `timeout_ms`
erweitern — beides sind Verbindungsparameter, beide wirken auf den Lauf, keiner von
beiden ist ein Geheimnis. Das ist eine Zeile in `wt3000_transport` und macht die
Protokollzeile erst zu dem Beleg, als der sie hier eingebaut wird. Der einzige vorhandene
Test dazu — `test_describe_zeigt_kein_passwort`
([test_config_resolution.py:227](../tests/test_config_resolution.py#L227)) — prüft
Anwesenheit der IP und Abwesenheit des Passworts und bleibt von der Erweiterung
unberührt. Er bekommt zwei Zeilen dazu, die `use_remote` und `timeout_ms` einfordern.

**Prüfung (vorher rot):** Auf der Fixture aus 0c, mit einer unlesbaren `wt3000.json` im
`tmp_path` und `monkeypatch.chdir(tmp_path)`:

```python
assert stage5.main() == 1                      # heute: WTError verlaesst main()
assert "Abbruch" in caplog.text
```

Der Test braucht ein echtes `setup_logging()` oder `caplog`; die Fixture legt es still.
Für diesen einen Fall wird die Fixture mit `setup_logging=False` aufgerufen — als
Parameter der Fabrik aus 0c vorzusehen.

---

### Schritt 4 — `RangeAccess` prüft seine Elemente `S` · Befund A-03

**Ort:** [wt3000_rangeio.py:232](../src/wt3000_scpi/wt3000_rangeio.py#L232) (`get_range`),
[:285](../src/wt3000_scpi/wt3000_rangeio.py#L285) (`set_range`)

Beide Methoden führen den Scope künftig über `self.expand_scope(scope)`, bevor sie das
Kommando bauen. Für `get_range()` ist das trivial (die Signatur nimmt schon `element: int`
entgegen), für `set_range()` ist eine Überlegung nötig:

**Die Nebenwirkung, die die Analyse nicht benennt.** `expand_scope()` wirft für einen
SIGMA-Scope einen `WTError`, wenn `RangeAccess` ohne `sigma_members` angelegt wurde
([wt3000_rangeio.py:219](../src/wt3000_scpi/wt3000_rangeio.py#L219)). Heute geht
`set_range(quantity, "SIGMA", …)` in diesem Fall stillschweigend durch — nach der
Umstellung nicht mehr. Das ist eine **Verhaltensänderung**, keine reine Prüfung.

Sie ist trotzdem richtig, und zwar aus einem nachprüfbaren Grund: der einzige Aufrufer,
der `set_range()` mit einem Sammelscope aufruft, ist `apply_range_plan()`
([wt3000_ranging.py:450](../src/wt3000_scpi/wt3000_ranging.py#L450)), und der ruft
unmittelbar danach `expand_scope(spec.scope)` für das Verify auf
([:483](../src/wt3000_scpi/wt3000_ranging.py#L483), [:499](../src/wt3000_scpi/wt3000_ranging.py#L499)).
Der `WTError` fällt dort heute schon — nur eben **nach** dem Schreibzugriff statt davor.
Die Umstellung verschiebt ihn an die richtige Stelle: vor die Leitung, nicht danach. Das
ist genau das Prinzip, das die Analyse in Abschnitt 5 an `_validate()` lobt.

Alle übrigen Aufrufer im Bestand übergeben ganze Zahlen (nachgesehen: `wt3000_ranging`
Zeilen 411/560, beide Geräteskripte). Für sie ändert sich nichts außer der Prüfung.

**Der zweite Teil des Befunds** — `RangeAccess` wird in `stage5b` und beiden Werkzeugen
mit `DEFAULT_ELEMENTS = (1,2,3,4)` erzeugt, also mit einer Annahme statt mit dem
gelesenen Steckbrief — wird hier **nicht** behoben. Das ist S-01/M1-3 und verlangt, dass
`DeviceInfo` die Elementliste liefert. Was hierher gehört, ist eine Zeile im Docstring von
`__init__`, die festhält: die Voreinstellung ist eine Annahme, und wer sie nicht
überschreibt, prüft gegen eine Annahme. Heute liest sich `DEFAULT_ELEMENTS` wie eine
Tatsache.

**Prüfung (vorher rot):** Reproduktion 7.2 als Test —
`set_range(Quantity.VOLTAGE, 7, 1000.0)` wirft `WTError`, und `transport.written` ist
leer. Der zweite Prüfsatz ist der eigentliche: es wurde nichts gesendet.

---

### Schritt 5 — Rohe Fehlerwege übersetzen `S` · Befunde A-04, A-06

Zwei Teile, getrennt committierbar, aber inhaltlich derselbe Vorgang: `except WTError` in
den sieben Skripten zu dem machen, wofür es dasteht.

#### 5a — Layer 0: der DLL-Ladeteil

**Ort:** [wt3000_transport.py:455–459](../src/wt3000_scpi/wt3000_transport.py#L455) und
[:503](../src/wt3000_scpi/wt3000_transport.py#L503) sowie `_initialize()` (siehe 1.2).

Vier Wege, ein Muster. Der Maßstab für die Meldungsqualität ist `resolve_dll_path()`, das
seine drei Abhilfen bereits nennt:

```python
try:
    if isinstance(dll, Path) and hasattr(os, "add_dll_directory"):
        os.add_dll_directory(str(dll.parent))
    self._tm = ct.WinDLL(str(dll))
except AttributeError as exc:
    raise WTError(
        f"ctypes.WinDLL steht auf dieser Plattform nicht zur Verfuegung "
        f"({sys.platform}). TmctlTransport ist Windows-gebunden; "
        "geraetefreie Laeufe gehen ueber FakeTransport."
    ) from exc
except OSError as exc:
    raise WTError(
        f"TMCTL-DLL {dll} konnte nicht geladen werden: {exc}\n"
        "  Haeufigste Ursachen: falsche Bitness (64-Bit-Python braucht "
        "tmctl64.dll), eine fehlende abhaengige DLL im selben Verzeichnis, "
        "oder das Verzeichnis existiert nicht mehr."
    ) from exc
```

Die `encode("ascii")`-Fälle in `write()` und `_initialize()` bekommen je ein
`except UnicodeEncodeError` → `ProtocolError` mit dem beanstandeten Zeichen im Text. Für
`_initialize()` gilt dabei dasselbe wie in Schritt 3: die Meldung nennt das *Feld*
(`user`, `password`, `ip`), nicht den Wert.

**Warum das nicht kosmetisch ist:** Ohne die Übersetzung wird `raise SystemExit(main())`
nie erreicht, der Rückgabewert kommt aus dem Traceback statt aus dem Skript, und in der
Protokolldatei steht nichts. Nach Schritt 3 steht die Protokolldatei bereits — dieser
Schritt füllt sie im häufigsten Installationsfehler überhaupt.

**Prüfung:** `mypy` läuft mit `platform = "win32"` und kennt `ct.WinDLL`; der
`AttributeError`-Zweig ist für mypy erreichbar, weil `hasattr` zur Laufzeit prüft. Falls
mypy den Zweig doch als unerreichbar meldet, ist das ein Hinweis auf die Formulierung,
nicht auf die Sache — dann über `getattr(ct, "WinDLL", None)` gehen. Der Test selbst
ersetzt `ct.WinDLL` per `monkeypatch` durch etwas, das `OSError` wirft, und erwartet
`WTError`; die Konstruktorsperre aus `conftest.py` muss dafür lokal aufgehoben werden —
das ist der eine Ort, an dem das legitim ist, und gehört so kommentiert.

#### 5b — Layer 1–4: `int()` und `float()` auf Geräteantworten

Sechs Stellen, aber nicht sechs gleiche. Der Bestand hat für Zahlenantworten bereits
`parse_nr3()` ([wt3000_common.py:139](../src/wt3000_scpi/wt3000_common.py#L139)), das
den Kommandokopf abstreift und `ValueError` in `WTError` mit Kontext wandelt. Es fehlt
das Gegenstück für Ganzzahlen. Also:

```python
def parse_nr1(response: str, context: str = "") -> int:
    """Ganzzahlantwort (Registerinhalt, Zaehler) in einen int wandeln."""
```

— gebaut wie `parse_nr3()`, in `wt3000_common` (Layer 1, importiert nur `wt3000_core`;
`strip_response_header` und `WTError` liegen bereits dort).

Dann fällt bei der Durchsicht der sechs Stellen etwas auf, das die Analyse nicht
erwähnt: **die Auswertung der Condition-Bits liegt viermal im Bestand** —
[stage2:66–71](../src/wt3000_scpi/stage2_read_numeric.py#L66),
[stage3:83–89](../src/wt3000_scpi/stage3_own_itemtable.py#L83),
[stage4:105–112](../src/wt3000_scpi/stage4_measure.py#L105) und
[wt3000_device.py:808–818](../src/wt3000_scpi/wt3000_device.py#L808), in leicht
abweichenden Fassungen (Stufe 2 kennt Bit 15 nicht, die anderen drei schon). Das ist
S-02 („Parser- und Scope-Regeln liegen mehrfach vor") an einer weiteren Stelle, und
dieser Schritt fasst ohnehin genau diese vier Stellen an.

**Vorschlag:** eine Funktion in `wt3000_common`, die beides tut —

```python
def read_condition(session, log) -> int:
    """':STATus:CONDition?' lesen, auswerten und Auffaelligkeiten protokollieren."""
```

Nein, so nicht: `wt3000_common` kennt keine Sitzung und soll keine bekommen. Richtig ist
die Aufteilung in zwei Teile, die beide sitzungsfrei bleiben:

```python
def parse_condition(response: str) -> int:            # = parse_nr1 mit Kontext
def condition_warnings(bits: int) -> list[str]:       # gibt die Meldungstexte zurueck
```

Die vier Aufrufstellen protokollieren die Liste dann selbst, mit ihrem eigenen Logger.
`wt3000_device.log_condition()` wird zu drei Zeilen, und Stufe 2 bekommt Bit 15 (POV)
dazu, das ihr heute fehlt — eine kleine, aber echte Verbesserung nebenbei.

Die verbleibenden zwei Stellen:

* [stage4_measure.py:96](../src/wt3000_scpi/stage4_measure.py#L96) `float(":RATE?")` →
  `parse_nr3(…, ":RATE")`.
* [wt3000_measure.py:504](../src/wt3000_scpi/wt3000_measure.py#L504) — **die
  kritischste**, weil sie in der laufenden Messschleife sitzt. → `parse_condition(…)`,
  ohne Warnungen (die gehören nicht in eine Schleife, die stundenlang läuft). Ein
  `ValueError` dort beendet heute eine womöglich stundenlange Messreihe mit einem
  Traceback; als `WTError` läuft sie in den vorgesehenen Abbruch von `_loop_body`.

**Prüfung (vorher rot):** Je ein Test mit einer Antworttabelle, die auf
`:STATus:CONDition?` mit `":STATUS:CONDITION 16"` (also mit Header) antwortet. Heute
`ValueError`, danach: korrekt ausgewertete `16`, weil `strip_response_header()` greift.
Das ist der bessere Prüfsatz als ein reines „wirft WTError" — er zeigt, dass die
Übersetzung nicht nur fängt, sondern den Fall auch löst.

---

### Schritt 6 — `drain_after_failure()` in den einen Pfad, der ihn braucht `S` · Befund A-07

**Ort:** [wt3000_measure.py:321–326](../src/wt3000_scpi/wt3000_measure.py#L321)

```python
for key, command in queries.items():
    try:
        device[key] = session.query(command)
    except WTError as error:
        device[key] = f"<Fehler: {error}>"
        session.drain_after_failure()      # <- die eine fehlende Zeile
```

`write_metadata()` ist die einzige Stelle im Bestand, an der ein fehlgeschlagener Query
nicht zum Abbruch führt, sondern die nächste Abfrage nach sich zieht. Sie ist damit auch
die einzige, an der eine verspätete Antwort in die *falsche* Zeile geraten kann — und die
Datei, in der das passiert, ist die, aus der eine Messreihe später interpretiert wird.
Ein plausibel aussehendes, falsches Sidecar ist schlimmer als ein fehlendes.

`drain_after_failure()` ([wt3000_core.py:265](../src/wt3000_scpi/wt3000_core.py#L265))
ist getestet, im gesamten Produktivcode ungenutzt (S-03) und für genau diesen Fall
gebaut. Es setzt das Timeout kurz herunter, liest einmal, verwirft und stellt das Timeout
im `finally` wieder her.

**Prüfung (vorher rot):** `FakeTransport.prime()` existiert genau dafür — sein Docstring
nennt den Fall wörtlich. Ein Test legt eine verspätete Antwort ab, lässt einen Query
scheitern und prüft, dass das **nächste** Metadatenfeld den richtigen Inhalt hat und
nicht den nachlaufenden Rumpf. Ohne die Zeile ist der Test rot.

**Damit ist M1-5s erster Spiegelstrich erledigt** („`drain_after_failure()` in einen
begründeten Produktivpfad integrieren") — und zwar an dem einzigen Ort, den der Bestand
heute dafür anbietet.

---

### Schritt 7 — Die vier ungeprüften Stufen durchspielen `S` · Befund A-13 (Rest)

Nach Schritt 0 trägt die Vorrichtung für alle fünf Stufen und beide Werkzeuge. Was fehlt,
sind die Antworttabellen und die Prüfsätze. Je Skript mindestens:

| Prüfsatz | gilt für |
|---|---|
| `main()` läuft durch und gibt 0 zurück | alle |
| `:COMMunicate:REMote OFF` steht in `written`, egal wie der Lauf ausging | 2, 3, 4, beide Werkzeuge |
| Die Item-Tabelle steht nach `main()` wieder auf dem Ausgangsstand | 3, 4 |
| Der Kopf der Datei sagt die Wahrheit über das, was gesendet wurde | alle — das ist der Befund BF-H4, der `test_stage5b_write_probe.py` überhaupt ausgelöst hat |

Die Antworttabellen wachsen dabei; `range_responses()` aus `conftest.py` ist die Vorlage.
Für Stufe 4 kommt der Blockdatenpfad dazu — das ist der aufwendigste Teil dieses Schritts
und der Grund, warum er nicht in Schritt 0 steckt.

Der letzte Prüfsatz verdient eine eigene Bemerkung: er ist die maschinelle Fassung der
Zusagen aus den Dateiköpfen. Stufe 2 sagt *„verändert die Item-Tabelle NICHT"* und öffnet
trotzdem mit `read_only=False` (A-14). Ein Test *„Stufe 2 sendet kein Kommando, das die
Item-Tabelle berührt"* wäre heute grün — er würde die Zusage festschreiben, bevor
Schritt 9 sie in `read_only=True` überführt.

---

### Schritt 8 — `main(config=None)` `M` · Befund A-09, A-10 (Rest)

Der erste Schritt mit einer Änderung an der Programmoberfläche, deshalb hinten.

```python
def main(config: WTConfig | None = None, output_dir: Path | None = None) -> int:
    """... 'None' heisst weiterhin: aus der Aufloesungskette bzw. OUTPUT_DIR."""
    ziel = output_dir or OUTPUT_DIR
    ...
    config = config or WTConfig.from_environment()
```

Der zweite Parameter ist eine Zugabe, die Schritt 0b vorbereitet hat: er löst die Fuge
„der Import tut etwas" auf, ohne die Konstante zu entfernen — sie wird zum Vorgabewert.
Der `monkeypatch` auf `OUTPUT_DIR` in der Fixture bleibt dabei gültig; Tests können den
Pfad danach wahlweise auch als Argument übergeben.

**Was dabei nicht passieren darf:** dass die Stufenskripte anfangen, sich gegenseitig
oder die Fassade zu importieren, um „gemeinsamen Code" zu teilen. Genau das verhindert
seit Schritt 0a der `LAYERS`-Eintrag. Gemeinsames wandert nach `wt3000_common` (Layer 1)
oder in die Fassade — nie quer.

**`use_remote` als stiller Schalter** (zweiter Teil von A-09) wird hier mit erledigt: nach
Schritt 3 steht `config.describe()` im Protokollkopf, nach diesem Schritt ist der Wert
außerdem am Aufruf übergebbar. Beides zusammen ist die Antwort auf
[wt3000_transport.py:100–107](../src/wt3000_scpi/wt3000_transport.py#L100), wo der Code
selbst verlangt, die Entscheidung *„an der Aufrufstelle zu dokumentieren"*.

**Dies ist die Vorarbeit für M5-2** (gemeinsame Kommandozeile `wt3000` mit Unterbefehlen).
Der Plan baut sie hier **nicht** — er stellt nur sicher, dass die sieben `main()` sie
später aufnehmen können, ohne dass jedes eine eigene Kommandozeile entwickelt.

---

### Schritt 9 — Die vier Entscheidungen `M` · Befunde A-05, A-12, A-14, A-15, A-16

Keine Reparaturen. Jede ist eine Festlegung, die zu treffen und dann zu dokumentieren
ist. Empfehlung je Punkt, damit sie nicht offen im Raum stehen:

| Befund | Frage | Empfehlung | Begründung |
|---|---|---|---|
| **A-05** | `FakeTransport._lookup()` wirft nackten `KeyError` gegen die Zusage des `Transport`-Protocols | **`FakeTransportError(WTError, KeyError)`** einführen | Die Doppelvererbung hält beide Absichten: der Fehler bleibt für `except KeyError` auffällig *und* wird von `except WTError` gefangen. Damit verhält sich ein Trockenlauf im Fehlerfall wie ein Gerätelauf — sonst prüft er genau die Pfade nicht, für die man ihn baut. Zusätzlich: die Zusage im Protocol-Docstring auf *Leitungsfehler* einschränken. Der Punkt entscheidet mit, wie `SocketTransport` später `socket.timeout` behandelt. |
| **A-12** | Weiterleitung `wt3000_core` → `wt3000_transport`: festschreiben oder zurückbauen? | **zurückbauen** | Die Weiterleitung war eine Übergangshilfe von M1-2 und hat ihren Zweck erfüllt. Solange sie steht, ist die Trennung von Layer 0 und 1 am Dateikopf unlesbar — was der erklärte Zweck von M1-2 war. Der Rückbau berührt acht Dateien; nach Schritt 0a meldet der Layer-Test jede Abweichung, vorher hätte er es für fünf davon nicht getan. **Deshalb steht dieser Punkt hier und nicht früher.** |
| **A-14** | Stufe 2 mit `read_only=False` und zweiter Verbindung | **`read_only=True`**, zweites Verbindungspaar entfällt | Solange `EXERCISE_RESTORE_WRITE` auf `False` steht, stellt die zweite Sitzung nichts wieder her und kostet einen `TmcInitialize`, ein `REMote ON`/`OFF`-Paar und ein `:NUMeric:NORMal?`. Der Dateikopf sagt ohnehin *„verändert die Item-Tabelle NICHT"*. Der Test aus Schritt 7 friert das vorher ein. |
| **A-15** | „SCHREIBT NICHTS" deckt `read_error_queue()` nicht ab | **nur dokumentieren** | Kein Fehler, sondern eine Grenze der Zusage: `read_only` sperrt SCPI-Set-Kommandos, „ändert nichts am Gerät" ist etwas anderes — `:STATus:ERRor?` entfernt den Eintrag. Ein Satz in den Köpfen von Stufe 5/5b und einer im Docstring von `read_only`. |
| **A-16** | `WTSession` verlangt eine ganze `WTConfig` für drei Zahlen | **vertagen bis `SocketTransport`** | Keine akute Wirkung. Aber die Entscheidung fällt spätestens beim zweiten Transport, und dann rückwirkend teurer. Was jetzt hineingehört: ein Kommentar an [wt3000_core.py:112](../src/wt3000_scpi/wt3000_core.py#L112), der die drei tatsächlich benutzten Felder benennt (`read_buffer_size`, `drain_timeout_ms`, `timeout_ms`) — damit die Fuge sichtbar ist, wenn jemand sie schließen will. |

A-12 ist der einzige dieser fünf Punkte mit nennenswertem Umfang. Er sollte ein eigener
Commit sein, der nichts anderes tut.

---

### Schritt 10 — Dokumentation nachziehen `XS` · Befund A-17

Gesammelt am Ende, weil mehrere frühere Schritte Zahlen und Aussagen verändern.

| Stelle | Was |
|---|---|
| [README.md:304](../README.md#L304) | Der Widerspruch `1000` gegen `1000V` besteht nicht mehr — `wt3000_input` sendet seit der Stilllegung von `format_voltage()` ebenfalls `format_nrf()`. Absatz streichen oder auf die verbliebene offene Frage (Direktstrom, Sensorstrom) einkürzen. Nach Schritt 2 liefern die Geräteskripte dafür einen maschinellen Beleg — der Text sollte darauf verweisen. |
| README.md, 6 Links | `ROADMAP.md`, `AENDERUNGEN_2026-08-18.md`, `WT3000_Commands_Overview.md` liegen seit `0a415a2` unter `MarkDowns/`. Alle sechs Links gehen ins Leere. `OFFENE_PUNKTE.md` fehlt in der Dokumentationstabelle ganz. |
| [README.md:70](../README.md#L70), [:272](../README.md#L272) | „241 Tests" → aktueller Stand. Heute 306; nach diesem Plan deutlich mehr. **Erwägen, die Zahl ganz zu streichen** — sie ist bei jedem Schritt falsch und trägt nichts, was `pytest` nicht selbst sagt. |
| [wt3000_numeric.py:3](../src/wt3000_scpi/wt3000_numeric.py#L3) | Dateikopf sagt „Layer 3", `__init__.py` und `LAYERS` sagen Layer 2. |
| [wt3000_measure.py:140](../src/wt3000_scpi/wt3000_measure.py#L140) | „Layer 4 — der Datensatz", tatsächlich Layer 3. |
| `MarkDowns/OFFENE_PUNKTE.md` | S-01, S-03, S-05, S-06 als (teil-)erledigt kennzeichnen, mit Verweis auf die Schritte dieses Plans. |
| `MarkDowns/ROADMAP.md` | M1-5 hat nach Schritt 5 und 6 drei von fünf Spiegelstrichen; M5-4 nach Schritt 7 einen Teil. Status nachziehen. |

Die beiden Layer-Angaben in den Dateiköpfen sind die einzigen Einträge dieser Tabelle,
die einen Leser aktiv in die Irre führen — wer die Schichtung am Dateikopf nachvollzieht,
liest dort das Gegenteil dessen, was der Test erzwingt. Sie könnten auch vorgezogen
werden; sie kosten je eine Zeile.

---

## 4 — Zusammenfassung der Schrittfolge

| # | Schritt | Aufwand | Befunde | Prüfung vorher rot? |
|---|---|---|---|---|
| 0 | Netz aufspannen (`LAYERS`, `OUTPUT_DIR`, Fixture nach `conftest`) | XS | A-11, A-10, A-13⅓ | nein — sichert Bestand |
| 1 | REMOTE in Stufe 3/4 garantieren | XS | A-01 | **ja** |
| 2 | Geräteskripte belastbar machen | S | A-02 | **ja** |
| 3 | `setup_logging()` zuerst, Auflösung ins `try` | XS | A-08 | **ja** |
| 4 | `set_range`/`get_range` über `expand_scope()` | S | A-03 | **ja** |
| 5 | Rohe Fehlerwege übersetzen (Layer 0; `int`/`float`) | S | A-04, A-06 | **ja** |
| 6 | `drain_after_failure()` in `write_metadata()` | S | A-07 | **ja** |
| 7 | Die vier ungeprüften Stufen durchspielen | S–M | A-13 | nein — neue Abdeckung |
| 8 | `main(config=None, output_dir=None)` | M | A-09, A-10 | teils |
| 9 | Die vier Entscheidungen (v. a. A-12 Rückbau) | M | A-05, A-12, A-14, A-15, A-16 | nein |
| 10 | Dokumentation nachziehen | XS | A-17 | nein |

**Kritischer Pfad für den Gerätetermin:** Schritte 0 → 2 (→ 3). Alles andere kann danach
kommen. Wer nur einen Nachmittag hat, macht 0, 1, 2 und 3 — das sind vier XS/S-Schritte,
sie decken die drei Befunde mit Gerätewirkung ab, und sie hinterlassen eine Suite, die
den Rest absichert.

**Nicht Teil dieses Plans:** M0 (Gerätefragen), M1-3 (`DeviceInfo` vervollständigen,
S-01), M1-4 (Protokollzustand *herstellen*), M2, M3, M4-3, M5-1/M5-3. Schritt 4 und
Schritt 9 grenzen ausdrücklich gegen M1-3 bzw. gegen die Transportentscheidung ab.

---

## 5 — Rückverfolgung Befund → Schritt

| Befund | Schritt | Art |
|---|---|---|
| A-01 REMOTE in Stufe 3/4 | 1 | Reparatur |
| A-02 Werkzeuge ohne `finally` | 2 | Reparatur |
| A-03 `set_range()` ohne Elementprüfung | 4 | Reparatur |
| A-04 Konstruktor `TmctlTransport` | 5a | Reparatur |
| A-05 `FakeTransport` bricht die Zusage | 9 | Entscheidung → `FakeTransportError` |
| A-06 rohes `int()`/`float()` | 5b | Reparatur + Entdopplung |
| A-07 `write_metadata()` ohne Drain | 6 | Reparatur |
| A-08 `from_environment()` vor `setup_logging()` | 3 | Reparatur |
| A-09 kein `main(config)` | 8 | Umbau |
| A-10 `OUTPUT_DIR` uneinheitlich | 0b (Vereinheitlichung), 8 (Auflösung) | Umbau |
| A-11 `LAYERS` unvollständig | 0a | Absicherung |
| A-12 Weiterleitung in `wt3000_core` | 9 | Entscheidung → Rückbau |
| A-13 vier Stufen nicht durchspielbar | 0c (Vorrichtung), 7 (Tests) | Absicherung |
| A-14 Stufe 2 sperrt ohne zu schreiben | 9 | Entscheidung → `read_only=True` |
| A-15 „schreibt nichts" ≠ „ändert nichts" | 9 | Entscheidung → dokumentieren |
| A-16 `WTSession` verlangt ganze `WTConfig` | 9 | Entscheidung → vertagen |
| A-17 Dokumentation | 10 | Nachzug |
| — `TEST_VALUE = 0.75` (unversioniert) | 2a | Rücknahme, siehe 1.3 |
| — `encode("ascii")` in `_initialize()` | 5a | Reparatur, siehe 1.2 |
