# Roadmap — vom Stufenskript zur Treiberbibliothek

**Stand:** 2026-08-20, `wt3000-scpi 0.3.0` (M1-2, M1-1, M4-1 und M4-2 umgesetzt)
**Bezug:** [AENDERUNGEN_2026-08-18.md](AENDERUNGEN_2026-08-18.md) (Fehlerprüfung, Befunde B-01…B-15)

**Zielbild.** Der fertige Treiber kann fünf Dinge:

1. Gerätekonfiguration einlesen
2. Gerätekonfiguration einstellen
3. Mess-Konfiguration einlesen und anpassen (Bereiche, Verdrahtung, Filter, Skalierung …)
4. Messung starten und stoppen
5. Messdaten exportieren — CSV, mit Platz für weitere Formate

Dieses Dokument schlüsselt auf, was dafür noch fehlt, in welcher Reihenfolge es
sinnvoll entsteht und wie jeder Punkt konkret umgesetzt werden kann.

**Lesehinweis zu SCPI-Knoten:** Knoten, die im heutigen Code bereits nachweislich
benutzt werden, sind ohne Zusatz genannt. Alles andere ist mit **(prüfen)** markiert —
diese Namen stammen aus der Kommandogruppen-Systematik des WT3000 und sind vor der
Umsetzung gegen IM WT3001E-17EN und das Gerät abzugleichen.

---

## 1 — Ausgangslage

| Zielfunktion | heute vorhanden | Reifegrad |
|---|---|---|
| **1. Gerätekonfiguration einlesen** | nichts Eigenes. Nur Rohabzüge (`:INPut?`, `:MEASure?`, `:COMMunicate?`) in `write_metadata()` — als Text, nicht ausgewertet | **20 %** |
| **2. Gerätekonfiguration einstellen** | nichts. Weder Kommunikation, noch Averaging, Integration, Harmonische, Setup-Speicher | **5 %** |
| **3. Mess-Konfiguration lesen/anpassen** | `InputConfig` deckt Verdrahtung, Bereiche, Auto-Range, Crest, Filter, Skalierung, Sync, Modus, Rate ab. Snapshot mit `capture/save/load/diff/restore`. `RangePlan` als deklarativer Sollzustand für Bereiche | **75 %** |
| **4. Messung starten und stoppen** | blockierende Schleife `run_measurement_loop()`, Abbruch nur per Strg+C. Keine aufrufbare Start/Stop-Schnittstelle, keine Gerätesteuerung (Integrator, Einzelmessung) | **30 %** |
| **5. Messdaten exportieren** | `Sample` als Datensatz-Objekt (M4-1), `SampleSink` als Vertrag mit vier Implementierungen — CSV, JSONL, Rückruf, Bündel (M4-2). Es fehlen Einheiten und die Bindung der Metadaten an die Daten | **80 %** |
| *Querschnitt* | Transport, Sitzung, Fehlerklassen, Item-Tabelle, Blockparser, 282 gerätefreie Tests, saubere Schichtung | **solide Basis** |

**Kurzfassung:** Die untere Hälfte (Transport, Protokoll, Zahlenformate, INPut-Gruppe)
ist belastbar und getestet. Was fehlt, ist die obere Hälfte: eine benutzbare
Schnittstelle, die Gerätegruppen jenseits von `:INPut`/`:NUMeric`, eine steuerbare
Messung und ein austauschbarer Export.

---

## 2 — Meilensteine

| MS | Ziel | Inhalt | grober Umfang |
|----|------|--------|---------------|
| **M0** | Offene Gerätefragen schließen | Was nur am Gerät entschieden werden kann — blockiert M2/M3 | 1–2 Tage **am Gerät** |
| **M1** | Fundament | Fassade `WT3000`, Transport-Protokoll, Gerätesteckbrief, Sollzustand herstellen | 4–7 Tage |
| **M2** | Konfiguration | Gerätekonfiguration lesen/schreiben, Messkonfiguration vervollständigen, ein Backup-Format für alles | 6–10 Tage |
| **M3** | Messung | Start/Stopp als Schnittstelle, Gerätesteuerung, Taktung am Gerät statt per `sleep` | 5–8 Tage |
| **M4** | Export | Sink-Protokoll, Datensatz-Objekt, Einheiten, CSV als erste Implementierung | 3–5 Tage |
| **M5** | Auslieferbar | Paket, Doku, CLI, CI, Typprüfung | 3–5 Tage |

Aufwände sind grob und ohne Gerätezeit gerechnet, außer wo ausdrücklich vermerkt.

---

## M0 — Offene Gerätefragen schließen

> Diese Punkte blockieren echte Arbeit weiter oben. Sie brauchen Gerätezeit, aber
> wenig Programmierzeit. Empfehlung: als *ein* Messtermin planen, Ergebnisse als
> Protokoll ins Projekt legen.

### M0-1 — Parametersyntax der Bereichsknoten festlegen `S · am Gerät`
**Blockiert:** M2 (Messkonfiguration schreiben), M3 (jede Bereichsänderung im Ablauf)
Siehe Befund B-01: `wt3000_rangeio` sendet `1000`, `wt3000_input` sendet `1000V` — auf
denselben Knoten. Höchstens eine Form kann richtig sein.

- Prüfskript nach dem Muster von `stage5b_range_probe.py`: an **einem** unkritischen
  Element (Element 4, Direkteingang) nacheinander `1000`, `1000V`, `1.0E+03` senden und
  jeweils zurücklesen
