# M4-1 — `Sample`: Datensatz-Objekt statt Parameterliste

**Datum:** 2026-08-20
**Bezug:** [ROADMAP.md](ROADMAP.md) M4-1
**Stand vorher:** 241 Tests grün · **Stand nachher:** 254 Tests grün, 0,59 s, weiterhin ohne Gerät und ohne `tmctl.dll`

---

## 1 — Was umgesetzt wurde

Zwei neue Typen in [wt3000_measure.py](src/wt3000_scpi/wt3000_measure.py) (Layer 4):

| Typ | Zweck |
|---|---|
| `Sample` | Ein vollständiger Messzyklus: `timestamp`, `elapsed_s`, `number`, `condition`, `values`, `mark` |
| `SampleMark` | Bewertung des **Zyklus** — `OK`, `DUPLICATE` (M3-3), `MISSING` (M3-4) |

Vorher wanderte eine Messzeile als fünf getrennte Parameter in `CsvRecorder.write_row()`:

```python
recorder.write_row(timestamp=..., elapsed_s=..., sample=..., condition=..., values=...)
```

Jetzt gibt es genau einen Vertrag zwischen messender und schreibender Seite:

```python
recorder.write(Sample(timestamp=..., elapsed_s=..., number=..., condition=..., values=...))
```

**Geänderte Signaturen.** `CsvRecorder.write_row(...)` → `CsvRecorder.write(sample)`.
Der neue Name ist derselbe, den das `SampleSink`-Protocol aus M4-2 tragen wird — die
Umbenennung fällt damit nur einmal an. Eine `write_row`-Weiterleitung gibt es **bewusst
nicht**: die alte Signatur ist genau das, was M4-1 abschafft, und eine Weiterleitung
hätte den nächsten Sink wieder an ihr Maß genommen.

**`status_flags()` liegt jetzt im Datensatz, nicht im Recorder.** Sie ist die gemeinsame
Grundlage jedes künftigen Ausgabeformats: der Aufrufer bekommt `['mark=DUPLICATE',
'U2=OVERRANGE']` und entscheidet selbst, wie er das unterbringt.

**Der Schleifenzähler heißt `number` statt `sample`.** Ein `int` namens `sample` neben
einem Typ namens `Sample` ist eine Verwechslung, die beim Lesen nicht auffällt, weil
beide Formen im selben Ausdruck plausibel sind.

---

## 2 — Erkenntnisse aus der Umsetzung

### 2.1 Die Kennzeichnung braucht keine neue CSV-Spalte

`SampleMark` gehört laut Roadmap in den Datensatz, gesetzt wird sie aber erst von M3-3
und M3-4. Die naheliegende Umsetzung — eine eigene Spalte `mark` — hätte **jetzt** das
Dateiformat geändert, für ein Feld, das bis auf Weiteres immer `OK` enthält. Jede
bestehende Auswertung hätte die Spalte verdaut, ohne dass ihr etwas geboten wird.

Stattdessen faltet `Sample.status_flags()` die Kennzeichnung in die vorhandene Spalte
`status_flags`, die ohnehin schon Freitext-Marken der Form `NAME=WERT` führt. Die
Spaltenzahl bleibt unverändert; M3-3 muss künftig nur noch `mark` setzen und nichts am
Format anfassen. Die Kennzeichnung steht dabei **vor** den Einzelwerten — bei einem
ausgefallenen Zyklus (`MISSING`, M3-4) ist sie die einzige Angabe, die es überhaupt gibt.

### 2.2 `MISSING` erzwingt einen Datensatz ohne Werte — und das kollidiert mit P-3

M3-4 verlangt, ausgefallene Zyklen als Zeile mit Statuskennzeichnung zu schreiben statt
sie auszulassen. Ein solcher `Sample` trägt keine Messwerte. Genau daran bricht aber die
Längenprüfung aus P-3 ab, die in `CsvRecorder.write()` bewusst erhalten geblieben ist:
`0 Messwerte passen nicht zu 40 Wertspalten`.

