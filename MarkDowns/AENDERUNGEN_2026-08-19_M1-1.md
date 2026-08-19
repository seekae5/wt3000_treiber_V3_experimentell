# M1-1 — Fassade `WT3000`: Umsetzung und Erkenntnisse

**Datum:** 2026-08-19
**Bezug:** [ROADMAP.md](ROADMAP.md) M1-1 · [AENDERUNGEN_2026-08-18.md](AENDERUNGEN_2026-08-18.md) (Befunde B-01…B-15)
**Stand vorher:** 151 Tests grün · **Stand nachher:** 176 Tests grün, 0,45 s, weiterhin ohne Gerät und ohne `tmctl.dll`

---

## 1 — Was umgesetzt wurde

Neues Modul [wt3000_device.py](src/wt3000_scpi/wt3000_device.py) (Layer 4, 763 Zeilen) mit vier
Klassen. Es ist ab jetzt der einzige Einstiegspunkt, den ein Anwender braucht:

```python
from wt3000_scpi import WT3000, Quantity

with WT3000.connect(ip="192.168.10.20") as wt:
    wt.check_protocol_state()
    wt.device.log_summary()
    print(wt.ranges.get_range(Quantity.VOLTAGE, 1).describe(Quantity.VOLTAGE))
```

| Klasse | Zweck |
|---|---|
| `WT3000` | Fassade: Verbindung, Steckbrief, Eigenschaften `input`/`ranges`/`items`/`measure`/`device`, Context Manager |
| `DeviceInfo` | Was beim Verbinden einmalig erhoben wird: `*IDN?`, Verdrahtung, Wiring-Units, Modultypen, bestückte Elemente, Scope-Abbildung |
| `ItemAccess` | Bindet die freien Ablauffunktionen aus `wt3000_itemspec` an eine Sitzung, plus `applied()` als Context Manager |
| `MeasureControl` | Messwerte lesen (`read_values`, `read_mapped`), HOLD, Aufzeichnung nach CSV |

**Drei Konstruktionswege.** `connect()` für den Normalfall, `from_config()` für eine
fertige `WTConfig`, und — über die Roadmap hinaus — `from_transport()` für einen bereits
bestehenden Transport. Der dritte ist der Grund, warum diese Fassade überhaupt prüfbar
ist: mit `FakeTransport` aus M1-2 läuft sie ohne Gerät, und zwar mit echter `WTSession`,
echtem Blockparser und echter Fehlerqueue darunter.

**Zwei Schlösser, unverändert.** `read_only=True` und `allow_changes=False` sind beide
Voreinstellung. Wer messen und nichts verändern will — der Normalfall — fasst keinen
der beiden Schalter an. Die Kombination `read_only=True, allow_changes=True` wird beim
Konstruieren als Widerspruch abgewiesen, statt später beim ersten Set-Kommando
aufzufallen. Die Gruppen aus `DEFAULT_PROTECTED` bleiben auch bei `allow_changes=True`
gesperrt und brauchen weiter `wt.input.unlocked(...)`.

**Was `close()` tut**, in dieser Reihenfolge und jeder Schritt in seinem eigenen `try`:
`:NUMeric:HOLD OFF` (nur in einer Schreibsitzung), `:COMMunicate:REMote OFF`, Transport
schließen (nur wenn die Fassade ihn selbst geöffnet hat). Ein misslungener Schritt darf
die folgenden nicht überspringen — ein hängengebliebenes HOLD ist der unangenehmste
Rest, den eine abgebrochene Sitzung hinterlässt: das Gerät liefert in der nächsten
Sitzung eingefrorene Werte, während die Anzeige weiterläuft.

**Geänderte Bestandsdateien:**

| Datei | Änderung |
|---|---|
| [`__init__.py`](src/wt3000_scpi/__init__.py) | exportiert `WT3000`, `WTConfig`, alle acht Fehlerklassen, die Aufzählungen; `wt3000_device` in `MODULES` |
| [`wt3000_input.py`](src/wt3000_scpi/wt3000_input.py) | neu: `InputConfig.get_modules()` — 13 Zeilen, benutzt den vorhandenen Cache |
| [`test_package_layout.py`](tests/test_package_layout.py) | `LAYERS`-Eintrag für `wt3000_device` |
| [`test_device_facade.py`](tests/test_device_facade.py) | neu, 23 Testfälle |