- Dasselbe für den Sensoreingang: `EXTernal,10` gegen `EXTernal,10V`
- Dasselbe für den Direktstrom: `5A` gegen `500MA` gegen `0.5`
- Ergebnis: die unterlegene Form ersatzlos entfernen, Formatierung an **einer** Stelle führen (`wt3000_common.format_nrf()` erweitern oder `format_voltage/format_current` dorthin ziehen)
- **Fertig, wenn:** eine Formatierungsfunktion existiert, beide Module sie benutzen, und ein Test die gewählte Form festhält

### M0-2 — Rundungsverhalten bei ungültigen Stellwerten `S · am Gerät`
**Blockiert:** `verify_plan(allow_snapping=…)` — die Voreinstellung ist heute geraten

- Einen Zwischenwert senden (z. B. 700 V bei CF3, steht in keiner Tabelle) und zurücklesen
- Drei mögliche Ausgänge unterscheiden: (a) Gerät rundet auf die nächste Stufe, (b) Gerät lehnt ab und legt einen Eintrag in die Fehlerqueue, (c) Gerät übernimmt kommentarlos einen krummen Wert
- Ergebnis bestimmt, ob `_check_allowed()` vorgelagert bleiben muss und wie `allow_snapping` voreingestellt wird
- **Fertig, wenn:** das Verhalten im Docstring von `verify_plan()` steht und der `ZU VERIFIZIEREN`-Vermerk entfällt

### M0-3 — Braucht `:INPut` ein `:COMMunicate:REMote ON`? `S · am Gerät`
**Blockiert:** jede schreibende Nutzung von `InputConfig`/`RangeAccess`

- `python -m wt3000_scpi.stage5b_range_probe --write-probe` einmal laufen lassen — das Skript ist genau dafür gebaut und schreibt einen Nulleffekt. Ohne den Schalter bleibt es rein lesend (P-5)
- Zusätzlich einmal mit `use_remote=True` gegenprüfen
- Ergebnis: `use_remote` wird entweder Voreinstellung `True` oder der Kommentar in `WTConfig` wird zur Feststellung statt zur Vermutung
- **Fertig, wenn:** `WTConfig.use_remote` einen begründeten Standardwert hat

### M0-4 — Antwortformate von `:INPut:MODUle?` und `:INPut:WIRing?` belegen `S · am Gerät`
**Blockiert:** M1-3 (Gerätesteckbrief), Befund B-09

- `InputConfig.get_module()` nimmt an, dass die Antwort `30,30,30,30` lautet (Zahlen). Antwortet das Gerät stattdessen mit Typbezeichnungen, wirft `parse_float()` — und der ganze Snapshot fällt aus
- Rohantworten beider Knoten protokollieren (`stage5_input_config.py` legt sie bereits in den Rohabzug)
- Parser danach auf die tatsächliche Form festziehen, Testfall mit der echten Antwort ergänzen
- **Fertig, wenn:** ein Test die reale Geräteantwort als Eingabe benutzt

### M0-5 — Zeitpunkt eines neuen Datensatzes ermitteln `M · am Gerät`
**Blockiert:** M3-3 (Taktung ohne Drift)

- Heute wird blind im `:RATE`-Takt gepollt. Wiederholungen desselben Datensatzes fallen nur als gleiche Zahlen auf
- Zu prüfen, was das Gerät anbietet: „Updating"-Bit im `:STATus:CONDition?` **(prüfen)**, Extended Event Register über `:STATus:EESE` **(prüfen)**, Serial Poll `:STATus:SPOLl?` **(prüfen)**
- Messreihe: 200 Datensätze mit doppelter Rate lesen und zählen, wie viele identisch sind — das quantifiziert den Nutzen
- **Fertig, wenn:** entschieden ist, ob M3-3 „auf Ereignis warten" oder „Takt plus Dubletten-Erkennung" wird

---

## M1 — Fundament

### M1-1 — Fassade `WT3000` als einziger Einstiegspunkt `M` — **umgesetzt 2026-08-19**
**Das ist die wichtigste fehlende Funktion überhaupt.** Bis hierher musste ein Anwender
Transport, Sitzung, `InputConfig`, `RangeAccess` und die Wiring-Units von Hand
zusammenstecken; `__init__.py` exportierte nur `__version__` und `MODULES`.

- [x] Neues Modul `wt3000_device.py` (Layer 4) mit einer Klasse `WT3000`
- [x] Konstruktion über Klassenmethoden statt vieler Parameter:
  `WT3000.connect(ip=..., read_only=True)` und `WT3000.from_config(WTConfig(...))`.
  Zusatz: `WT3000.from_transport(...)` setzt auf einen bestehenden Transport auf —
  damit läuft die Fassade auf `FakeTransport` (M1-2) und ist gerätefrei prüfbar
- [x] Context Manager: `with WT3000.connect(...) as wt:` — schaltet HOLD ab, schaltet
  REMote ab, schließt den Transport. Jeder Schritt in eigenem `try`, damit ein
  misslungener die folgenden nicht überspringt
- [x] Eigenschaften statt Objektgeflecht: `wt.input`, `wt.ranges`, `wt.items`,
  `wt.device`, `wt.measure` — jede liefert das passende, bereits verdrahtete
  Fachobjekt. `wt.items` und `wt.measure` sind dafür neu (`ItemAccess`,
  `MeasureControl`): die Abläufe in `wt3000_itemspec`/`wt3000_measure` sind freie
  Funktionen mit `session` als erstem Parameter und hatten kein Objekt
- [x] Die bisher manuelle Verdrahtung `sigma_members_from_units(cfg.get_wiring_units())`
  passiert intern und einmalig beim Verbinden, in `DeviceInfo.read()`
- [x] `__init__.py` exportiert `WT3000`, `WTConfig`, die Fehlerklassen und die
  Aufzählungen; `MODULES` bleibt für den Importtest
