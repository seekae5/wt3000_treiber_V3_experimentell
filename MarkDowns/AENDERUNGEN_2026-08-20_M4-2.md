# M4-2 — `SampleSink`: CSV als eine Implementierung von mehreren

**Datum:** 2026-08-20
**Bezug:** [ROADMAP.md](ROADMAP.md) M4-2 · [AENDERUNGEN_2026-08-20_M4-1.md](AENDERUNGEN_2026-08-20_M4-1.md)
**Stand vorher:** 254 Tests grün · **Stand nachher:** 282 Tests grün, 0,68 s, weiterhin ohne Gerät und ohne `tmctl.dll`

---

## 1 — Was umgesetzt wurde

**Ein Protocol** in [wt3000_measure.py](src/wt3000_scpi/wt3000_measure.py), neben `Sample`:

```python
class SampleSink(Protocol):
    def open(self, columns, metadata) -> None: ...
    def write(self, sample: Sample) -> None: ...
    def close(self) -> None: ...
```

**Ein neues Modul** [wt3000_sinks.py](src/wt3000_scpi/wt3000_sinks.py) mit vier Implementierungen:

| Senke | Zweck |
|---|---|
| `CsvSink` | aus `CsvRecorder` hervorgegangen — Trennzeichen, Statuskodierung, Sofort-Flush unverändert |
| `JsonlSink` | Metadaten **in** der Datei, Werte benannt statt positioniert, angebrochene Datei bleibt auswertbar |
| `CallbackSink` | reicht jeden Datensatz an eine Funktion — die Grundlage für eine Live-Anzeige |
| `MultiSink` | verteilt auf mehrere Senken: CSV für die Auswertung *und* Rückruf für die Anzeige |

Dazu `require_matching_columns()` — Befund B-07 als **eine** Regel für alle Senken statt
einer Fassung in der CSV — und `SinkNotOpen(WTError)` für den Fall „`write()` vor `open()`".

**Die Messschleife** kennt kein Ausgabeformat mehr. Sie öffnet und schließt die Senke
selbst; die Spaltennamen stammen aus der Item-Tabelle, gegen die auch gemessen wird.

**Die Fassade**: `MeasureControl.record(sink, table, …)` nimmt jede Senke,
`record_csv(csv_path, table, …)` bleibt der Einzeiler für den häufigsten Fall.

---

## 2 — Erkenntnisse aus der Umsetzung

### 2.1 Der Schichtungstest hat die Einordnung erzwungen — zu Recht

Nach dem ersten Durchlauf schlug `test_importrichtung_zeigt_nach_unten[wt3000_device]`
fehl: die Fassade importierte `wt3000_sinks`, und der Test kennt die Regel „Layer 4 darf
aus keinem zweiten Layer-4-Modul importieren".

Der Fehler lag nicht im Test, sondern in meiner Einordnung. `wt3000_sinks` **ist kein
Layer 4**: es kennt kein einziges SCPI-Kommando und keine Sitzung, es setzt nur einen
Vertrag um. Damit steht es neben `wt3000_measure`, und die Fassade darf es bündeln — das
ist ihre Aufgabe. Die Einordnung ist in `LAYERS` jetzt ausdrücklich festgehalten,
**in beide Richtungen**:

```python
"wt3000_sinks": {"wt3000_core", "wt3000_numeric", "wt3000_measure"},
```

Der zweite Teil ist der wichtigere: für `wt3000_measure` gibt es **keinen** Eintrag
`wt3000_sinks`. Genau daran hängt das „Fertig, wenn" — stünde er dort, wäre die
Entkopplung wieder dahin, und der Test würde es beim nächsten Mal melden.

### 2.2 Warum das Protocol nicht bei den Implementierungen wohnt

Naheliegend wäre `SampleSink` in `wt3000_sinks.py` gewesen. Das erzeugt aber einen
Zyklus: die Senken brauchen `Sample` aus `wt3000_measure`, und die Messschleife bräuchte
`SampleSink` aus `wt3000_sinks`. Auflösbar wäre das mit `if TYPE_CHECKING`, aber das ist
ein Trick, kein Entwurf.

Der Vertrag gehört ohnehin zum Datentyp, den er transportiert: `Sample` und `SampleSink`
sind ein Paar. So bleibt die Importrichtung eindeutig — `wt3000_sinks` holt sich beide
von dort, nie umgekehrt.

### 2.3 Wer die Senke öffnet, entscheidet mehr als es aussieht

