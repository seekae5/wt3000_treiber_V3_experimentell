# P-3 — CSV-Zeile gegen den Spaltenkopf absichern

**Datum:** 2026-08-19
**Bezug:** [PLAN_BEFUNDE_2026-08-19.md](PLAN_BEFUNDE_2026-08-19.md) P-3 · Befund BF-H3 · Befund B-07 aus [AENDERUNGEN_2026-08-18.md](AENDERUNGEN_2026-08-18.md)
**Stand vorher:** 186 Tests grün · **Stand nachher:** 193 Tests grün, weiterhin ohne Gerät und ohne `tmctl.dll`, `pyflakes` ohne Meldung

---

## 1 — Das Problem

Der Spaltenkopf der CSV entsteht aus der Item-Tabelle, die Datenzeilen aus der
gelesenen Werteliste. Zwischen beiden gab es keinen Abgleich:

* `read_numeric_values(..., expected_count=n)` protokollierte eine abweichende
  Anzahl nur als Warnung.
* `CsvRecorder.write_row()` baute die Zeile aus vier festen Feldern, `len(values)`
  Wertzellen und der Flag-Spalte — ohne `len(self._columns)` je anzusehen.

Bei zu wenigen Werten rutschte `status_flags` unter eine Messwertspalte, bei zu
vielen entstanden unbenannte Spalten hinter dem Kopf. In beiden Fällen bleibt jede
Zeile für sich plausibel; die Verschiebung zeigt sich erst im Vergleich mit dem
Kopf — in der Praxis also erst bei der Auswertung, oft Wochen später und ohne dass
noch nachvollziehbar wäre, welcher Wert eigentlich wohin gehörte.

Das ist der einzige Fehler dieser Codebasis, der die Daten überlebt. Ein Absturz
kostet eine Messreihe; eine verrutschte Spalte macht sie falsch, ohne dass es
jemand merkt.

---

## 2 — Was geändert wurde

### 2.1 Abbruch beim Lesen — eine Abfrage früher
[`wt3000_numeric.py:299–337`](src/wt3000_scpi/wt3000_numeric.py)

`read_numeric_values()` hat einen Schalter `strict` bekommen, Voreinstellung
`True`. Weicht die Werteanzahl von `expected_count` ab, kommt jetzt ein
`ProtocolError` statt einer Warnung.

Warum `ProtocolError` und nicht `WTError`: die Antwort des Geräts passt nicht zu
dem, was `:NUMeric:NORMal?` unmittelbar vorher gemeldet hat. Das ist ein Verstoß
gegen die Übereinkunft zwischen beiden Abfragen. `ProtocolError` erbt von
`WTError`, alle bestehenden `except WTError`-Zweige greifen also weiterhin.

Der Fehlertext benennt die vermutliche Ursache — jemand hat die Item-Tabelle am
Bedienfeld oder aus einer zweiten Sitzung verstellt — und nennt `strict=False` als
Diagnoseweg. Dieser Schalter stellt die alte Warnung wieder her; gedacht ist er zum
Nachsehen, was das Gerät überhaupt liefert, nicht für Messläufe.

### 2.2 Abbruch beim Schreiben — die zweite Bruchstelle
[`wt3000_measure.py:181–188`](src/wt3000_scpi/wt3000_measure.py)

`CsvRecorder.write_row()` prüft `len(values)` gegen `len(self._columns)`, **bevor**
irgendetwas in die Datei geht. Bei Abweichung eine `WTError`, die beide Zahlen, die
laufende Sample-Nummer und den Dateinamen nennt.

Zwei Prüfungen für dieselbe Sache sind hier kein Übermaß: die erste greift, wenn
die Werte vom Gerät kommen, die zweite auch dann, wenn ein Aufrufer den Recorder
direkt füttert — und der Recorder ist genau der Baustein, der in ROADMAP M4-2 zu
einem austauschbaren `SampleSink` wird. Die Zusage „die Zeile passt zum Kopf"
gehört dorthin, wo die Zeile entsteht.

**Abbruch statt Auffüllen**, wie in `Befund.md` vorgeschlagen und im Plan bestätigt:
Eine abweichende Werteanzahl heißt, dass die Item-Tabelle nicht mehr die ist, gegen
die der Kopf geschrieben wurde. Aufgefüllte oder abgeschnittene Zeilen wären dann
inhaltlich falsch, nicht bloß unvollständig — und niemand würde es der Datei ansehen.

### 2.3 `map_values()` bleibt bewusst bei der Warnung
[`wt3000_numeric.py:234–268`](src/wt3000_scpi/wt3000_numeric.py)

Hier wurde nur der Docstring ergänzt. Die Trennung ist Absicht:

| Stelle | Verhalten | Begründung |
|---|---|---|
| `read_numeric_values()` | Abbruch | Datenpfad — hier entsteht die Werteliste |
| `CsvRecorder.write_row()` | Abbruch | Datenpfad — hier entsteht die Datei |
| `ItemTable.map_values()` | Warnung | Anzeige und Diagnose |