- [x] Sollzustand **geprüft** (`wt.check_protocol_state()`) — der designierte Ort für
  Befund B-14 und die Grundlage für M1-4, das ihn dann auch herstellt
- [x] **Fertig, wenn:** ein Anwender mit fünf Zeilen eine Verbindung aufbaut, die
  Konfiguration liest und sauber wieder trennt — `tests/test_device_facade.py`,
  23 Testfälle; Suite gesamt 176 statt 151

Vorgezogen aus M1-3, weil die Fassade die Elementliste ohnehin festlegen muss:
`DeviceInfo` liest `:INPut:MODUle?` und gibt `RangeAccess` nur die **bestückten**
Elemente. `InputConfig._elements_of("ALL")` hängt weiter an der Konstanten
(Befund B-12), ebenso die Bereichstabellen (B-09) — das bleibt M1-3.
Einzige Änderung an einem bestehenden Fachmodul: `InputConfig.get_modules()`,
damit die Fassade `:INPut:MODUle?` nicht ein viertes Mal selbst zerlegt (B-03).

Siehe [AENDERUNGEN_2026-08-19_M1-1.md](AENDERUNGEN_2026-08-19_M1-1.md).

### M1-2 — Transport hinter ein Protokoll legen `M` — **umgesetzt 2026-08-19**
Heute ist `TmctlTransport` fest verdrahtet: `ctypes.WinDLL` und `os.add_dll_directory`
machen den Treiber auf Windows festgenagelt und für Tests unerreichbar.

- [x] `typing.Protocol` namens `Transport` mit `write/read/query/set_timeout/close` in ein
  eigenes Modul (Layer 0) — `src/wt3000_scpi/wt3000_transport.py`
- [x] `TmctlTransport` implementiert es unverändert weiter — inhaltlich unverändert aus
  `wt3000_core` dorthin verschoben. `wt3000_core` reicht alle verschobenen Namen
  (`WTConfig`, `TmctlTransport`, `WTError`, `TmctlError`, `ProtocolError`,
  `TM_CTL_ETHER`, `MAX_PROGRAM_MESSAGE_BYTES`) unverändert weiter, damit bestehende
  Importe und `except WTError` wortgleich weiterfunktionieren
- [x] `FakeTransport` als zweite Implementierung: beantwortet Kommandos aus einer Tabelle,
  merkt sich Geschriebenes, kann Blockdaten und Fehlerqueue nachbilden. Damit werden
  `WTSession`, `query_block()` und die gesamte Messschleife **ohne Gerät** testbar —
  heute testet `FakeSession` erst eine Ebene darüber. Zusatz: `chunk_size` zerlegt jede
  Antwort in mehrere Lesevorgänge und erreicht damit erstmals die Nachlese-Schleife in
  `_assemble_block()`; `float_block()` ist das Gegenstück zu `parse_float_block()`
- [x] Platzhalter für später: `SocketTransport` (VXI-11/Raw-Socket) und `VisaTransport`.
  Nicht bauen, nur die Fuge offenlassen — als auskommentierte Klassenrümpfe am Modulende
- [x] `WTSession` bekommt den Transport als `Transport`-Protokoll statt als konkrete Klasse
- [x] **Fertig, wenn:** die Testsuite eine vollständige Messschleife gegen `FakeTransport`
  durchspielt, inklusive Item-Tabelle und CSV — `tests/test_fake_transport.py`,
  23 Testfälle; Suite gesamt 151 statt 125

Bewusst offen geblieben, gehört nicht in diesen Schritt: `FakeSession` in
`tests/conftest.py` bleibt bestehen — die vorhandenen Tests der Fachmodule benutzen sie
und sollen hier nicht mitwandern. Der auskommentierte Originalblock am Ende von
`wt3000_core.py` ist beim nächsten Aufräumen ersatzlos zu löschen.

### M1-3 — Gerätesteckbrief statt harter Annahmen `M`
An mehreren Stellen steht heute „vier Elemente, 30-A-Module, V3A3,P1W2" fest im Code:
`DEFAULT_ELEMENTS`, `_elements_of("ALL") → (1,2,3,4)`, die Bereichstabellen.

- Dataclass `DeviceInfo`, beim Verbinden einmal erhoben und zwischengespeichert:
  Modell und Firmware aus `*IDN?`, Elementanzahl und Modultypen aus `:INPut:MODUle?`,
  vorhandene Optionen **(prüfen: eigener Knoten oder aus `*IDN?` ableitbar)**,
  Verdrahtung, Wiring-Units
- `RangeAccess` und `InputConfig` bekommen die Elementliste aus `DeviceInfo`, nicht aus
  einer Konstanten. `_elements_of("ALL")` liefert dann nur bestückte Elemente (Befund B-12)
- Bereichstabellen (`VOLTAGE_RANGES`, `CURRENT_RANGES`, `SENSOR_RANGES`) nach Modultyp
  auswählbar machen und mit einer klaren `WTError` statt `KeyError` quittieren (Befund B-09)
- Modellprüfung beim Verbinden: passt `*IDN?` nicht zu einem unterstützten Gerät, eine
  deutliche Warnung — kein Abbruch, aber protokolliert
- **Fertig, wenn:** der Treiber auf einem 3-Element-Gerät oder mit 2-A-Modulen ohne
  Codeänderung startet

### M1-4 — Sollzustand der Kommunikation herstellen statt nur prüfen `S`
Alle Stufenskripte prüfen `:COMMunicate:HEADer` und `:NUMeric:FORMat` und **brechen ab**,
wenn sie nicht stimmen. Für einen Treiber, den fremder Code aufruft, ist das zu wenig.

