# Fehlerprüfung wt3000_scpi — Änderungen und Befunde

**Datum:** 2026-08-18
**Stand vorher:** `wt3000-scpi 0.3.0`, Commit `919873f`, 115 Tests grün
**Stand nachher:** 124 Tests grün, `pyflakes` ohne Meldung, `tools_import_check.py` in Ordnung

**Prüfumfang:** alle 14 Module unter `src/wt3000_scpi/`, die 7 Testdateien und
`tools_import_check.py` (6021 Zeilen). Kein Gerät und keine `tmctl.dll` beteiligt —
geprüft wurde durch Lesen, statische Analyse und die vorhandene Testsuite.

**Änderungsregel für diesen Durchgang:** geändert wurde ausschließlich, was ein
direkter Fehler, ein Duplikat oder eine unklare Bezeichnung ist. Alles andere steht
unter [Befunde ohne Änderung](#befunde-ohne-änderung) und wartet auf eine
Entscheidung. Jede Änderung ist im Quelltext mit `UEBERARBEITET (F-nn)` markiert und
hier unter derselben Nummer beschrieben.

---

## Übersicht

| Nr. | Art | Datei | Kurz |
|-----|-----|-------|------|
| [F-01](#f-01) | tote Einbindung | `wt3000_measure.py` | `import math` unbenutzt |
| [F-02](#f-02) | tote Einbindung | `wt3000_rangeio.py` | `is_element_scope` unbenutzt |
| [F-03](#f-03) | Duplikat | `wt3000_itemspec.py` | Kommentarkopf stand zweimal |
| [F-04](#f-04) | Duplikat | `wt3000_itemspec.py` | zweite Fassung der SIGMA/SIGMB-Regel |
| [F-05](#f-05) | **Fehler** | `wt3000_input.py` | Wiederherstellung bricht an Gerätekurzform ab |
| [F-06](#f-06) | Fehler | `stage2_read_numeric.py` | verdeckte Modulvariable `_SESSION` |
| [F-07](#f-07) | Fehler | `stage2_read_numeric.py` | Fernsteuerung blieb nach Abbruch an |
| [F-08](#f-08) | Duplikat | 5 Stufenskripte | `setup_logging()` fünfmal identisch |
| [F-09](#f-09) | unklare Bezeichnung | `wt3000_itemspec.py`, `wt3000_ranging.py` | zwei `probe_write_capability()` |

F-05 ist der einzige Befund, der am Gerät zu falschem Verhalten führt, ohne dass es
auffällt: er blockiert die Wiederherstellung des eingemessenen Zustands.

---

## Änderungen

### F-01
**`src/wt3000_scpi/wt3000_measure.py:14` — `import math` entfernt**

Das Modul band `math` ein, benutzte es aber nirgends. Die einzige Stelle, an der
`math` gebraucht wird (`math.nan`/`math.inf` als Sentinel-Werte), liegt in
`wt3000_numeric.py`. Reine Aufräumarbeit, kein Verhaltensunterschied.

### F-02
**`src/wt3000_scpi/wt3000_rangeio.py:38` — `is_element_scope` aus der Importliste entfernt**

Ebenfalls eingebunden, aber nie aufgerufen. Die Funktion selbst bleibt in
`wt3000_common.py:94` bestehen — sie gehört zur öffentlichen Schnittstelle und wird
in `tests/test_scope_and_items.py` geprüft.

### F-03
**`src/wt3000_scpi/wt3000_itemspec.py:73` — doppelter Kommentarkopf entfernt**

Der Block

```
# ---------------------------------------------------------------------------
# Vergleichsregeln
# ---------------------------------------------------------------------------
```

stand zweimal unmittelbar hintereinander. Reine Dublette.

### F-04
**`src/wt3000_scpi/wt3000_itemspec.py:101` — `_canonical_element()` leitet an `wt3000_common` weiter**

`wt3000_itemspec._canonical_element()` war eine vollständige, Zeile für Zeile
identische Zweitfassung von `wt3000_common.canonical_element()`
(`wt3000_common.py:74`). Der Kopf von `wt3000_common.py` benennt diesen Zustand
selbst: *„liegt die Regel ab jetzt genau EINMAL – hier"*, und der Docstring von
`canonical_element()` sagt ausdrücklich *„wt3000_itemspec._canonical_element() kann
hierher delegieren"*. Die Delegation fehlte bloß.

Warum das mehr als Kosmetik ist: es geht um genau die Regel, aus der der
ursprüngliche SIGMA/SIGMB-Vertauscher entstanden ist. Zwei Kopien einer
Sicherheitsregel bedeuten, dass eine korrigiert wird und die andere stehen bleibt.
`tests/test_scope_and_items.py::test_beide_kopien_der_regel_sind_deckungsgleich`
prüft bislang, dass die Kopien übereinstimmen — dieser Test kann bestehen bleiben und
ist ab jetzt trivial erfüllt.

Der Name `_canonical_element` bleibt als dünne Weiterleitung erhalten, damit
bestehende Aufrufer und Tests unverändert laufen. Die Schichtung bleibt gewahrt:
`wt3000_itemspec` darf laut `tests/test_package_layout.py` aus `wt3000_common`
importieren.

### F-05
**`src/wt3000_scpi/wt3000_input.py:887` (`set_sync_source`) und `:987` (`_set_mode`) — Kurzform des Geräts wird angenommen**

**Das ist der eigentliche Fehler dieses Durchgangs.**

Ausgangslage: Mit `VERBose OFF` — dem Sollzustand des Projekts — antwortet das Gerät
in Kurzform. `:INPut:SYNChronize:ELEMent1?` liefert `EXT`, nicht `EXTERNAL`;
`:INPut:VOLTage:MODE:ELEMent1?` liefert `RMEA`, nicht `RMEAN`.

`InputSnapshot.capture()` (`wt3000_input.py:1151`) legt diese Antworten unverändert in
den Snapshot: `sync_source=config.get_sync_source(element)`. `restore_input_snapshot()`
(`:1372`) reicht denselben Wert wieder an den Setter zurück:
`config.set_sync_source(wanted.sync_source, element)`.

Der Setter prüfte die Eingabe aber exakt gegen die **Langformen** der Aufzählung:

```python
upper = token.upper()
valid = {s.value.upper() for s in SyncSource}
if upper not in valid:
    raise WTError(f"Ungueltige Sync-Quelle {source!r} ...")
```

`'EXT'` steht nicht in dieser Menge. Die Wiederherstellung des eingemessenen Zustands
brach also mit *„Ungueltige Sync-Quelle 'EXT'"* an einem Wert ab, den das Gerät
unmittelbar vorher selbst geliefert hatte.

Beim Messmodus ist die Wirkung eine Stufe schlimmer: der Fehler tritt in
`_set_mode()` auf, wird also von `_restore_mode()` (`:1355`) **nicht** aufgefangen —
das fängt ausschließlich `ConfigLocked`. Ein `WTError` aus dem Modus-Setter reißt die
komplette `restore_input_snapshot()` ab, mitten in der Wiederherstellung, mit
teilweise zurückgestelltem Gerät.

Das ist der Restbestand der Korrektur zu INPUT-13. Diese hatte Vergleich (`diff()`)
und Wiederherstellungs-Entscheidung auf **eine** Regel gebracht (`enum_match()`), den
Eingang der Setter aber ausgelassen. Der Kommentarblock ab `wt3000_input.py:307`
beschreibt das Ziel korrekt — die Umsetzung war unvollständig.

Änderung: beide Setter normalisieren die Eingabe zuerst über `canonical_enum_token()`
auf die Langform und prüfen erst danach. Gesendet wird die Langform.

```python
canonical = canonical_enum_token(token, SYNC_TOKENS)
if canonical not in SYNC_TOKENS:
    raise WTError(...)
```

Was dabei ausdrücklich **nicht** aufgeweicht wird:

* Mehrdeutige Kurzformen (`'U'` passt auf `U1..U4`) gelten weiterhin als Fehler.
  `canonical_enum_token()` gibt bei mehreren Kandidaten den Text unverändert zurück,
  die Prüfung schlägt an. Raten wäre hier schlimmer als abbrechen.
* Unbekannte Werte werden weiterhin abgewiesen.
* Beide Schreibsperren (`allow_changes`, `protected_groups`) sind unberührt.

Nebenbei entfielen zwei weitere Duplikate: `valid = {s.value.upper() for s in
SyncSource}` war eine zweite Bildung der bereits vorhandenen Modulkonstante
`SYNC_TOKENS`, `{m.value for m in MeasMode}` eine von `MODE_TOKENS`.

**Neue Regressionstests:** `tests/test_input_setters.py` (9 Fälle) — Kurzform geht
hinein, Langform ebenso, Mehrdeutiges und Unbekanntes fliegt weiterhin raus, die
Gruppensperre greift unverändert.

### F-06
**`src/wt3000_scpi/stage2_read_numeric.py:85` — Sitzung als Parameter statt als Modulvariable**

Stufe 2 hielt die Sitzung in einer modulweiten Variablen:

```python
def read_numeric_values_for(table: ItemTable):
    return read_numeric_values(_SESSION, expected_count=len(table.items))

_SESSION: WTSession | None = None
```

`_SESSION` wurde erst in `main()` über `global` gesetzt. Jeder Aufruf von
`log_reading()` außerhalb von `main()` — Import, Test, Wiederverwendung als
Bibliothek — trifft auf `None` und läuft in einen `AttributeError`, statt eine
verständliche Meldung zu liefern. Die Modulvariable wird zudem beim Import angelegt
und beim zweiten `main()`-Aufruf im selben Prozess mit einer neuen Sitzung
überschrieben.

Stufe 3 löst dieselbe Aufgabe direkt: `read_and_log(session, table, cycle)`. Stufe 2
macht es jetzt genauso. `read_numeric_values_for()` und `_SESSION` sind ersatzlos
entfallen.

### F-07
**`src/wt3000_scpi/stage2_read_numeric.py:154` — `disable_remote()` in `finally`**

Bei `use_remote=True` schaltete Stufe 2 die Fernsteuerung ein
(`:COMMunicate:REMote ON`, Bedienfeld bis auf LOCAL gesperrt), aber in der
Hauptsitzung nie wieder ab. Abgeschaltet wurde nur in der zweiten, kurzen
Wiederherstellungs-Sitzung im `finally` — und die wird ausschließlich geöffnet, wenn
`backup is not None`. Bricht der Lauf vorher ab (Verbindungsprüfung, `HEADer`- oder
`FORMat`-Prüfung, Fehler beim Lesen der Item-Tabelle), bleibt das Gerät mit
gesperrtem Bedienfeld zurück.

Stufe 3 (`stage3_own_itemtable.py:209`) und Stufe 4 (`stage4_measure.py:220`) machen
es an dieser Stelle bereits richtig. Stufe 2 hat jetzt dasselbe `try/finally` um den
Nutzteil.

Wirksam nur bei `use_remote=True`; die Voreinstellung in `WTConfig` ist `False`.

### F-08
**`src/wt3000_scpi/wt3000_common.py:206` — `setup_logging()` liegt einmal statt fünfmal**

`setup_logging()` stand in allen fünf Stufenskripten als **byteweise identische**
Kopie (je 546 Zeichen). Das ist dieselbe Konstellation, aus der laut `__init__.py` der
Klon unter `Build/` entstanden ist: eine Kopie wird angepasst, die anderen bleiben
stehen.

Die Funktion liegt jetzt in `wt3000_common.py`; die fünf Skripte importieren sie. Die
Wahl des Moduls ist begründet: `setup_logging()` hängt ausschließlich an der
Standardbibliothek, kennt kein Gerät und kein Kommando — das ist genau die Definition
von `wt3000_common`. Ein eigenes Modul hätte die Schichtliste in `__init__.py` und in
`tests/test_package_layout.py` mitgezogen, ohne etwas zu gewinnen.

Im Docstring steht jetzt außerdem der Hinweis, dass eine Bibliothek diese Funktion
nicht aufrufen sollte — sie leert die Handler des Root-Loggers, was in einer
größeren Anwendung deren Logging abschaltet. Für die Stufenskripte, die den Prozess
allein bewohnen, ist das richtig; für den Bibliotheksbetrieb nicht.

Der nicht mehr gebrauchte `import sys` ist in allen fünf Skripten entfallen.

### F-09
**`probe_write_capability()` → `probe_item_write_capability()` / `probe_range_write_capability()`**

Es gab zwei öffentliche Funktionen desselben Namens mit völlig verschiedener Wirkung:

| bisher | Modul | tut |
|--------|-------|-----|
| `probe_write_capability(session, target, backup)` | `wt3000_itemspec` | schreibt **ein Item** der NUMeric-Tabelle |
| `probe_write_capability(access, backup)` | `wt3000_ranging` | schreibt einen **Messbereich** der INPut-Gruppe |

Beide werden von Stufenskripten unter dem bloßen Namen importiert (Stufe 3 und 4 die
erste, Stufe 5b die zweite). In einer Bibliothek ist das eine Stolperfalle: ein
vertauschter Import verändert eine Item-Tabelle, wo ein Messbereich gemeint war — und
die Messbereiche sind der eingemessene Teil des Aufbaus.

Neue Namen: `probe_item_write_capability()` und `probe_range_write_capability()`.
Alle vier Aufrufstellen sind mitgeführt. Bewusst **ohne** Alias unter dem alten Namen —
ein Alias hieße wieder zwei Namen für dieselbe Sache, und bei Version 0.3.0 vor der
Bibliotheksfreigabe ist das der günstigste Zeitpunkt für den Schnitt.

> **Achtung, Schnittstellenänderung:** eigener Code außerhalb dieses Projektbestands,
> der `probe_write_capability` importiert, muss angepasst werden.

---

## Nicht geändert, obwohl auffällig: Zeilenenden

Die Dateien im Paket haben gemischte Zeilenenden: `wt3000_input.py`, `__init__.py`,
alle Tests und `tools_import_check.py` benutzen LF, die übrigen zwölf Module CRLF mit
einem einzelnen `\r` als Dateiende. Das ist im Bearbeitungsverlauf einmal versehentlich
vereinheitlicht und danach wieder auf den Ausgangszustand zurückgesetzt worden, damit
der Änderungsvergleich lesbar bleibt. Eine Vereinheitlichung (`.gitattributes` mit
`* text=auto eol=lf`) ist sinnvoll, gehört aber in einen eigenen Schritt — sie berührt
jede Zeile jeder Datei und würde jede inhaltliche Änderung darin unsichtbar machen.

---

## Befunde ohne Änderung

Geprüft, für richtig befunden oder als Entscheidung des Aufbauverantwortlichen
eingestuft — hier dokumentiert, im Quelltext nicht angefasst. Reihenfolge nach
Dringlichkeit.

### B-01 — Zwei Schreibwege auf dieselben SCPI-Knoten, mit verschiedener Parametersyntax
**Hohe Priorität. Am Gerät zu klären.**

`wt3000_rangeio.RangeAccess.set_range()` (`:286`) und
`wt3000_input.InputConfig.set_voltage_range()` (`:744`) /
`set_current_range()` (`:759`) / `set_current_range_sensor()` (`:796`) schreiben **denselben**
Knoten `[:INPut]:VOLTage:RANGe` bzw. `[:INPut]:CURRent:RANGe` — in verschiedener
Schreibweise:

| Knoten | `wt3000_rangeio` | `wt3000_input` |
|--------|------------------|----------------|
| Spannungsbereich | `... 1000` | `... 1000V` |
| Strombereich direkt | `... 5` | `... 5A` / `... 500MA` |
| Sensorbereich | `... EXTernal,10` | `... EXTernal,10V` |

Beide Stellen tragen den Vermerk `ZU VERIFIZIEREN`. Höchstens eine der beiden Formen
kann die richtige sein; unter Umständen akzeptiert das Gerät beide. Solange das nicht
geprüft ist, hängen zwei Module mit unterschiedlicher Annahme am selben Knoten.
Empfehlung: an einem unkritischen Element einmal beide Formen senden und zurücklesen,
danach die unterlegene Form entfernen und die Formatierung an genau einer Stelle
führen.

### B-02 — `InputConfig.unlocked()` gibt mehr frei, als der Aufrufer verlangt
`wt3000_input.py:465`. Der Kontextmanager setzt `self._allow_changes = True` und
entfernt die genannten Gruppen aus `protected_groups`. Da `_require_writable()` beide
Bedingungen prüft, wird durch `allow_changes=True` **jede nicht geschützte Gruppe**
schreibbar — nicht nur die genannte. `DEFAULT_PROTECTED` enthält vier von neun
Gruppen; die übrigen fünf (`AUTO`, `FILTER`, `SYNC`, `MODE`, `RATE`) hängen also
allein am `allow_changes`-Schalter. Nach `with cfg.unlocked(GROUP_RATE):` ließe sich
im Block auch die Sync-Quelle verstellen.

Nicht geändert, weil der dokumentierte Ablauf davon abhängt: das Anwendungsbeispiel im
Docstring von `restore_input_snapshot()` (`:1372`) nennt
`unlocked(GROUP_RANGE, GROUP_FILTER, GROUP_MODE, GROUP_RATE)`, die Wiederherstellung
schreibt aber auch `AUTO`, `SYNC` und `SCALING`. Eine strenge Auslegung würde diesen
Ablauf sofort mit `ConfigLocked` abbrechen. Das ist eine Entscheidung über das
Sicherungskonzept, kein mechanischer Fehler — und sie gehört dem, der den Aufbau
verantwortet.

Zwei saubere Auflösungen: entweder `unlocked()` gibt wirklich nur die genannten
Gruppen frei und die Docstrings nennen die vollständige Liste, oder das Konzept
verzichtet auf die zweite Sperre und dokumentiert `allow_changes` als das eine Schloss.

### B-03 — Zwei Fassungen der Antwort-Parser, mit unterschiedlichem Verhalten
`wt3000_input.py` führt eigene Parser, die den Funktionen in `wt3000_common.py`
entsprechen:

| `wt3000_input` | `wt3000_common` | gleich? |
|----------------|-----------------|---------|
| `strip_header` (`:230`) | `strip_response_header` (`:125`) | **nein** |
| `parse_bool` (`:254`) | `parse_boolean` (`:149`) | fast (`TRUE`/`FALSE` fehlen) |
| `parse_float` (`:264`) | `parse_nr3` (`:139`) | ja |
| `_float_close` (`:300`) | `values_match` (`:175`) | nein (Verhalten bei 0.0) |
| `target_node` (`:197`) | `scope_suffix` (`:107`) | **nein** |

Der wichtigste Unterschied betrifft die Kopfentfernung. `strip_header` nimmt das
*letzte* Leerzeichen-Token, `strip_response_header` schneidet am *ersten* Leerzeichen
und nur, wenn die Antwort mit `:` beginnt. Für `'ELEMENT2 OFF'` (verkettete Antwort
mit eingeschalteten Headern) liefert die erste `'OFF'`, die zweite `'ELEMENT2 OFF'`.
Beide Fassungen sind in Gebrauch und beide sind für ihren Aufrufer plausibel.

`target_node` und `scope_suffix` erzeugen dieselben Zeichenketten, nehmen aber
verschiedene Eingaben an: `target_node('SIGM')` bricht ab, `scope_suffix('SIGM')`
liefert `':SIGMA'`. Beides ist absichtlich so — `tests/test_scope_and_items.py` hält
beide Verhalten fest.

Nicht zusammengeführt, weil eine mechanische Vereinigung das Verhalten am Gerät
ändern würde. Die Testsuite benennt diesen Punkt selbst als offene Aufgabe
(*„bis Punkt 6 der Bearbeitungsreihenfolge sie auf eine reduziert"*). Für die
Bibliotheksfassung ist das der wichtigste verbleibende Aufräumpunkt: `wt3000_input`
ist das einzige Fachmodul, das `wt3000_common` gar nicht benutzt, obwohl die
Schichtung es erlaubt.

### B-04 — `drain_after_failure()` wird nirgends aufgerufen
`wt3000_core.py:322`. Die Methode räumt eine verspätete Antwort nach einem
fehlgeschlagenen Query ab. Sie ist implementiert, dokumentiert und wird von keiner
Stelle im Projekt benutzt.

Am ehesten fällt das in `write_metadata()` (`wt3000_measure.py:204`) auf: dort werden
elf Abfragen nacheinander abgesetzt und `WTError` je Abfrage abgefangen und als
`"<Fehler: ...>"` in die Metadaten geschrieben. Trifft eine Antwort verspätet ein,
liest die *nächste* Abfrage die Antwort der vorigen — alle folgenden Werte sind dann
um eine Position verschoben, ohne dass es jemandem auffällt. Genau dafür ist
`drain_after_failure()` gedacht.

### B-05 — Stufe 2 protokolliert ein aktives HOLD nur
`stage2_read_numeric.py:74`. Die Vorbedingungsprüfung liest `:NUMeric:HOLD?` und
schreibt das Ergebnis mit dem Zusatz *„in Stufe 2 nicht genutzt"* ins Protokoll.
Steht HOLD aus einem abgestürzten früheren Lauf noch auf ON, liefern alle drei
Lesedurchläufe denselben eingefrorenen Datensatz — und das Protokoll sieht dabei
völlig unauffällig aus. Empfehlung: bei `HOLD = 1` eine Warnung, besser einen
Abbruch. Nicht geändert, weil es eine neue Verhaltensentscheidung wäre.

### B-06 — Tote Teilbedingung in `NumericHold.__exit__`
`wt3000_measure.py:106`: `if not self._enabled and not self._armed: return`.
`_armed` wird nur in `refresh()` gesetzt, und `refresh()` kehrt bei
`_enabled=False` sofort zurück — `_armed` kann also nie wahr sein, während
`_enabled` falsch ist. Die zweite Hälfte der Bedingung ist unerreichbar.

Praktische Folge: bei `use_hold=False` wird nie `:NUMeric:HOLD OFF` gesendet. Ist
HOLD aus einem früheren Lauf noch aktiv, bleibt es das — im Widerspruch zum
Klassen-Docstring (*„OFF wird deshalb im __exit__ garantiert gesendet"*). Ob das ein
Fehler oder Absicht ist, hängt daran, ob `use_hold=False` „HOLD nicht anfassen" oder
„ohne HOLD messen" bedeuten soll. Deshalb nicht geändert.

### B-07 — CSV-Zeile kann gegen den Kopf verrutschen
`wt3000_measure.py:154` (`CsvRecorder.write_row`). Die Zeile wird aus
`len(values)` Zellen gebaut, der Kopf aus `len(column_names)` Spalten. Weichen sie ab,
landet `status_flags` in einer Datenspalte und alle folgenden Werte sind verschoben.
Gemeldet wird die Abweichung nur als Warnung in `read_numeric_values()`
(`wt3000_numeric.py`) und in `map_values()`. Für Messdaten, die später ausgewertet
werden, wäre ein harter Abbruch angemessener. `tests/test_numeric_parser.py`
dokumentiert das aktuelle Verhalten ausdrücklich als bewusst offen gelassen
(Fundstelle NUMERIC-1) — die Entscheidung liegt also schon vor und ist nicht meine.

### B-08 — Voreinstellung `dll_path` zeigt auf einen fremden Rechner
`wt3000_core.py:28`:
`C:\Users\Persystems\PycharmProjects\WT3000_SCPI\tmctl8020\dll\tmctl64.dll`.
Für ein Skript ist das eine bequeme Voreinstellung, für eine Bibliothek ist es keine.
Empfehlung für den Bibliotheksschritt: Standard aus einer Umgebungsvariablen
(z. B. `WT3000_TMCTL_DLL`) mit dem heutigen Pfad als letzter Rückfallebene. Die
Fehlermeldung bei fehlender DLL (`:92`) ist bereits klar und nennt den Pfad.

### B-09 — Tabellenzugriffe werfen `KeyError` statt `WTError`
`wt3000_input.py`: `VOLTAGE_RANGES[crest]`, `CURRENT_RANGES[(module, crest)]`,
`SENSOR_RANGES[crest]`. Meldet das Gerät einen unerwarteten Crest-Faktor oder
Elementtyp — etwa weil `:INPut:MODUle?` in einer anderen Schreibweise antwortet als
angenommen —, kommt ein nackter `KeyError` heraus statt einer `WTError` mit Kontext.
Die Stufenskripte fangen nur `WTError`, ein `KeyError` reißt den Lauf also an der
`finally`-Wiederherstellung vorbei. Kleiner Aufwand, klarer Gewinn — aber eine
Verhaltensänderung im Fehlerpfad und damit nicht Teil dieses Durchgangs.

### B-10 — Präfixregel in `_functions_compatible()` deckt eine Richtung nicht ab
`wt3000_itemspec.py:79`. Die Regel `req == act or req.startswith(act)` ist richtig
gewählt: das Gerät antwortet mit `VERBose OFF` in Kurzform, die Antwort muss also ein
Präfix der Anforderung sein. Der Docstring begründet das korrekt.

Der verbleibende Rest: gesendet `UTHD`, zurückgelesen `U` gilt als Treffer, obwohl das
zwei verschiedene Messgrößen sind. Ohne eine vollständige Tabelle der Kurzformen aller
Item-Funktionen ist das nicht auflösbar — mit einer solchen Tabelle wäre die
Präfixregel ganz entbehrlich. Als Restrisiko benannt, unverändert gelassen.

### B-11 — `resolve_wiring_units()` benennt nach Rohposition
`wt3000_input.py:404`. `name = {0: "SIGMA", 1: "SIGMB"}.get(position, "")` zählt auch
Muster `NONE` mit. Bei `('NONE', 'P1W2')` hieße die einzige Unit `SIGMB`. Ob das
richtig ist, hängt daran, wie das Gerät eine leere erste Wiring-Unit meldet — nach
Handbuchlage ist die Positionsbindung vermutlich korrekt. Nicht angefasst, weil eine
Änderung ohne Gerätebeleg raten hieße. Bei mehr als zwei Units bleibt der Name leer;
`sigma_members_from_units()` überspringt solche Einträge sauber.

### B-12 — `_elements_of("ALL")` liefert fest `(1, 2, 3, 4)`
`wt3000_input.py:565`. Bestückung wird nicht berücksichtigt. Die Rückleseprobe nach
einem `:ALL`-Kommando fragt damit auch Elemente ab, die laut `:INPut:MODUle?` nicht
bestückt sind (`module == 0`); `InputSnapshot.capture()` überspringt diese Elemente
dagegen richtig. Auf dem vorliegenden Vier-Element-Aufbau ohne Wirkung.

### B-13 — Messprofil an zwei Stellen, in zwei Fassungen
`wt3000_measure.build_standard_profile()` (31 Items, `FU` nur für Element 3) und
`stage3_own_itemtable.TARGET_ITEMS` (33 Items, `FU` für Elemente 1–3). Die
abweichende Fassung in Stufe 3 ist im Kommentar begründet (Stufe 3 prüft absichtlich
auch die strukturell auf `NO_DATA` laufenden Items). Kein Fehler, aber für die
Bibliothek gehören Messprofile an eine Stelle, mit einem Namen je Profil.

### B-14 — `check_preconditions()` in vier Fassungen
Je einmal in Stufe 2, 3 und 4 (überlappend: `HEADer`, `NUMeric:FORMat`,
`STATus:CONDition`) und einmal in `wt3000_ranging.py` mit ganz anderer Aufgabe. Die
drei Skriptfassungen sind modulprivat, kollidieren also nicht — anders als bei F-09.
Zusammenzuführen lohnt sich, sobald die Stufenskripte zu Beispielen einer Bibliothek
werden; sie unterscheiden sich heute in Kleinigkeiten (Stufe 4 prüft zusätzlich Bit 15
POV und vergleicht das Abtastintervall mit `:RATE?`).

### B-15 — `probe_extra_items()` wertet die Rohantwort ohne Kopfentfernung aus
`wt3000_itemspec.py:142`. `NumericItem.parse(index, response)` bekommt die Antwort auf
`:NUMeric:NORMal:ITEM<n>?` unverändert. Mit eingeschalteten Headern stünde der
Kommandokopf im Funktionsnamen. Alle Stufenskripte prüfen `:COMMunicate:HEADer` als
Vorbedingung und brechen bei `!= 0` ab, der Fall kann also praktisch nicht eintreten —
für die Bibliothek, die ohne diese Vorprüfung benutzbar sein soll, aber schon.

---

## Was geprüft und für richtig befunden wurde

Damit nachvollziehbar ist, was *nicht* offen ist:

* **Sentinel-Bitmuster** `FLOAT_NO_DATA = 0x7E951BEE` und
  `FLOAT_OVERRANGE = 0x7E94F56A` (`wt3000_numeric.py`): nachgerechnet, sie entsprechen
  9.910E+37 (NAN) und 9.900E+37 (INF) und sind als IEEE-Single endlich. Die Prüfung
  auf dem rohen Bitmuster **vor** der Float-Wandlung ist zwingend und korrekt gelöst;
  `math.isnan()` würde hier nicht greifen.
* **Blockheader-Auswertung** `_assemble_block()` (`wt3000_core.py`): `int()` auf
  `bytes` ist in Python 3 zulässig, `int(b'')` wirft `ValueError` und wird gefangen.
  Das Nachlesen bis zur angekündigten Nutzlastlänge ist richtig begrenzt.
* **Protokollregeln** `_validate()`: die Regel „genau ein Query je Programmnachricht"
  und die Längenprüfung inklusive Terminator entsprechen Kapitel 5 des Handbuchs.
* **Reihenfolge in `apply_plan()` und `restore_ranges()`** (`wt3000_ranging.py`):
  erst Autorange aus, dann fester Bereich, dann Autorange auf den Sollwert — die
  Begründung im Kommentar stimmt, und `restore_ranges()` entscheidet richtig **vor**
  dem ersten Schreibkommando, was anzufassen ist.
* **`applied_ranges()`**: die Wiederherstellung liegt im `finally` und läuft damit
  auch bei Strg+C und bei einem Fehler im Nutzblock. Die Verifikation vor dem `yield`
  verhindert, dass der Nutzblock auf einem halb gesetzten Zustand misst.
* **Eingangsart (Sensor/direkt)**: die Korrektur zu RANGEIO-2 ist durchgezogen —
  `RangeValue`, `ranges_match()`, Konfliktschlüssel in `RangePlan.validate()`,
  Sicherung in der JSON-Datei und Vorprüfung gegen das Gerät greifen ineinander.
* **Schichtung**: `tests/test_package_layout.py` prüft sie mit `ast` statt durch
  Konvention, alle Importe zeigen nach unten, keine absoluten Geschwisterimporte.

---

## Prüfung nach den Änderungen

```bash
python -m pytest
```

```
124 passed
```

```bash
python -m pyflakes src/wt3000_scpi/*.py tests/*.py tools_import_check.py
python tools_import_check.py
```

```
(keine Meldung)
wt3000_scpi 0.3.0: 8 Module importierbar.
```

Alle 115 vorher vorhandenen Tests laufen unverändert durch; die 9 neuen Fälle in
`tests/test_input_setters.py` decken F-05 ab.

---

## Empfohlene Reihenfolge für den nächsten Durchgang

1. **B-01** am Gerät klären — solange zwei Schreibwege verschiedene Parametersyntax
   benutzen, ist jede Bereichsänderung ein Versuch.
2. **B-02** entscheiden — das Sicherungskonzept muss eindeutig sein, bevor die
   Bibliothek fremde Aufrufer bekommt.
3. **B-03** auflösen — `wt3000_input` auf `wt3000_common` umstellen, danach gibt es
   jede Regel nur noch einmal.
4. **B-04**, **B-09**, **B-07** — Fehlerpfade härten.
5. Zeilenenden vereinheitlichen (`.gitattributes`), als eigener Commit ohne
   inhaltliche Änderung.