---

## 2 — Erkenntnisse aus der Umsetzung

### 2.1 Der eigentliche Gewinn ist die Verdrahtung der Wiring-Units, nicht die Bequemlichkeit

Das Argument für M1-1 lautete „weniger Zeilen für den Anwender". Beim Bauen zeigte sich
ein handfesteres: **die manuelle Verdrahtung war nicht nur lästig, sie fehlte.**

`RangeAccess` ohne `sigma_members` lehnt jeden SIGMA-Scope ab — richtig so, geraten wird
in diesem Treiber nichts. Nur legt [stage5b_range_probe.py:96](src/wt3000_scpi/stage5b_range_probe.py:96)
genau so ein Objekt an:

```python
writable = RangeAccess(session, allow_changes=True)   # ohne sigma_members
```

Solange nur elementweise gearbeitet wird, fällt das nicht auf. Der erste SIGMA-Scope
läuft in einen Fehler — mitten im Ablauf, nach dem Schreiben der Bereiche. Über die
Fassade kann das nicht mehr passieren: `DeviceInfo.read()` erhebt die Zuordnung einmal
beim Verbinden, und `wt.ranges` bekommt sie ohne Zutun des Aufrufers. Der Test dafür ist
`test_wiring_units_sind_ohne_zutun_verdrahtet` und prüft gleich mit, dass die strikte
Scope-Regel erhalten bleibt: `SIGM` → `(1,2,3)`, `SIGMB` → `(4,)`, kein Präfixmatching.

### 2.2 `wt.items` und `wt.measure` brauchten neue Klassen — das war nicht absehbar

`wt.input` und `wt.ranges` sind Weiterreichungen: `InputConfig` und `RangeAccess`
existieren als Klassen. `wt3000_itemspec` und `wt3000_measure` bestehen dagegen aus
**freien Funktionen mit `session` als erstem Parameter**. Es gab dort schlicht kein
Objekt, das eine Eigenschaft hätte liefern können.

Das ist kein Mangel dieser Module — für einen Ablauf ist eine freie Funktion die
ehrlichere Form. Aber es heißt, dass `ItemAccess` und `MeasureControl` neu entstehen
mussten. Beide sind bewusst dünn geblieben: sie halten die Sitzung und rufen die
vorhandenen Funktionen auf. Kein Ablauf ist in die Fassade gewandert, denn dort wäre er
nicht mehr da, wo er getestet ist.

### 2.3 `ItemAccess.applied()` schließt eine Lücke, die im Vergleich zu `applied_ranges()` auffiel

`wt3000_ranging` hat mit `applied_ranges()` einen Context Manager, der den ganzen Ablauf
kapselt: sichern, Schreibprobe, anwenden, verifizieren, Nutzblock, wiederherstellen,
Gegenprobe. Für die **Item-Tabelle gab es das nicht** — Stufe 3 und Stufe 4 bauen
denselben `try/finally` jeweils von Hand nach, rund 40 Zeilen pro Skript, in zwei
Fassungen. Beim Anbinden von `wt.items` fiel die Asymmetrie auf.

`ItemAccess.applied()` ist das Gegenstück. Der Test
`test_applied_stellt_auch_nach_einem_fehler_zurueck` weist nach, dass die
Wiederherstellung auch bei einem Fehler im Nutzblock läuft — das ist der Fall, für den
der `finally` da ist, und er war bisher in keinem Test.

### 2.4 Ein Geräte­modell im Test ist unverzichtbar, sobald es um Wiederherstellung geht

`FakeTransport` beantwortet Kommandos aus einer Tabelle und **merkt sich nichts**. Für
Parser reicht das. Für die Item-Tabelle nicht: Schreiben, Verifizieren und
Wiederherstellen sind erst dann eine Aussage, wenn eine Abfrage zeigt, was ein
vorheriges Schreiben bewirkt hat.