- Methode `wt.ensure_protocol_state()`: liest `HEADer`, `VERBose`, `:NUMeric:FORMat`,
  sichert den Ist-Zustand, setzt auf `HEADer 0` / `VERBose 0` / `FORMat FLOat`
- Rückstellung beim Verlassen des Context Managers — dieselbe Mechanik wie bei
  `applied_ranges()`
- In der `read_only`-Sitzung bleibt es beim Prüfen und Abbrechen, weil Schreiben dort
  ausgeschlossen ist. Die Fehlermeldung nennt dann den nötigen Handgriff
- **Fertig, wenn:** eine frisch bediente Frontplatte den Treiber nicht mehr ausbremst

### M1-5 — Fehlerpfade härten `S`
- `drain_after_failure()` tatsächlich aufrufen: in `WTSession.query()` bei
  `TmctlError`, und in `write_metadata()` nach jeder fehlgeschlagenen Abfrage (Befund B-04) —
  sonst verschiebt eine verspätete Antwort alle folgenden Werte
- Eigene Fehlerklasse `TimeoutError(WTError)`, damit „Gerät antwortet nicht" von
  „Gerät antwortet falsch" unterscheidbar wird
- `KeyError`/`ValueError` an den Tabellenzugriffen in `WTError` überführen (Befund B-09) —
  die Stufenskripte fangen nur `WTError`, alles andere reißt an der Wiederherstellung vorbei
- Bibliotheks-Logging: `logging.getLogger("wt3000").addHandler(logging.NullHandler())`
  im Paketkopf, damit der Treiber ohne Konfiguration still bleibt
- **Fertig, wenn:** ein simulierter Timeout mitten in der Messschleife die
  Wiederherstellung nicht verhindert

---

## M2 — Konfiguration lesen und einstellen

### M2-1 — Gerätekonfiguration: die fehlenden Kommandogruppen `L`
Das größte inhaltliche Loch. Heute deckt der Treiber `:INPut` und `:NUMeric` ab —
alles andere gar nicht.

Neues Modul `wt3000_deviceconfig.py` (Layer 2/3), aufgebaut wie `wt3000_input.py`:
Getter, Setter mit Rückleseprobe, Gruppensperre, Snapshot.

| Gruppe | Knoten | warum sie gebraucht wird |
|---|---|---|
| Kommunikation | `:COMMunicate:HEADer / VERBose / REMote / LOCKout` **(LOCKout prüfen)** | Sollzustand, Bedienfeldsperre |
| Averaging | `:MEASure:AVERaging:STATe / TYPE / COUNt` **(prüfen)** | verändert **jeden** Messwert — ohne diesen Wert ist eine Messreihe nicht interpretierbar |
| Frequenzmessquelle | in der `:MEASure`-Gruppe **(genauer Knoten prüfen)** | bestimmt, welche `FU`-Items überhaupt Werte liefern; heute im Standardprofil hart auf Element 3 angenommen |
| Oberschwingungen | `:HARMonics:*`, PLL-Quelle **(prüfen, Option /G6)** | Voraussetzung für THD/Ordnungsitems, die die Item-Tabelle bereits kennt |
| Integration | `:INTEGrate:MODE / TIMer / STARt / STOP / RESet` **(prüfen)** | Wh/Ah-Zählung, siehe M3-2 |
| Delta / Effizienz / Motor | `:MEASure:*` **(prüfen, optionsabhängig)** | nur erfassen und protokollieren, nicht setzen |
| Anzeige/System | Datum/Uhrzeit, Sprache, Bildschirm **(prüfen)** | nur lesen — für die Zuordnung Messdatei ↔ Gerätezeit |

Umsetzung:

- Für jede Gruppe zuerst **nur Lesen** bauen und im Snapshot ablegen. Das ist risikolos
  und liefert sofort den vollständigen Gerätesteckbrief für die Metadaten
- Schreiben nur dort ergänzen, wo es die fünf Zielfunktionen wirklich brauchen:
  Kommunikation, Averaging, Frequenzquelle, Integration. Anzeige und System bleiben lesend
- Gruppensperre wie in `wt3000_input`: neue `GROUP_*`-Konstanten, `DEFAULT_PROTECTED`
  um die eichungsnahen Gruppen erweitern
- Reihenfolge der Arbeit: Kommunikation → Averaging → Frequenzquelle → Integration →
  Rest. Nach jeder Gruppe ist das Ergebnis benutzbar
- **Fertig, wenn:** `DeviceSnapshot.capture()` einen vollständigen, wieder einspielbaren
  Gerätezustand liefert und `diff()` gegen einen früheren Stand vergleicht

### M2-2 — Setup-Speicher des Geräts nutzen `M · am Gerät`
Die robusteste Sicherung ist die, die das Gerät selbst führt.

- Prüfen, was das WT3000 anbietet: Setup-Speicherplätze über `*SAV`/`*RCL` **(prüfen)**
  oder Setup-Dateien über die `:FILE`-Gruppe **(prüfen)**
- Wenn vorhanden: `wt.save_setup(slot)` / `wt.load_setup(slot)` — ein Aufruf sichert
  bzw. stellt den *kompletten* Gerätezustand her, auch die Gruppen, die der Treiber
  gar nicht kennt
- Das ersetzt die feingliedrige Wiederherstellung nicht, sondern legt sich als Netz
  darunter: vor jeder schreibenden Sitzung ein Setup sichern, im Notfall zurückladen
- **Fertig, wenn:** es einen dokumentierten Weg gibt, ein versehentlich verstelltes
  Gerät mit einem Aufruf zurückzuholen

### M2-3 — Messkonfiguration vervollständigen `M`
`InputConfig` ist zu 75 % fertig. Was fehlt:

- `:INPut:INDependent` **setzen** können, nicht nur lesen — heute wird nur gewarnt,
  wenn es aus ist, und elementweise Bereichskommandos wirken dann gekoppelt
- Eingangsart umschalten (Direkteingang ↔ externer Stromsensor). Wird heute in
  `wt3000_ranging` bewusst abgelehnt. Als **ausdrückliche, eigens entsperrte** Methode
  nachrüsten, nicht als Nebenwirkung eines Bereichswechsels
- NULL-Funktion und Peak-Over-Rücksetzung **(Knoten prüfen)**
- `InputPlan` analog zu `RangePlan`: ein deklarativer Sollzustand für die **ganze**
  Eingangskonfiguration mit `validate()` vor dem ersten Set-Kommando. Heute gibt es
  Deklaratives nur für Bereiche; alles andere geht über `restore_input_snapshot()`,
  also nur „zurück auf früher", nicht „hin zu einem Ziel"
- **Fertig, wenn:** eine Messaufgabe als Datei beschrieben und mit einem Aufruf
  eingestellt werden kann

### M2-4 — Ein Backup-Format für alles `M`
Heute existieren drei getrennte Sicherungen in drei Formaten: Item-Tabelle
(`save_backup_bundle`), Bereiche (`RangeBackup`), Eingangskonfiguration
(`InputSnapshot`). Beim Wiederherstellen muss der Aufrufer alle drei kennen.

- Ein `SessionBackup` als Klammer: Gerätesteckbrief + Gerätekonfiguration +
  Eingangskonfiguration + Bereiche + Item-Tabelle + Tail, in **einer** JSON-Datei
- Versionsfeld im Kopf (`"format": 1`), damit ältere Dateien erkennbar bleiben —
  `RangeBackup.from_dict()` macht das mit `current_sensor` bereits richtig vor
- `wt.restore(backup)` stellt in der belegten Reihenfolge zurück: Crest → Verdrahtung →
  Bereiche → Auto-Range → Filter → Skalierung → Sync → Modus → Rate → Item-Tabelle
- Ein eigenes kleines Skript `restore_from_file.py`, das nichts tut außer: Datei laden,
  Zustand herstellen, Gegenprobe. Der Notfallknopf
- **Fertig, wenn:** ein Lauf, der mittendrin abgestürzt ist, aus einer einzigen Datei
  vollständig zurückgeholt werden kann

### M2-5 — Doppelte Regeln auf eine reduzieren `M`
Befund B-03. Voraussetzung dafür, dass eine dritte Konfigurationsgruppe (M2-1) nicht
eine vierte Kopie derselben Parser erzeugt.

- `wt3000_input` auf `wt3000_common` umstellen: `parse_bool` → `parse_boolean`,
  `parse_float` → `parse_nr3`, `_float_close` → `values_match`
- Der Sonderfall bleibt `strip_header` vs. `strip_response_header` — die beiden
  verhalten sich für dieselbe Eingabe **verschieden** (letztes Token gegen Schnitt am
  ersten Leerzeichen). Erst entscheiden, welches Verhalten das richtige ist, dann
  zusammenlegen. Ein Testfall mit einer echten verketteten Geräteantwort entscheidet das
- `target_node` und `scope_suffix` zusammenführen, inklusive der Frage, ob `'SIGM'`
  angenommen wird (heute: `scope_suffix` ja, `target_node` nein)
- **Fertig, wenn:** jede Normalisierungs- und Parserregel im Paket genau einmal existiert

---

## M3 — Messung starten und stoppen

### M3-1 — Aufzeichnung als steuerbares Objekt `M`
`run_measurement_loop()` ist eine blockierende Funktion mit `KeyboardInterrupt` als
einzigem Ausgang. Aus einer Anwendung heraus ist sie nicht benutzbar.

- Klasse `Measurement` in `wt3000_measure.py` mit `start()`, `stop()`, `is_running`,
  `wait(timeout)` und `statistics`
- Innen ein Hintergrund-Thread mit `threading.Event` als Stoppsignal — nicht als Flag,
  damit `stop()` sofort greift und nicht erst nach dem laufenden `sleep`
- Zweiter, einfacherer Weg für Skripte: ein Generator `wt.measure.stream()`, der
  Datensätze liefert und beim Verlassen der Schleife aufräumt. Deckt 90 % der Fälle ohne
  Thread ab
- Fehler im Thread nicht verschlucken: in einem Feld ablegen und bei `stop()`/`wait()`
  erneut auslösen, sonst endet ein Verbindungsabbruch in einer stillen Endlosschleife
- `KeyboardInterrupt` bleibt als sauberer Abbruch erhalten — das ist heute schon richtig gelöst
- Rückstellung (`HOLD OFF`, Item-Tabelle, Bereiche) muss auch bei `stop()` mitten im
  Zyklus greifen: `try/finally` im Thread, nicht im Aufrufer
- **Fertig, wenn:** eine Messung aus einem anderen Programmteil gestartet, nach 10 s
  gestoppt und das Ergebnis abgeholt werden kann

### M3-2 — Gerätesteuerung: Start/Stopp auf Geräteseite `M`
„Messung starten" hat zwei Bedeutungen. M3-1 ist die Aufzeichnung durch den Treiber;
dies hier ist die Steuerung des Geräts selbst — und fehlt vollständig.

- Integrator: `:INTEGrate:STARt / :STOP / :RESet`, Modus und Timer **(prüfen)**.
  Braucht eine Zustandsabfrage vorweg, damit `RESet` nicht eine laufende Integration
  verwirft — und einen ausdrücklichen Schutz gegen genau das
- Einzelmessung im HOLD-Betrieb: `:SINGle` **(prüfen)** — sauberer als das heutige
  „HOLD ON schickt und sofort lesen"