Das ist **kein Fehler dieser Umsetzung**, sondern eine Feststellung für M3-4: dort muss
entschieden werden, ob ein `MISSING`-Datensatz mit `NO_DATA`-Werten aufgefüllt wird (dann
bleibt P-3 unangetastet) oder ob `write()` einen Sonderweg für leere Datensätze bekommt.
`tests/test_sample.py::test_ausgefallener_zyklus_ohne_werte_meldet_nur_die_kennzeichnung`
hält fest, dass `status_flags()` diesen Fall schon heute richtig behandelt — die Frage
liegt allein bei der schreibenden Seite.

### 2.3 `frozen=True` mit einem `list`-Feld ist hier die richtige Wahl

Ein gelesener Zyklus ändert sich nicht mehr, also gehört er eingefroren. Dass `values`
trotzdem eine veränderliche Liste bleibt, macht `Sample` nicht hashbar — geprüft, es
löst `TypeError: unhashable type: 'list'` aus. Das stört niemanden: Datensätze werden
geschrieben und verglichen, nicht als Schlüssel benutzt. Der Preis der Alternative wäre
eine Tupel-Kopie je Zyklus bei Messreihen mit 40 Items.

M3-3 und M3-4 setzen `mark` folglich über `dataclasses.replace()`, nicht durch Zuweisung.
Das ist die bessere Reihenfolge: erst den Zyklus lesen, dann bewerten, und das Ergebnis
ist ein neuer Datensatz statt eines nachträglich veränderten.

### 2.4 Der Umbau macht M3-1 kleiner, als er in der Roadmap aussieht

Der Vermerk an `run_measurement_loop()` sagte bisher, ohne M4-1 entstehe die Signatur
zweimal. Das ist erledigt, und mehr als das: aus `recorder.write(datensatz)` wird für den
Generator `stream()` aus M3-1 ein `yield datensatz` — eine Zeile. Die Schleife muss dafür
nicht noch einmal aufgemacht werden. Der Vermerk ist entsprechend auf `ERLEDIGT`
umgestellt; die drei übrigen M3-1-Punkte (`KeyboardInterrupt` im Thread, `stop_event.wait`
statt `time.sleep`, Zuständigkeit für die Rückstellung) stehen unverändert.

---

## 3 — Bewusst nicht mit erledigt

| Punkt | Warum nicht |
|---|---|
| `SampleSink`-Protocol, `CsvSink` | Das ist M4-2. `CsvRecorder` heißt weiter so; nur die Methode trägt schon den künftigen Namen |
| Erkennung von Dubletten / Ausfällen | M3-3 und M3-4. Hier entsteht nur die Stelle, an der das Ergebnis transportiert wird |
| Einheiten am Datensatz | M4-3. `Sample` trägt Werte, keine Metadaten |
| `MeasureControl.read_sample()` | `read_values()` ist ein Einzelabruf ohne Zyklusbezug — `number` und `elapsed_s` wären dort erfunden |

---

## 4 — Prüfung

| | vorher | nachher |
|---|---|---|
| pytest | 241 | **254** (13 neue in `tests/test_sample.py`) |
| ruff | sauber | sauber |
| pyflakes | sauber | sauber |
| mypy | 16 Dateien ohne Befund | 16 Dateien ohne Befund |

Angepasste Aufrufstellen: `tests/test_fake_transport.py` (drei `write_row`-Aufrufe, der
Attrappen-Recorder `Verweigerer`, der Import), `src/wt3000_scpi/__init__.py` (Export von
`Sample` und `SampleMark`), sowie zwei Fließtext-Verweise auf den alten Methodennamen in
`wt3000_numeric.py` und `tests/test_numeric_parser.py`.

`stage4_measure.py` und `wt3000_device.py` brauchten **keine** Änderung: beide reichen
einen `CsvRecorder` an `run_measurement_loop()` durch und rufen `write_row()` nirgends
selbst auf. Dass der Umbau dort folgenlos blieb, ist der Beleg dafür, dass die Fassade
aus M1-1 die Schichtgrenze hält.

---

## 5 — Empfohlene Reihenfolge danach

1. **M4-2** — `SampleSink`-Protocol und `CsvSink`. Jetzt der kleinste Schritt überhaupt,
   weil der Vertrag bereits auf einen Typ eingedampft ist
2. **Thread-Frage in `WTSession`** entscheiden (Lock oder Sitzungsbesitz) — Vorbedingung
   für M3-1, siehe den Vermerk im Klassendocstring
3. **M3-1** — `Measurement` mit `start()`/`stop()` und `stream()`