`ItemTableTransport` in [test_device_facade.py](tests/test_device_facade.py) ist deshalb
eine 40-Zeilen-Ableitung von `FakeTransport`, die `ITEM<n>`- und `NUMber`-Kommandos
übernimmt und die Abfragen daraus beantwortet. Damit läuft der vollständige Kreis durch:
Backup lesen → Tail sichern → Schreibprobe → anwenden → verifizieren → Nutzblock →
zurückstellen → Gegenprobe. **Empfehlung:** dieses Modell gehört bei nächster Gelegenheit
nach `wt3000_transport.py` neben `FakeTransport`, sobald ein zweiter Test es braucht —
heute wäre es dort ungenutzter Vorrat.

### 2.5 `:COMMunicate:REMote ON` ist in einer Nur-Lesen-Sitzung nicht sendbar

Eine Kleinigkeit mit Folgen für die Voreinstellung: `WTConfig.use_remote` steht auf
`True`, `REMote ON` ist aber selbst ein Set-Kommando und scheitert in einer
`read_only`-Sitzung an der eigenen Sperre. Die Fassade schaltet die Fernsteuerung
deshalb **nur in einer Schreibsitzung** ein und protokolliert das sonst.

Dieselbe Überlegung bei HOLD: `wt.measure.hold()` und `record()` schalten HOLD in einer
Nur-Lesen-Sitzung ab und warnen, statt einen Fehler zu werfen. Die Werte sind dann
ungefroren — der Zeitstempel wird unschärfer, die Messung bleibt gültig. Rein lesend zu
messen ist ein normaler Fall und darf nicht am Zeitstempel-Anker scheitern.

### 2.6 Das `__init__.py`-Argument trug nicht mehr

Der Modulkopf begründete, dass die Paketwurzel *bewusst nichts* importiert: ein Rechner
ohne Gerät und ohne `tmctl.dll` soll das Paket importieren können. Der Grund ist richtig,
das Mittel war es nicht mehr — die Eigenschaft hängt daran, dass **kein Fachmodul beim
Import etwas voraussetzt** (`TmctlTransport` lädt die DLL erst bei Instanziierung), und
genau das hält `test_package_layout.py` seit Punkt 4 fest. Die Wurzel kann also
exportieren, ohne die Eigenschaft zu verlieren. Gegenprobe:
`tools_import_check.py` läuft unverändert durch, jetzt über 10 statt 9 Module.

### 2.7 Ein halber Schritt Richtung M1-3 war unvermeidlich

Die Fassade muss festlegen, welche Elemente `RangeAccess` bekommt — sie kann die Frage
nicht offenlassen. Deshalb liest `DeviceInfo` `:INPut:MODUle?` und übergibt die
**bestückten** Elemente. Auf einem 3-Element-Gerät liefert `wt.ranges.expand_scope("ALL")`
damit `(1, 2, 3)` statt der Konstanten `(1, 2, 3, 4)`.

Damit dafür nicht die vierte Fassung desselben Parsers entsteht (Befund B-03), bekam
`InputConfig` die Methode `get_modules()` — 13 Zeilen auf dem vorhandenen Cache. Das ist
die **einzige** Änderung an einem bestehenden Fachmodul in diesem Schritt.

Ausdrücklich **nicht** mit erledigt: `InputConfig._elements_of("ALL")` liefert weiterhin
fest `(1,2,3,4)` (B-12), und die Bereichstabellen wählen weiterhin nicht nach Modultyp
(B-09). Beides bleibt M1-3. Auf dem vorliegenden 4-Element-Gerät fällt der Unterschied
nicht auf — auf einem 3-Element-Gerät wäre er ein Widerspruch zwischen `wt.ranges` und
`wt.input`. **Das ist der wichtigste offene Punkt aus dieser Änderung.**

---

## 3 — Bewusst nicht mit erledigt