- `*OPC?` **(prüfen)** zur Synchronisation nach langsamen Set-Kommandos, statt fester
  Wartezeiten
- `*CLS` vor jedem Lauf, damit die Fehlerqueue nicht Reste des Vorlaufs meldet
- `*RST` **bewusst nicht** anbieten oder nur mit ausdrücklicher Entsperrung — es setzt
  die eingemessene Konfiguration zurück
- **Fertig, wenn:** eine Wh-Messung über eine definierte Dauer gestartet, beendet und
  ausgelesen werden kann

### M3-3 — Taktung am Gerät statt per `sleep` `M`
Abhängig vom Ergebnis aus M0-5.

- Bevorzugt: auf das Aktualisierungs-Ereignis des Geräts warten (Status-Register
  pollen, **prüfen**), statt im `:RATE`-Takt blind zu lesen
- Rückfallebene, wenn es kein Ereignis gibt: Dubletten erkennen. Ein Datensatz, dessen
  Werte bitgleich zum vorigen sind, bekommt eine Kennzeichnung in der Ausgabe statt
  stillschweigend als neuer Messpunkt zu erscheinen
- Die vorhandene driftfreie Taktung (`next_tick += interval`) und die
  Overrun-Zählung bleiben — sie sind richtig gebaut
- Zeitstempel weiterhin am `HOLD ON`-Moment festmachen, nicht am Antworteingang.
  Das ist heute schon korrekt und gehört im Docstring festgehalten
- **Fertig, wenn:** eine Messreihe über 10 Minuten keine unerkannten Wiederholungen enthält

### M3-4 — Verbindungsabbruch überleben `M`
Für Langzeitmessungen zwingend, heute gar nicht vorgesehen.

- Bei `TmctlError` im Lesezyklus: Zyklus als fehlend kennzeichnen, weiterlaufen,
  nach *n* Fehlversuchen die Verbindung neu aufbauen
- Nach dem Neuaufbau prüfen, ob Item-Tabelle und Bereiche noch dem Sollzustand
  entsprechen (`verify_item_table()`, `verify_plan()` gibt es bereits) — sonst
  neu setzen, bevor weiter aufgezeichnet wird
- Abbruchgrenze konfigurierbar, Voreinstellung eher konservativ
- Die Lücke muss in den Daten sichtbar sein: fehlende Zyklen als Zeile mit
  Statuskennzeichnung schreiben, nicht auslassen
- **Fertig, wenn:** ein gezogenes Netzwerkkabel die Messung nicht beendet und die
  Datei die Lücke ausweist

---

## M4 — Datenexport

### M4-1 — Datensatz-Objekt statt Parameterliste `S` — **umgesetzt 2026-08-20**
Bis hierher wanderte eine Messzeile als fünf getrennte Parameter in
`CsvRecorder.write_row()`. Jedes weitere Ausgabeformat hätte diese Signatur nachbauen
müssen.

- [x] Dataclass `Sample` (eingefroren): Zeitstempel, verstrichene Zeit, laufende Nummer,
  Condition-Register, `list[NumericValue]`, plus `mark` für die Kennzeichnung aus
  M3-3/M3-4. Dazu die Aufzählung `SampleMark` mit `OK`/`DUPLICATE`/`MISSING`
- [x] Alles, was misst, liefert `Sample`; alles, was schreibt, nimmt `Sample`.
  `CsvRecorder.write_row(...)` heißt jetzt `CsvRecorder.write(sample)` — derselbe Name,
  den das `SampleSink`-Protocol aus M4-2 tragen wird. Bewusst **keine** Weiterleitung
  unter dem alten Namen: die alte Signatur ist genau das, was dieser Punkt abschafft
- [x] `Sample.status_flags(columns)` als gemeinsame Grundlage jedes Ausgabeformats. Die
  Kennzeichnung des Zyklus wird in die vorhandene Spalte `status_flags` gefaltet — M3-3
  und M3-4 brauchen dadurch **kein** geändertes Dateiformat
- [x] **Fertig, wenn:** Messschleife und Export nur noch über `Sample` verbunden sind —
  `tests/test_sample.py`, 13 Testfälle; Suite gesamt 254 statt 241

Festgestellt und an M3-4 weitergereicht: ein `MISSING`-Datensatz trägt keine Messwerte
und bricht damit an der Längenprüfung aus P-3 ab. Dort ist zu entscheiden, ob solche
Zyklen mit `NO_DATA` aufgefüllt werden oder ob `write()` einen Sonderweg bekommt.

Siehe [AENDERUNGEN_2026-08-20_M4-1.md](AENDERUNGEN_2026-08-20_M4-1.md).

### M4-2 — Sink-Protokoll: CSV als eine Implementierung von mehreren `M` — **umgesetzt 2026-08-20**
Die vom Zielbild geforderte Erweiterbarkeit.

- [x] `typing.Protocol` namens `SampleSink` mit `open(columns, metadata)`, `write(sample)`,
  `close()` — bewusst klein gehalten. Es wohnt in `wt3000_measure.py` neben `Sample`:
  Datentyp und Vertrag sind ein Paar, und dadurch bleibt die Importrichtung eindeutig
- [x] Neues Modul `wt3000_sinks.py` mit `CsvSink` als erster Implementierung, aus dem
  bisherigen `CsvRecorder` hervorgegangen (Trennzeichen, Statuskodierung, Sofort-Flush
  unverändert). Neu ist die Aufteilung Konstruktor (Format) / `open()` (Spalten und
  Metadaten) — ohne sie kann formatunabhängiger Code keine Senke in Betrieb nehmen