`open(columns, metadata)` getrennt vom Konstruktor zu haben ergibt nur Sinn, wenn
**formatunabhängiger** Code sie ruft. Der Konstruktor nimmt entgegen, was das Format
ausmacht (Pfad, Trennzeichen, Rückruffunktion); `open()` nimmt entgegen, was der Messlauf
mitbringt und was jede Senke gleichermaßen braucht.

Deshalb liegt der Lebenszyklus jetzt in der Messschleife und nicht mehr beim Aufrufer.
Zwei Gewinne: der Spaltenkopf kann nicht mehr aus einer anderen Quelle stammen als die
Daten (vorher übergab der Aufrufer `column_names` von Hand), und `close()` steht in einem
`finally` — dem einzigen Ort, an dem es sich auch bei Abbruch, Fehler und Strg+C zusagen
lässt.

Der Preis ist eine Einschränkung, die man kennen muss und die im Docstring steht: nach
einem Lauf ist die Senke geschlossen. Zwei Messreihen in dieselbe Datei gehen so nicht.

### 2.4 JSON verträgt kein `NaN` und kein `Infinity`

Pythons `json`-Modul schreibt beides klaglos, weil `allow_nan` voreingestellt ist — im
JSON-Standard sind sie aber nicht zulässig, und ein fremder Parser stolpert darüber.
`JsonlSink` schreibt deshalb `null` für den Zahlwert und führt die Unterscheidung
`NO_DATA`/`OVERRANGE` in `status_flags`. Ein eigener Test hält das fest.

### 2.5 `MultiSink.close()` folgt der Regel aus `WT3000.close()`

`open()` und `write()` brechen beim ersten Fehler ab — dort heißt ein Fehlschlag, dass
die Messreihe so nicht zustande kommt. `close()` geht dagegen über **alle** Senken und
meldet den ersten Fehler erst danach. Sonst bliebe wegen einer vollen Platte die zweite
Datei offen. Dieselbe Begründung wie beim Aufräumen der Sitzung: ein misslungener
Schritt darf die folgenden nicht überspringen.

---

## 3 — Bewusst nicht mit erledigt

| Punkt | Warum nicht |
|---|---|
| `ParquetSink` | Das Paket hat `dependencies = []`. Parquet braucht pyarrow oder fastparquet — ob der Treiber eine erste Laufzeitabhängigkeit bekommt, ist eine Projektentscheidung und kein Nebenprodukt dieses Meilensteins. Die Fuge ist offen: eine Klasse, drei Methoden |
| Einheiten am Datensatz | M4-3 |
| Metadaten an die Daten binden | M4-3. `JsonlSink` macht es bereits vor, `CsvSink` nimmt sie entgegen und schreibt sie nicht — eine CSV hat keinen Ort dafür, der nicht den Spaltenkopf beschädigt |
| `write_metadata()`-Sidecar ablösen | Ebenfalls M4-3. Er läuft heute parallel zur Senke weiter |
| Rotation über mehrere Dateien | M4-4 |

---

## 4 — Prüfung

| | vorher | nachher |
|---|---|---|
| pytest | 254 | **282** (25 davon neu in `tests/test_sinks.py`, der Rest aus den parametrisierten Schichtungstests, die das neue Modul mit abdecken) |
| ruff | sauber | sauber |
| pyflakes | sauber | sauber |
| mypy | 16 Dateien ohne Befund | **17** Dateien ohne Befund |

Angepasste Aufrufstellen: `wt3000_device.py` (Import, `record()`, neu `record_csv()`),
`stage4_measure.py` (Import und Aufruf), `__init__.py` (Exporte, `MODULES`,
Schichtungskopf), `tests/test_fake_transport.py` (drei Schleifenaufrufe, der
Attrappen-Recorder), `tests/test_sample.py` (vier `CsvRecorder`-Blöcke),
`tests/test_package_layout.py` (`LAYERS`).

Der Beleg für das Abnahmekriterium steht in
`tests/test_sinks.py::test_zweites_format_ohne_eine_zeile_aenderung_an_der_schleife`:
eine Senke, die es im Paket gar nicht gibt und die von nichts importiert wird, wird von
der Messschleife geöffnet, bedient und geschlossen.

---

## 5 — Empfohlene Reihenfolge danach

1. **Thread-Frage in `WTSession`** entscheiden (Lock oder Sitzungsbesitz) — Vorbedingung
   für M3-1, siehe den Vermerk im Klassendocstring. Steht in keinem Roadmap-Punkt
2. **M3-1** — `Measurement` mit `start()`/`stop()` und `stream()`. Aus
   `sink.write(datensatz)` wird ein `yield datensatz`
3. **M4-3** — Einheiten und Metadaten. `JsonlSink` zeigt bereits, wo sie hingehören