| Punkt | Grund |
|---|---|
| **M1-4** Sollzustand *herstellen* | `wt.check_protocol_state()` prüft `HEADer`/`FORMat` und bricht ab. Das Herstellen samt Rückstellung beim Verlassen ist ein eigener Meilenstein und braucht dieselbe Mechanik wie `applied_ranges()` |
| **B-14** vier Fassungen von `check_preconditions()` | Die Fassade ist der designierte Ort, an dem die drei Stufen­kopien aufgehen sollen — aber die Stufenskripte anzufassen, ohne sie am Gerät nachprüfen zu können, wäre eine Änderung ohne Absicherung. Der gemeinsame Kern (`HEADer` + `FORMat` + Condition-Bits) liegt jetzt einmal in `check_protocol_state()` |
| **B-04** `drain_after_failure()` | Gehört in `WTSession.query()`, nicht in die Fassade. M1-5 |
| **B-08** `dll_path` auf einen fremden Pfad | `connect(dll_path=...)` macht ihn jetzt überschreibbar, ohne `WTConfig` anzufassen. Die Voreinstellung selbst zu ändern ist eine Entscheidung des Aufbau­verantwortlichen |
| **M3-1** steuerbare Messung | `wt.measure.record()` macht die Schleife erreichbar, nicht steuerbar. Sie blockiert weiterhin und bricht nur über Strg+C oder ein Limit ab |
| Stufenskripte auf die Fassade umstellen | Sie sind der einzige am Gerät erprobte Pfad. Sie bleiben unverändert und sind ab jetzt Beispiele für den Weg *ohne* Fassade |

---

## 4 — Prüfung

```
pytest                     176 passed in 0.45s
python tools_import_check.py   wt3000_scpi 0.3.0: 10 Module importierbar
pyflakes src/ tests/           keine Meldung
```

Die Schichtprüfung greift für das neue Modul mit: `wt3000_device` steht in `LAYERS`
und darf aus allen Schichten darunter importieren — aus keinem Stufenskript und aus
keinem zweiten Layer-4-Modul. Damit ist festgehalten, dass die Fassade die Fachmodule
**bündelt** und sie nicht um eigene Gerätekenntnis ergänzt.

Was die 23 Testfälle abdecken: Steckbrief inkl. unbestückter Elemente und
fehlgeschlagenem `*IDN?`, Verdrahtung der Wiring-Units, beide Schlösser einzeln und in
Kombination, REMote in beiden Sitzungsarten, `close()` mehrfach und nach einem Fehler im
Block, Transport-Eigentum, Protokollzustand in vier Varianten, Condition-Bits,
Werteabbildung, HOLD in der Nur-Lesen-Sitzung, und der vollständige
`applied()`-Kreis inklusive Wiederherstellung nach einem Fehler.

**Nicht getestet, weil nur am Gerät prüfbar:** `connect()`/`from_config()` mit echter
TMCTL-DLL, das tatsächliche Verhalten von `:COMMunicate:REMote` und die Frage, ob
`:INPut:MODUle?` für ein unbestücktes Element wirklich `0` meldet (Annahme aus dem
Docstring von `get_module()`, im Code als solche gekennzeichnet).

---

## 5 — Empfohlene Reihenfolge danach

1. **`pip install -e ".[test]"`** in eine funktionierende Umgebung. Das Projekt-`venv/`
   ist leer, `pytest` ist auf keinem Interpreter des Rechners installiert — die 176
   Tests laufen zurzeit nur in einer eigens gebauten Umgebung. Solange das so bleibt,
   ist die Absicherung nur nominell vorhanden.
2. **M1-3** — `DeviceInfo` zu Ende führen, damit `wt.input` und `wt.ranges` dieselbe
   Elementliste benutzen (Abschnitt 2.7, Befunde B-12 und B-09).
3. **B-03** auflösen — `wt3000_input` auf `wt3000_common` umstellen; B-13/B-14 gleich
   mitnehmen. Danach gibt es jede Regel nur noch einmal.
4. **M1-4 und M1-5** — Sollzustand herstellen, `drain_after_failure()` aufrufen,
   Tabellenzugriffe in `WTError` überführen.
5. Beim nächsten Aufräumen: den auskommentierten Layer-0-Block am Ende von
   [wt3000_core.py](src/wt3000_scpi/wt3000_core.py) löschen (rund 170 von 376 Zeilen —
   git hält die Herkunft fest), und `.gitattributes` für einheitliche Zeilenenden
   nachziehen.