- [x] Weitere Senken, ohne einen Eingriff in die Messschleife: `JsonlSink`,
  `CallbackSink`, `MultiSink`. **`ParquetSink` bewusst nicht** — das Paket hat heute
  `dependencies = []`, und Parquet braucht pyarrow oder fastparquet. Ob der Treiber
  eine erste Laufzeitabhängigkeit bekommt, ist eine eigene Entscheidung
- [x] Die Messschleife kennt nur `SampleSink`, nie ein konkretes Format. Sie öffnet und
  schließt die Senke selbst — die Spaltennamen stammen aus der Item-Tabelle, gegen die
  auch gemessen wird, und ein `finally` ist der einzige Ort, an dem sich `close()` auch
  bei Abbruch, Fehler und Strg+C zusagen lässt
- [x] Zeilenlängenfehler abfangen (Befund B-07): die Regel liegt jetzt als
  `require_matching_columns()` an **einer** Stelle und gilt für jede Senke, nicht nur
  für die CSV
- [x] **Fertig, wenn:** ein zweites Format ohne eine Zeile Änderung an der Messschleife
  ergänzt werden kann — `tests/test_sinks.py`, 25 Testfälle; Suite gesamt 282 statt 254

`MeasureControl.record()` nimmt jetzt eine beliebige Senke statt eines `csv_path`;
`record_csv()` bleibt der Einzeiler für den häufigsten Fall.

Siehe [AENDERUNGEN_2026-08-20_M4-2.md](AENDERUNGEN_2026-08-20_M4-2.md).

### M4-3 — Einheiten und Metadaten an die Daten binden `M`
Die aktuelle CSV enthält Zahlen ohne Einheit. Der Treiber weiß nicht, dass `U` in Volt
und `P` in Watt steht — das steht nirgends im Code.

- Tabelle `FUNCTION_UNITS` in `wt3000_numeric.py`: Funktionsname → Einheit
  (`U` → V, `I` → A, `P` → W, `S` → VA, `Q` → var, `LAMBDA` → dimensionslos,
  `PHI` → °, `FU`/`FI` → Hz, `WH` → Wh, `AH` → Ah, THD-Größen → %)
- Skalierung mitdenken: bei aktiver Skalierung (VT/CT/SFACtor) ist der Rohwert bereits
  umgerechnet — der Faktor gehört trotzdem in die Metadaten, sonst ist die Reihe später
  nicht nachvollziehbar (Element 4 hat CT = 2000)
- Zwei Kopfzeilen in der CSV (Name, Einheit) als Option, voreingestellt aus, damit
  bestehende Auswertungen weiterlaufen
- `write_metadata()` an den Sink koppeln, sodass Datei und Sidecar zwingend zusammen
  entstehen — heute sind das zwei unabhängige Aufrufe, und einer kann vergessen werden
- **Fertig, wenn:** eine Messdatei ohne Rückfrage beim Messenden interpretierbar ist

### M4-4 — Dateiverwaltung für lange Läufe `S`
- Rotation nach Zeilenzahl, Dateigröße oder Zeit (`wt3000_measurement_…_001.csv`)
- Fortsetzen einer abgebrochenen Reihe: Anhängen statt Überschreiben, wenn Kopf und
  Spalten übereinstimmen
- Zielverzeichnis, Namensschema und Trennzeichen aus der Konfiguration statt aus
  Modulkonstanten der Stufenskripte
- **Fertig, wenn:** eine Wochenmessung nicht in einer einzigen unhandlichen Datei endet

---

## M5 — Auslieferbarkeit

### M5-1 — Paket `S`
- `py.typed` ins Paket, sonst sind die Typannotationen für Anwender unsichtbar
- `pyproject.toml` ergänzen: Lizenz, Autoren, Klassifizierer, Projekt-URLs,
  `[project.optional-dependencies] dev` (pytest, ruff, mypy, pyflakes)
- `[project.scripts]` für die Kommandozeile, siehe M5-2
- Versionsstrang festlegen: `0.x` bleibt brechbar; die Schnittstellenänderung aus F-09
  gehört in einen `CHANGELOG.md`

### M5-2 — Kommandozeile `M`
Die fünf Stufenskripte sind Belege des Entwicklungswegs, keine Bedienoberfläche.
Parameter stehen als Modulkonstanten im Quelltext.

- Ein Einstiegspunkt `wt3000` mit Unterbefehlen:
  `info` (Steckbrief), `config show|save|load`, `measure` (Dauer, Rate, Ziel, Format),
  `restore <datei>`
- `argparse` genügt; Voreinstellungen aus Umgebungsvariablen (`WT3000_IP`,
  `WT3000_TMCTL_DLL`) mit den heutigen Werten als letzte Rückfallebene (Befund B-08)
- Die Stufenskripte bleiben als `examples/` erhalten — sie dokumentieren die
  Sicherungslogik besser als jede Prosa

### M5-3 — Doku `M`
- `README.md`: Installation, Verbindungsaufbau, drei Beispiele (lesen, konfigurieren,
  messen), und **prominent** das Sicherungskonzept — dass das Gerät eingemessen ist und
  welche Gruppen deshalb gesperrt bleiben
- Ein Dokument „Gerätezustand und Wiederherstellung": was der Treiber anfasst, was er
  sichert, wie man von Hand zurückholt
- Die `ZU VERIFIZIEREN`-Vermerke aus dem Code, sobald sie geklärt sind, in Feststellungen
  überführen — mit Datum und Beleg

### M5-4 — Prüfwerkzeuge `S`
- `ruff` und `mypy --strict` in die Entwicklungsabhängigkeiten; die Typannotationen sind
  bereits durchgängig vorhanden, der Aufwand ist deshalb gering