`map_values()` liefert ein Dictionary zum Nachschlagen; wer nachschlägt, merkt einen
fehlenden Schlüssel sofort. Ein Abbruch dort würde die Diagnose gerade dann
unmöglich machen, wenn man sie braucht — nämlich um zu sehen, welche Items das
Gerät überhaupt geliefert hat.

### 2.4 Ein offener Punkt ist damit entschieden
`tests/test_numeric_parser.py::test_zu_wenige_werte_werden_gemeldet` war
ausdrücklich als Anschlagpunkt für genau diese Entscheidung angelegt (*„Wird die
Fundstelle NUMERIC-1 spaeter auf einen harten Abbruch umgestellt, schlaegt genau
dieser Test an"*). Die Entscheidung ist gefallen und fiel differenziert aus, siehe
Tabelle oben. Der Test bleibt deshalb unverändert bestehen; sein Docstring hält ab
jetzt nicht mehr eine offene Frage fest, sondern die getroffene Festlegung.

---

## 3 — Prüfung

Sieben neue Fälle in [tests/test_fake_transport.py](tests/test_fake_transport.py),
alle gerätefrei.

| Test | prüft |
|---|---|
| `test_zu_wenige_werte_werden_nicht_geschrieben` | 2 Werte, 3 Spalten → `WTError`; die Datei enthält danach **nur** den Kopf, keine halbe Zeile |
| `test_zu_viele_werte_werden_nicht_geschrieben` | 4 Werte, 3 Spalten → `WTError` |
| `test_passende_anzahl_wird_unveraendert_geschrieben` | Gegenprobe: Zeilenlänge = Kopflänge, `status_flags` an letzter Stelle |
| `test_abweichende_werteanzahl_bricht_beim_lesen_ab` | `read_numeric_values(expected_count=4)` gegen einen Block mit 2 Werten → `ProtocolError` |
| `test_strict_false_liefert_die_werte_mit_warnung` | Diagnoseweg bleibt offen |
| `test_passende_anzahl_geht_ohne_beanstandung_durch` | Gegenprobe zum Regelfall |
| `test_messschleife_bricht_bei_verschobener_item_tabelle_ab` | Der Fall aus der Praxis: die Schleife läuft nicht mit falsch beschrifteten Spalten weiter — und `HOLD` wird trotzdem abgeschaltet |

Der letzte ist der wichtigste: er belegt, dass der neue Abbruch die
Aufräumzusagen aus dem `finally` von `NumericHold` nicht aushebelt.

**Gegenprobe durchgeführt.** Mit vorübergehend ausgebauten Prüfungen fallen vier der
sieben durch:

```
FAILED test_zu_wenige_werte_werden_nicht_geschrieben
FAILED test_zu_viele_werte_werden_nicht_geschrieben
FAILED test_abweichende_werteanzahl_bricht_beim_lesen_ab
FAILED test_messschleife_bricht_bei_verschobener_item_tabelle_ab
```

Die drei übrigen sind Negativkontrollen und bestehen erwartungsgemäß auch ohne die
Korrektur.

```
193 passed
pyflakes: keine Meldung
```

---

## 4 — Auswirkung auf bestehenden Code

**Verhaltensänderung für alle vier Aufrufer von `read_numeric_values()`:**
`stage2_read_numeric.py:88`, `stage3_own_itemtable.py:96`, `wt3000_measure.py:349`
(die Messschleife) und `wt3000_device.py:393` (`MeasureControl.read_values`). Alle
übergeben bereits `expected_count`; alle brechen ab jetzt ab, statt weiterzumessen.

Das ist der Zweck der Änderung. Praktisch tritt der Fall nur ein, wenn sich die
Item-Tabelle während des Laufs ändert — und dann ist Abbrechen richtig. Kein
Aufrufer musste angepasst werden: alle fangen `WTError`, und `ProtocolError` erbt
davon.

---

## 5 — Was offen bleibt

* **Paket A des Plans:** nur noch P-4 (Blockheader vollständig validieren) offen.
* **ROADMAP M4-3 wird davon berührt:** die CSV enthält weiterhin keine Einheiten,
  und `write_metadata()` ist nicht an den Recorder gekoppelt. Die Spaltenzuordnung
  ist ab jetzt zuverlässig — was in den Spalten steht, ist damit noch nicht
  selbsterklärend.
* **Nicht angefasst:** dass `CsvRecorder` seine Spaltennamen ungeprüft aus
  `item.key` bezieht. Enthält ein Messprofil dasselbe Item zweimal, entstehen zwei
  gleichnamige Spalten — `map_values()` hängt in diesem Fall `#2` an, der Kopf der
  CSV nicht. Kein aktuelles Profil trifft das; es gehört zu M4-1, wenn `Sample` und
  Spaltennamen aus einer Hand kommen.