- CI (GitHub Actions o. ä.): pytest, ruff, mypy bei jedem Commit
- Testabdeckung messen und die Fachmodule bei mindestens 80 % halten
- Zeilenenden vereinheitlichen (`.gitattributes`, `* text=auto eol=lf`) — als eigener
  Commit ohne inhaltliche Änderung, sonst verdeckt er alles andere

---

## 3 — Vorgeschlagene Zielarchitektur

Die heutige Schichtung trägt und bleibt. Neue Module fügen sich ein, ohne die
Importrichtung zu drehen:

```
Layer 0   wt3000_transport   Protocol 'Transport'          NEU  (M1-2)
          └ TmctlTransport (aus wt3000_core), FakeTransport, später Socket/VISA

Layer 1   wt3000_core        WTSession, Fehlerklassen, WTConfig
          wt3000_common      Scope-/Parserregeln, setup_logging

Layer 2   wt3000_numeric     :NUMeric  + Einheitentabelle          (M4-3)
          wt3000_rangeio     :INPut-Bereichsknoten
          wt3000_input       übrige :INPut-Stellgrößen
          wt3000_deviceconfig  :COMMunicate/:MEASure/:INTEGrate/…  NEU  (M2-1)

Layer 3   wt3000_itemspec    Ablauf Item-Tabelle
          wt3000_ranging     Ablauf Messbereiche
          wt3000_measure     Measurement, Sample, Taktung          (M3)
          wt3000_backup      SessionBackup über alle Gruppen       NEU  (M2-4)

Layer 4   wt3000_export      SampleSink, CsvSink, JsonlSink …      NEU  (M4-2)
          wt3000_device      Fassade WT3000                        NEU  (M1-1)

Layer 5   cli.py             Unterbefehle                          NEU  (M5-2)
          examples/          die heutigen Stufenskripte
```

`tests/test_package_layout.py` prüft diese Richtung bereits mit `ast` — die
`LAYERS`-Tabelle dort ist bei jedem neuen Modul mitzuführen. Das ist kein Zusatzaufwand,
sondern die Absicherung, dass die Schichtung nicht wieder aufweicht.

---

## 4 — Reihenfolge und Abhängigkeiten

```
M0-1 ─┬─> M2-3 ──> M2-4 ──> M3-4
M0-2 ─┘
M0-3 ────> M1-4
M0-4 ────> M1-3 ──> M2-1 ──> M2-2
M0-5 ────> M3-3

M1-2 ──> M1-1 ──> alles Weitere
M2-5 ──> M2-1        (sonst entsteht eine vierte Kopie derselben Parser)
M4-1 ──> M4-2 ──> M4-3 ──> M4-4
M3-1 ──> M3-2
```

**Empfohlener Einstieg**, wenn schnell etwas Benutzbares entstehen soll:

1. **M1-2 + M1-1** — Transport-Protokoll und Fassade. Danach ist der Treiber zum
   ersten Mal von außen benutzbar, und alles Weitere lässt sich gerätefrei testen.
2. **M0** komplett — ein Messtermin, der vier offene Annahmen zu Feststellungen macht.
3. ~~**M4-1 + M4-2** — Export entkoppeln.~~ Erledigt: jedes weitere Format ist ab jetzt
   eine Klasse in `wt3000_sinks.py` statt eines Eingriffs in die Messschleife.
4. **M3-1** — Messung steuerbar machen. Ab hier ist das Zielbild in Grundzügen erfüllt.
5. **M2-1** — die fehlenden Gerätegruppen, gruppenweise, in der genannten Reihenfolge.

---

## 5 — Bewusst nicht auf der Roadmap

Damit der Umfang nicht ausufert — jeweils mit der Bedingung, unter der es doch
hereinkäme:

| Nicht enthalten | Begründung / Bedingung |
|---|---|
| Grafische Oberfläche | Der Treiber ist eine Bibliothek. Eine Anzeige setzt auf `CallbackSink` (M4-2) auf und ist ein eigenes Projekt |
| Wellenform-/Rohdatenerfassung | Andere Kommandogruppe, andere Datenmengen, anderer Zweck. Erst wenn eine Messaufgabe es verlangt |
| Weitere Yokogawa-Modelle (WT1800, WT5000) | Erst sinnvoll, wenn M1-3 steht — dann ist der Steckbrief die Stelle, an der ein zweites Modell andockt |
| VISA- statt TMCTL-Transport | Fuge wird in M1-2 offengehalten, gebaut wird es nur bei Bedarf |
| Asynchrone Schnittstelle (`asyncio`) | Der Flaschenhals sind Set-Kommandos mit 100–250 ms am Gerät, nicht die Nebenläufigkeit im Programm. Threads (M3-1) reichen |
| Automatische Kalibrierprüfung | Berührt die Eichung. Gehört, wenn überhaupt, in ein getrenntes Werkzeug mit eigener Freigabe |

---

## 6 — Zusammenfassung in einem Absatz

Der Unterbau des Treibers ist tragfähig: Transport, Protokollregeln, Zahlenformate,
Item-Tabelle und die gesamte `:INPut`-Gruppe sind gebaut, abgesichert und gerätefrei
getestet. Was zur vollen Inbetriebnahme fehlt, ist erstens eine **Schnittstelle**
(Fassade, Transport-Protokoll, Kommandozeile), zweitens die **Gerätekonfiguration
jenseits von `:INPut`** (Averaging, Frequenzquelle, Integration, Oberschwingungen),
drittens eine **steuerbare Messung** statt einer blockierenden Schleife und viertens
ein **austauschbarer Export** mit Einheiten. Vorgelagert sind fünf Fragen, die sich nur
am Gerät klären lassen — allen voran die Parametersyntax der Bereichsknoten, an der
heute zwei Module mit verschiedener Annahme hängen.
