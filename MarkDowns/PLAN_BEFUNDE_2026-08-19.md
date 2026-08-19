# Bewertung der Befunde und Umsetzungsplan

**Datum:** 2026-08-19
**Grundlage:** [Befund.md](Befund.md)
**Geprüfter Stand:** Commit `2f51b19`, `wt3000-scpi 0.3.0`, 176 Tests grün, `pyflakes` ohne Meldung
**Verwandte Dokumente:** [AENDERUNGEN_2026-08-18.md](AENDERUNGEN_2026-08-18.md) · [ROADMAP.md](ROADMAP.md)

Jeder Befund wurde gegen den tatsächlichen Quelltext geprüft, nicht gegen die
Beschreibung. Es wurde kein Code geändert.

---

## 1 — Bewertung auf einen Blick

| Nr. | Befund | Prüfergebnis | Priorität nach Prüfung | Maßnahme |
|-----|--------|--------------|------------------------|----------|
| BF-H1 | REMOTE bleibt nach fehlgeschlagener Initialisierung aktiv | **bestätigt, verschärft** | **hoch** | [P-1](#p-1) ✅ umgesetzt |
| BF-H2 | Restore-Fehler der Item-Tabelle wird unterdrückt | **bestätigt** | **hoch** | [P-2](#p-2) ✅ umgesetzt |
| BF-H3 | Abweichende Messwertanzahl verschiebt die CSV-Struktur | **bestätigt** | **hoch** | [P-3](#p-3) ✅ umgesetzt |
| BF-H4 | Schreibende Voreinstellung in Stufe 5b | bestätigt, aber **Zielrichtung falsch** | mittel | [P-5](#p-5) ✅ umgesetzt |
| BF-M1 | Keine reproduzierbare Installation, keine README | **überwiegend falsch** | niedrig (Restanteil) | [P-8](#p-8) ✅ umgesetzt |
| BF-M2 | Verbindungsdaten als Quellcode-Defaults | **bestätigt** | mittel | [P-7](#p-7) ✅ umgesetzt |
| BF-M3 | Blockheader-Fehler nicht einheitlich übersetzt | **bestätigt** | mittel | [P-4](#p-4) ✅ umgesetzt |
| BF-N1 | Doku und Implementierung auseinandergelaufen | **teils überholt**, teils Dublette | niedrig | [P-8](#p-8) ✅ umgesetzt |
| Z-1 | *(fehlt in Befund.md)* `from_transport()` hat dieselbe REMOTE-Lücke | neu | **hoch** | [P-1](#p-1) ✅ umgesetzt |
| Z-2 | *(fehlt in Befund.md)* schreibendes Geräteskript liegt in `tests/` | neu | mittel | [P-6](#p-6) ✅ umgesetzt |

**Kurzurteil:** Sechs von acht Befunden treffen zu, drei davon sind ernst und
klein zu beheben. Einer (BF-M1) ist gegen einen veralteten oder unvollständigen
Projektstand geschrieben und trifft heute nicht mehr zu. Einer (BF-H4) beschreibt
das Problem richtig, schlägt aber die falsche Lösung vor.

---

## 2 — Bewertung im Einzelnen

### BF-H1 — REMOTE bleibt nach fehlgeschlagener Initialisierung aktiv
**Urteil: bestätigt, und die Lage ist ernster als beschrieben.**

Prüfung: In `WT3000.__init__()` (`wt3000_device.py:483–495`) wird
`self._session.enable_remote()` gesendet, unmittelbar danach folgt
`DeviceInfo.read(self._session)`. Scheitert eine der dort abgesetzten Abfragen,
verlässt die Ausnahme den Konstruktor. `from_config()` (`:539–554`) fängt sie mit
`except BaseException`, ruft `transport.close()` und löst erneut aus. Ein
`disable_remote()` findet an keiner Stelle statt.

Der Kommentar im Ausnahmepfad behauptet ausdrücklich das Gegenteil:
*„Ohne dieses except bliebe die Verbindung offen und das Geraet je nach Zeitpunkt
in Fernsteuerung stehen."* Der Kommentar beschreibt die Absicht, der Code setzt
nur die halbe Absicht um.

Drei Punkte, die in Befund.md fehlen und das Gewicht erhöhen:

- **`use_remote` steht inzwischen auf `True`** (`wt3000_transport.py:75`). Als der
  Kommentar geschrieben wurde, war die Voreinstellung `False` und der Pfad
  theoretisch. Heute ist er der Normalfall jeder schreibenden Sitzung.
- **`from_transport()` hat dieselbe Lücke, sogar ohne jede Aufräumarbeit**
  (`wt3000_device.py:557–577`, Befund Z-1). Da dort `owns_transport=False` gilt,
  wird nicht einmal der Transport geschlossen. Eine Reparatur nur in
  `from_config()` würde die zweite Tür offen lassen.
- **Die direkte Konstruktion `WT3000(transport, …)` ist ebenfalls betroffen** und
  ist ein dokumentierter Weg.

`WT3000.close()` (`:722–751`) ist im Übrigen vorbildlich gebaut — jeder Schritt in
eigenem `try`, HOLD vor REMote vor Transport. Die Lücke betrifft ausschließlich den
Fall, dass gar kein Objekt entsteht, `close()` also nie erreichbar wird.

### BF-H2 — Restore-Fehler der Item-Tabelle wird unterdrückt
**Urteil: bestätigt.**

Prüfung: `ItemAccess.applied()` (`wt3000_device.py:293–330`) führt den Restore im
`finally` aus und fängt `WTError` ausschließlich zum Protokollieren ab. Kein
erneutes Auslösen, kein Rückgabeobjekt, kein Statusfeld. Der Docstring verspricht
*„Ausgangszustand garantiert zurueck"*.

Das stärkste Argument liefert das Projekt selbst: `applied_ranges()` in
`wt3000_ranging.py:636–641` löst in derselben Situation erneut aus
(`_log.error(...)` gefolgt von `raise`). Zwei Kontextmanager mit demselben Zweck,
derselben Struktur und **verschiedenem** Verhalten im Fehlerfall — und der
schwächere ist der neuere. Das ist keine Auslegungsfrage, sondern eine
Unstimmigkeit innerhalb einer Codebasis.

Der Zusatz in Befund.md, beide Fehler zu erhalten, ist richtig und in Python ohne
Zusatzaufwand zu haben: eine Ausnahme, die in einem `finally` ausgelöst wird,
während eine andere unterwegs ist, hängt die ursprüngliche automatisch als
`__context__` an und zeigt sie im Traceback.

### BF-H3 — Abweichende Messwertanzahl verschiebt die CSV-Struktur
**Urteil: bestätigt.** Deckungsgleich mit Befund B-07 aus
[AENDERUNGEN_2026-08-18.md](AENDERUNGEN_2026-08-18.md), dort bewusst offen gelassen,
weil `tests/test_numeric_parser.py` das heutige Verhalten ausdrücklich festhält.

Prüfung: `read_numeric_values()` (`wt3000_numeric.py:284–290`) protokolliert eine
Abweichung nur als Warnung. `CsvRecorder.write_row()` (`wt3000_measure.py:154–179`)
baut die Zeile aus vier festen Feldern, `len(values)` Wertzellen und einer
Flag-Spalte — ohne Abgleich mit `len(self._columns)`.

Die beschriebene Folge stimmt: bei zu wenigen Werten rutscht `status_flags` unter
eine Messwertspalte, bei zu vielen entstehen unbenannte Spalten. Beides fällt beim
Sichten der Datei nicht auf, weil jede Zeile für sich plausibel aussieht — die
Verschiebung zeigt sich erst gegen den Kopf.

Die Einschätzung „für metrologische Daten ist ein Abbruch die sicherere
Voreinstellung" teile ich uneingeschränkt. Eine stillschweigend verrutschte Spalte
ist der teuerste Fehler in dieser Codebasis, weil er die Daten überlebt.

**Anmerkung zur Festlegung:** `tests/test_numeric_parser.py::test_zu_wenige_werte_
werden_gemeldet` hält das heutige Verhalten von `map_values()` fest und erklärt
ausdrücklich, dass ein späterer harter Abbruch genau dort anschlagen soll. Der
Test ist also kein Hindernis, sondern der vorgesehene Anschlagpunkt — er ist im
Zuge der Änderung mitzuziehen.

### BF-H4 — Schreibende Voreinstellung in Stufe 5b
**Urteil: Problem bestätigt, vorgeschlagene Lösung falsch herum.**

Prüfung: `stage5b_range_probe.py:45` steht auf
`ENABLE_NOOP_WRITE_PROBE: bool = True`. Der Dateikopf (`:6–8`) sagt weiterhin
*„Voreinstellung: dieses Skript SCHREIBT NICHTS."* Der Widerspruch besteht.

Was Befund.md übersieht: unmittelbar hinter der Zeile steht ein Kommentar des
Bearbeiters — *„muss derzeit noch auf True stehen um Änderungen zuzulassen /
-> Modifizierbar machen"*. Die Umstellung war also eine bewusste Entscheidung, und
der offene Punkt ist bereits richtig benannt.

Damit ist die Zielrichtung „Default auf `False` setzen" die schlechtere von zwei
Möglichkeiten: sie nimmt dem Bearbeiter genau die Fähigkeit weg, die er für die
offenen Gerätefragen M0-1 bis M0-3 der [ROADMAP.md](ROADMAP.md) braucht, und
provoziert, dass die Zeile beim nächsten Mal wieder von Hand umgestellt wird.
Richtig ist der zweite Teil des Vorschlags: **Laufzeitparameter statt
Modulkonstante**. Dann ist die Voreinstellung wieder rein lesend, und das Schreiben
verlangt eine sichtbare, bewusste Handlung beim Aufruf.

Priorität deshalb **mittel** statt hoch: das Skript wird nicht versehentlich
gestartet, es wird gezielt für Schreibproben benutzt.

### BF-M1 — Keine reproduzierbare Installation, keine README
**Urteil: überwiegend falsch. Der Befund ist gegen einen unvollständigen
Projektstand geschrieben.**

Prüfung Punkt für Punkt:

| Behauptung | Tatsächlich |
|---|---|
| „Es fehlen `pyproject.toml` … und eine README" | Beide vorhanden. `pyproject.toml` (562 B) und `README.md` (10,5 kB) liegen im Projektstamm |
| „Die erforderliche Python-Version ist nicht maschinenlesbar dokumentiert" | `requires-python = ">=3.10"` steht in `pyproject.toml`; `pip` setzt das durch. Die README nennt es in Zeile 6 |
| „`src` muss manuell über `PYTHONPATH` verfügbar gemacht werden" | `[tool.hatch.build.targets.wheel] packages = ["src/wt3000_scpi"]` ist gesetzt; `pip install -e ".[test]"` steht in der README. Zusätzlich legt `tests/conftest.py` `src/` in den Suchpfad, damit die Suite auch ohne Installation läuft |
| „Test- und Entwicklungsabhängigkeiten sind nicht reproduzierbar" | **teilweise zutreffend** — `[project.optional-dependencies] test = ["pytest>=8.0"]` existiert, eine `dev`-Gruppe für `ruff`/`mypy`/`pyflakes` fehlt |
| „Es gibt keinen standardisierten Installations- oder Testbefehl" | README, Abschnitt *Installation* und *Tests*; `[tool.pytest.ini_options]` mit `testpaths` ist gesetzt |
| „Unter Python 3.9 scheitert bereits der Import in `wt3000_transport.py`" | **zutreffend und nachgestellt.** `FakeReply = bytes | str` (`:290`) ist ein Laufzeit-Typalias, kein Annotationsausdruck, und wirft unter 3.9 `TypeError`. Das ist aber genau der Grund für `requires-python`, nicht ein Mangel daneben |

Nutzbarer Restgehalt: eine `dev`-Abhängigkeitsgruppe fehlt, und wer versehentlich
mit dem System-Python 3.9 startet, bekommt einen nackten `TypeError` statt einer
verständlichen Meldung. Beides klein, beides sinnvoll — mehr ist an diesem Befund
nicht dran.

### BF-M2 — Verbindungsdaten als Quellcode-Defaults
**Urteil: bestätigt.** Entspricht Befund B-08 aus
[AENDERUNGEN_2026-08-18.md](AENDERUNGEN_2026-08-18.md), dort ohne die
Zugangsdaten-Betrachtung.

Prüfung: `WTConfig` (`wt3000_transport.py:60–75`) enthält
`dll_path` mit einem benutzerspezifischen Windows-Pfad, `ip = "192.168.10.20"`,
`user = "TEST"` und `password = "1"`.

Einordnung: Es handelt sich um Laborzugangsdaten eines abgeschlossenen Netzes,
nicht um schützenswerte Geheimnisse — die Dringlichkeit ist deshalb geringer, als
das Wort „Zugangsdaten" nahelegt. Der Portabilitätsteil wiegt schwerer: der
`dll_path` zeigt auf ein Verzeichnis, das auf keinem zweiten Rechner existiert, und
das ist die erste Hürde für jeden, der den Treiber als Bibliothek einsetzt. Die
ROADMAP führt das bereits unter M5-2 (`WT3000_IP`, `WT3000_TMCTL_DLL`).

### BF-M3 — Blockheader-Fehler nicht einheitlich übersetzt
**Urteil: bestätigt, kleiner Umfang.**

Prüfung: `WTSession._assemble_block()` (`wt3000_core.py:152–179`). Die Ziffernanzahl
wird in `:159–162` abgesichert. Das Längenfeld in `:167` —
`payload_length = int(raw[2:header_length])` — steht ungeschützt.

Zwei nachvollziehbare Auslöser:

- Antwort bricht nach dem Kopf ab: `b"#4"` → `raw[2:6]` ist leer → `int(b"")` →
  `ValueError`
- Längenfeld nicht numerisch: `b"#4AB12…"` → `ValueError`

Beides sind Antworten eines gestörten Geräts oder einer gestörten Verbindung,
also genau der Fall, für den `ProtocolError` gebaut wurde. Aufrufer, die
pflichtgemäß nur `WTError` behandeln — sämtliche Stufenskripte tun das —, laufen
in den ungefangenen `ValueError`. Der Aufwand für die Behebung liegt bei Minuten.

### BF-N1 — Doku und Implementierung auseinandergelaufen
**Urteil: teils überholt, teils Dublette, teils zutreffend.**

- *„Der Kopf von `__init__.py` sagt, das Modul importiere bewusst nichts aus dem
  Paket"* — **trifft nicht mehr zu.** Der Kopf wurde in M1-1 genau an dieser Stelle
  überarbeitet (`__init__.py:36–47`) und erklärt ausdrücklich, warum jetzt
  re-exportiert wird und dass die Import-Unabhängigkeit von einer anderen
  Eigenschaft getragen wird. Der Befund beschreibt den Stand vor dem Commit
  `b83e1fd`.
- *„Kommentare in `stage5b_range_probe.py` widersprechen dem aktivierten Default"*
  — zutreffend, aber deckungsgleich mit BF-H4.
- *„Mehrere `ZU VERIFIZIEREN`-Hinweise"* — zutreffend. Diese Hinweise sind allerdings
  kein Versehen, sondern bewusst gesetzte Marken; sie stehen als M0-1 bis M0-5 in
  der [ROADMAP.md](ROADMAP.md) und lassen sich ausschließlich am Gerät auflösen.

### Z-1 — `from_transport()` und direkte Konstruktion (neu)
Siehe BF-H1. Wird dort mitbehandelt.

### Z-2 — Schreibendes Geräteskript in der gerätefreien Testsuite (neu)
`tests/test_set_range_with_rangeio.py` baut eine echte `TmctlTransport`-Verbindung
auf, öffnet die Sitzung mit `read_only=False`, setzt einen Spannungsbereich an
Element 4 und stellt ihn zurück. Es ist ein Diagnoseskript zu ROADMAP-Punkt M0-1 —
inhaltlich richtig gebaut, mit Sicherung und Rückstellung.

Die Einordnung ist das Problem:

- `tests/conftest.py` erklärt im Kopf: *„Die gesamte Suite laeuft OHNE Geraet und
  ohne tmctl.dll."* Dieses Skript bricht die Zusage
- Der Name `test_*.py` sorgt dafür, dass `pytest` die Datei bei **jedem** Lauf
  einsammelt und importiert. Heute ohne Folgen: die Datei enthält nur `main()` und
  keine Testfunktion, geprüft — `pytest --collect-only` findet dort null Tests
- Genau darin liegt die Falle: eine später ergänzte Testfunktion oder ein Aufruf
  auf Modulebene würde `pytest` unbemerkt an das Messgerät schreiben lassen

Selbe Kategorie wie BF-H4: etwas, das nach „harmlos" aussieht, schreibt.

---

## 3 — Umsetzungsplan

Vier Pakete, absteigend nach Dringlichkeit. Innerhalb eines Pakets sind die Punkte
unabhängig voneinander und in beliebiger Reihenfolge machbar.

### Paket A — Garantien einhalten (zusammen etwa ein Arbeitstag) — ✅ ABGESCHLOSSEN 2026-08-19

> P-1 bis P-4 sind umgesetzt. Testsuite von 176 auf 204 Fälle, weiterhin ohne
> Gerät und ohne `tmctl.dll`; für jeden Befund existiert ein Test, der ohne die
> Korrektur fehlschlägt. Änderungsdokumente:
> [P-1](AENDERUNGEN_2026-08-19_P-1.md) · [P-2](AENDERUNGEN_2026-08-19_P-2.md) ·
> [P-3](AENDERUNGEN_2026-08-19_P-3.md) · [P-4](AENDERUNGEN_2026-08-19_P-4.md)

Alle vier Punkte betreffen Zusagen, die der Code im Docstring gibt und im
Fehlerfall nicht hält. Klein im Umfang, hoch in der Wirkung.

#### P-1
**BF-H1 + Z-1 — REMOTE beim gescheiterten Verbindungsaufbau abschalten** · `0,5 Tag` · Risiko gering
> **UMGESETZT am 2026-08-19** — siehe [AENDERUNGEN_2026-08-19_P-1.md](AENDERUNGEN_2026-08-19_P-1.md).
> 182 Tests grün (6 neue), Gegenprobe durchgeführt: ohne die Korrektur fallen drei davon durch.

Ziel: Nach einem misslungenen Verbindungsaufbau bleibt das Bedienfeld bedienbar —
unabhängig davon, über welchen der drei Wege konstruiert wurde.

Vorgehen:

- Die Reparatur gehört in `WT3000.__init__()`, **nicht** in `from_config()`. Nur
  dort werden alle drei Einstiegswege erfasst: `from_config()`, `from_transport()`
  und die direkte Konstruktion
- Ablauf im Konstruktor: alles nach `enable_remote()` — heute nur
  `DeviceInfo.read()` und `log_summary()` — in einen geschützten Abschnitt legen.
  Schlägt er fehl, zuerst `self._session.disable_remote()` versuchen, dessen
  eigenes Scheitern nur protokollieren, dann die ursprüngliche Ausnahme
  unverändert weiterreichen
- `disable_remote()` ist für diesen Einsatz bereits richtig gebaut: es prüft
  `_remote_active`, fängt `WTError` selbst ab und setzt das Flag im `finally`
  zurück. Ein Aufruf ohne vorher eingeschaltete Fernsteuerung ist folgenlos
- `from_config()` behält sein `except BaseException` mit `transport.close()` — das
  bleibt richtig, weil nur dieser Weg den Transport besitzt. Der irreführende
  Kommentar dort wird auf das reduziert, was der Block tatsächlich leistet
- Ausdrücklich mit prüfen: die Reihenfolge muss REMote OFF **vor** dem
  Transport-Close senden. Umgekehrt ginge das Kommando ins Leere

Prüfung (gerätefrei über `FakeTransport`):

- `FakeTransport` mit `fail_commands={":INPut:WIRing?"}` bestücken, damit
  `DeviceInfo.read()` scheitert
- `WT3000.from_transport(t, read_only=False, config=WTConfig(use_remote=True))`
  muss die Ausnahme durchreichen **und** `":COMMunicate:REMote OFF"` in
  `t.written` hinterlassen
- Gegenprobe mit `read_only=True`: dort wird REMote gar nicht erst eingeschaltet,
  also darf auch kein OFF gesendet werden
- Denselben Fall für `from_config()` — dort zusätzlich prüfen, dass der Transport
  geschlossen ist

#### P-2
**BF-H2 — Restore-Fehler der Item-Tabelle weiterreichen** · `0,5 Tag` · Risiko gering
> **UMGESETZT am 2026-08-19** — siehe [AENDERUNGEN_2026-08-19_P-2.md](AENDERUNGEN_2026-08-19_P-2.md).
> 186 Tests grün (4 neue), Gegenprobe durchgeführt: ohne die Korrektur fallen alle vier durch.
> Abweichung vom Plantext: die Gegenprobe nach dem Restore meldet Abweichungen als
> Fehler statt sie nur zu protokollieren — begründet im Änderungsdokument, Abschnitt 2.2.

Ziel: `ItemAccess.applied()` verhält sich im Fehlerfall wie `applied_ranges()`.
Wer den Kontextmanager ohne Ausnahme verlässt, darf sich darauf verlassen, dass
die Item-Tabelle steht.

Vorgehen:

- Im `finally` von `ItemAccess.applied()` (`wt3000_device.py:325–330`) nach dem
  Protokolleintrag erneut auslösen — wortgleich zum Vorbild in
  `wt3000_ranging.py:640–641`
- Die Verkettung beider Fehler entsteht dabei von selbst: eine im `finally`
  ausgelöste Ausnahme trägt die ursprüngliche als `__context__` und der Traceback
  zeigt beide. Kein Zusatzaufwand, keine Abhängigkeit von Python 3.11
- Zusätzlich, gleicher Handgriff: nach dem Restore eine Gegenprobe über
  `self.verify(backup)` und deren Ergebnis protokollieren. `applied_ranges()`
  macht das mit `backup.diff(...)` bereits vor; Stufe 3 und Stufe 4 bauen es von
  Hand nach
- **Bewusst nicht** umgesetzt: das in Befund.md alternativ vorgeschlagene
  Report-Objekt. Es wäre die größere Änderung — `applied()` gibt heute die
  `ItemTable` heraus, ein `ItemReport` würde den Rückgabetyp brechen. Der Nutzen
  über das erneute Auslösen hinaus ist gering, und wer die Auswertung braucht,
  kann `apply()`/`restore()` einzeln aufrufen. Falls doch gewünscht, gehört das in
  ROADMAP M2-4, wo die Sicherungsformate ohnehin zusammengeführt werden

Prüfung:

- `FakeTransport` mit `fail_commands` auf einem `:NUMeric:NORMal:ITEM…`-Kommando,
  sodass der Restore scheitert. `with wt.items.applied(specs):` muss die Ausnahme
  aus dem `with` heraustragen
- Zweiter Fall: Fehler im Nutzblock **und** misslungener Restore. Beide müssen im
  Traceback auffindbar sein
- Erfolgsfall: kein Fehler, `applied()` läuft durch, Ausgangstabelle steht wieder

#### P-3
**BF-H3 — CSV-Zeile gegen den Kopf absichern** · `0,5 Tag` · Risiko gering
> **UMGESETZT am 2026-08-19** — siehe [AENDERUNGEN_2026-08-19_P-3.md](AENDERUNGEN_2026-08-19_P-3.md).
> 193 Tests grün (7 neue), Gegenprobe durchgeführt: ohne die Korrektur fallen vier davon durch.
> Umgesetzt wie geplant, einschließlich `strict`-Schalter und der Trennung
> Datenpfad (Abbruch) gegen Diagnose (`map_values()` bleibt bei der Warnung).

Ziel: Eine Messdatei enthält entweder Zeilen, deren Spalten zum Kopf passen, oder
sie bricht ab. Kein dritter Fall.

Vorgehen:

- In `CsvRecorder.write_row()` vor dem Schreiben `len(values)` gegen
  `len(self._columns)` prüfen und bei Abweichung eine `WTError` auslösen, die beide
  Zahlen und die laufende Sample-Nummer nennt
- Abbruch statt Auffüllen ist die richtige Voreinstellung — dieser Einschätzung aus
  Befund.md folge ich. Begründung: Eine abweichende Werteanzahl bedeutet, dass die
  Item-Tabelle im Gerät nicht mehr der ist, gegen die der Kopf geschrieben wurde.
  Aufgefüllte Zeilen wären dann inhaltlich falsch, nicht nur unvollständig
- Die zweite Bruchstelle mit schließen: `read_numeric_values()` bekommt einen
  Schalter `strict` (Voreinstellung `True`), der bei abweichendem `expected_count`
  auslöst statt zu warnen. Damit fällt die Abweichung dort auf, wo sie entsteht —
  eine Abfrage früher als in der CSV
- `ItemTable.map_values()` (`wt3000_numeric.py`) bleibt bei der Warnung: die
  Funktion ist eine Bequemlichkeit für die Anzeige, nicht der Datenpfad. Die
  Trennung ist im Docstring festzuhalten
- Der Testfall `test_zu_wenige_werte_werden_gemeldet` beschreibt seinen eigenen
  Zweck als Anschlagpunkt für genau diese Umstellung. Er wird mitgezogen und
  dokumentiert danach die neue Festlegung

Prüfung:

- `CsvRecorder` mit drei Spalten, `write_row()` mit zwei und mit vier Werten →
  jeweils `WTError`, und die Datei enthält danach ausschließlich den Kopf
- Regelfall mit passender Anzahl → Zeile wie bisher, `status_flags` an letzter
  Stelle
- `read_numeric_values(..., expected_count=n, strict=True)` gegen einen
  `FakeTransport`-Block mit abweichender Länge

#### P-4
**BF-M3 — Blockheader vollständig validieren** · `0,25 Tag` · Risiko sehr gering
> **UMGESETZT am 2026-08-19** — siehe [AENDERUNGEN_2026-08-19_P-4.md](AENDERUNGEN_2026-08-19_P-4.md).
> 204 Tests grün (11 neue), Gegenprobe durchgeführt: ohne die Korrektur fallen sieben davon durch.
> **Paket A ist damit abgeschlossen.**

Ziel: Jeder Formfehler in einer Blockantwort verlässt `_assemble_block()` als
`ProtocolError`.

Vorgehen:

- Vor dem Zugriff prüfen, dass `raw` mindestens `header_length` Bytes hat —
  sonst ist das Längenfeld abgeschnitten
- Die Umwandlung des Längenfelds in denselben `try`-Block ziehen wie die
  Ziffernanzahl, oder einen zweiten mit eigener Meldung anlegen. Die Meldung soll
  die ersten Bytes zeigen, wie es die bestehende Meldung in `:162` vormacht
- Eine negative oder unplausibel große Nutzlastlänge ebenfalls abfangen — die
  Nachlese-Schleife begrenzt sich zwar nach 64 Durchläufen, aber die Meldung
  „nach 64 Lesevorgaengen immer noch unvollstaendig" führt dann auf die falsche
  Spur

Prüfung: `_assemble_block()` direkt mit `b"#"`, `b"#4"`, `b"#4AB12"` und `b"#0"`
aufrufen — jeder Fall `ProtocolError`, keiner ein nackter `ValueError`.

### Paket B — Schreibzugriffe sichtbar machen (etwa ein Tag) — ✅ ABGESCHLOSSEN 2026-08-19

> P-5 und P-6 sind umgesetzt. Änderungsdokumente:
> [P-5](AENDERUNGEN_2026-08-19_P-5.md) · [P-6](AENDERUNGEN_2026-08-19_P-6.md)

#### P-5
**BF-H4 — Schreibprobe in Stufe 5b zum Laufzeitparameter machen** · `0,5 Tag` · Risiko gering
> **UMGESETZT am 2026-08-19** — siehe [AENDERUNGEN_2026-08-19_P-5.md](AENDERUNGEN_2026-08-19_P-5.md).
> 214 Tests grün (8 neue), Gegenprobe durchgeführt. Umgesetzt wie geplant:
> `main(enable_write_probe=False)`, `--write-probe` über argparse, Warnzeilen vor
> dem ersten Zugriff. Stufenskripte sind damit erstmals überhaupt getestet.

Ziel: Voreinstellung wieder rein lesend, Schreiben nur auf ausdrückliche Ansage —
ohne dem Bearbeiter die Fähigkeit zu nehmen, die er für M0-1 bis M0-3 braucht.
Das setzt um, was der Kommentar im Code selbst fordert.

Vorgehen:

- `main()` bekommt einen Parameter `enable_write_probe: bool = False`; die
  Modulkonstante entfällt
- Kommandozeile über `argparse`: `python -m wt3000_scpi.stage5b_range_probe
  --write-probe`. Ohne den Schalter schreibt das Skript nichts
- Der Schalter soll unangenehm sein: beim Start eine Warnzeile ins Protokoll,
  die benennt, welches Element mit welchem Wert überschrieben wird
- Dateikopf auf das tatsächliche Verhalten bringen: die Voreinstellung ist lesend,
  der Schalter macht sie schreibend
- Denselben Weg für die anderen Stufenskripte vorsehen, aber **nicht** in diesem
  Durchgang — dort stehen die Laufparameter ebenfalls als Modulkonstanten
  (`EXERCISE_RESTORE_WRITE`, `FORCE_FULL_RESTORE`, `MAX_SAMPLES` …). Das gehört
  gesammelt in ROADMAP M5-2, sonst entstehen fünf verschiedene Kommandozeilen

Prüfung: `main(enable_write_probe=False)` gegen `FakeTransport` — `t.written` darf
kein `:INPut:VOLTage:RANGe`-Kommando enthalten. Damit ist die Voreinstellung
erstmals maschinell abgesichert.

#### P-6
**Z-2 — Geräteskript aus der Testsuite herausnehmen** · `0,25 Tag` · Risiko sehr gering
> **UMGESETZT am 2026-08-19** — siehe [AENDERUNGEN_2026-08-19_P-6.md](AENDERUNGEN_2026-08-19_P-6.md).
> 206 Tests grün (2 neue). Abweichung vom Plantext: die Sicherung ist keine
> AST-Prüfung, sondern eine Sperre auf Modulebene in `conftest.py` — nur die
> greift auch beim Einsammeln. Der AST-Scanner wurde gebaut und wieder verworfen,
> begründet im Änderungsdokument, Abschnitt 4.

Ziel: `tests/` enthält ausschließlich, was ohne Gerät läuft — so, wie `conftest.py`
es zusagt.

Vorgehen:

- `tests/test_set_range_with_rangeio.py` nach `tools/probe_set_range.py` oder
  `examples/` verschieben. Entscheidend ist nur, dass der Name nicht mehr auf
  `test_*.py` passt
- Kopf ergänzen: dieses Skript spricht mit dem Gerät und schreibt
- Den Schalter aus P-5 gleich mitgeben, damit beide Diagnoseskripte gleich bedient
  werden
- Ergänzend eine Sicherung in der Suite: ein Test, der `tests/` durchgeht und
  fehlschlägt, sobald eine Testdatei `TmctlTransport` importiert.
  `tests/test_package_layout.py` prüft Importe bereits mit `ast` und liefert das
  Muster dafür

Prüfung: `pytest --collect-only` sammelt die Datei nicht mehr ein; die neue
Sicherung schlägt an, wenn man sie versuchsweise zurückkopiert.

### Paket C — Portabilität (ein bis anderthalb Tage) — ✅ ABGESCHLOSSEN 2026-08-19

> P-7 ist umgesetzt: [AENDERUNGEN_2026-08-19_P-7.md](AENDERUNGEN_2026-08-19_P-7.md)

#### P-7
**BF-M2 — Herkunft der Verbindungsparameter konfigurierbar machen** · `1–1,5 Tage` · Risiko mittel
> **UMGESETZT am 2026-08-19** — siehe [AENDERUNGEN_2026-08-19_P-7.md](AENDERUNGEN_2026-08-19_P-7.md).
> 241 Tests grün (26 neue), Gegenprobe durchgeführt. Umgesetzt wie geplant, mit
> einem Zusatz: die Konfigurationsdatei ist JSON (nicht TOML — `tomllib` gibt es
> erst ab Python 3.11, verlangt werden 3.10), und `_`-Schlüssel gelten als
> Kommentare, damit die mitgelieferte Vorlage unverändert kopierbar ist.

Ziel: Der Treiber läuft auf einem zweiten Rechner, ohne dass Quelltext geändert
wird. Deckt zugleich ROADMAP M5-2 zur Hälfte ab.

Vorgehen:

- Rangfolge festlegen und dokumentieren: ausdrücklicher Parameter → Umgebungsvariable
  → Konfigurationsdatei → eingebaute Voreinstellung
- Umgebungsvariablen: `WT3000_IP`, `WT3000_TMCTL_DLL`, `WT3000_USER`,
  `WT3000_PASSWORD`, `WT3000_TIMEOUT_MS`. Auswertung in einer Klassenmethode
  `WTConfig.from_environment()`, damit `WTConfig` selbst eine reine Datenklasse
  bleibt und der Import weiterhin nichts von der Umgebung liest
- `dll_path`: die Voreinstellung auf einen neutralen Namen setzen (`tmctl64.dll`)
  und beim Öffnen zusätzlich in den üblichen Verzeichnissen suchen. Die
  Fehlermeldung in `TmctlTransport` ist bereits gut — sie nennt den gesuchten Pfad
  und ist um die geprüften Orte zu erweitern
- `user`/`password`: Voreinstellung leer. Wenn das Gerät ohne Anmeldung erreichbar
  ist, ändert das nichts; wenn nicht, ist die Meldung eindeutig. Die heutigen
  Laborwerte wandern in die README als Beispiel — nicht in den Quelltext
- **Verträglichkeit beachten:** `WTConfig` ist `frozen=True` und wird an vielen
  Stellen ohne Argumente erzeugt (`WTConfig()` in allen Stufenskripten). Ändert
  sich die Voreinstellung von `ip`, laufen diese Skripte ins Leere. Deshalb
  gehören die Skripte im selben Schritt auf `WTConfig.from_environment()` umgestellt

Prüfung: `from_environment()` gegen gesetzte und nicht gesetzte Variablen
(`monkeypatch.setenv`); Rangfolge Parameter vor Umgebung; unveränderte
Voreinstellungen, wenn nichts gesetzt ist.

### Paket D — Restarbeiten (halber Tag) — ✅ ABGESCHLOSSEN 2026-08-19

> P-8 ist umgesetzt: [AENDERUNGEN_2026-08-19_P-8.md](AENDERUNGEN_2026-08-19_P-8.md).
> **Damit sind alle acht Planpunkte erledigt**; die Testsuite ist von 176 auf 241
> Fälle gewachsen.

#### P-8
**BF-M1-Rest + BF-N1-Rest — Werkzeuge und Dokumentation nachziehen** · `0,5 Tag` · Risiko sehr gering
> **UMGESETZT am 2026-08-19** — siehe [AENDERUNGEN_2026-08-19_P-8.md](AENDERUNGEN_2026-08-19_P-8.md).
> `ruff check .` und `mypy` laufen ohne Argumente und sind grün. Zusatz gegenüber
> dem Plantext: die Werkzeuge wurden vor dem Deklarieren laufen gelassen und
> konfiguriert, sodass sie beim ersten Aufruf keine Altlasten vorsetzen — dabei
> kam eine echte Typlücke in `RangePlan.describe()` heraus.

- `[project.optional-dependencies]` um eine `dev`-Gruppe ergänzen: `pytest`,
  `pyflakes`, `ruff`, `mypy`. Damit ist reproduzierbar, womit geprüft wird —
  der einzig belastbare Punkt aus BF-M1
- README um einen Satz zum Interpreter erweitern: Python ab 3.10, das
  macOS-System-Python 3.9 genügt nicht, empfohlener Weg über `python3 -m venv`.
  Das ersetzt den nackten `TypeError` durch eine Erwartung
- BF-N1 zu `__init__.py` benötigt keine Maßnahme — der Kopf ist seit M1-1 aktuell.
  Der Punkt wird in diesem Dokument als erledigt vermerkt, damit er nicht erneut
  auftaucht
- Die `ZU VERIFIZIEREN`-Marken bleiben stehen, bis M0 am Gerät beantwortet ist.
  Sie sind der einzige Ort, an dem eine ungeprüfte Hardwareannahme sichtbar ist;
  sie vorher zu entfernen würde die Unsicherheit verstecken, nicht beseitigen

---

## 4 — Reihenfolge und Abnahme

```
Paket A   P-1 ─┐
          P-2 ─┼─ unabhängig voneinander, zusammen etwa ein Arbeitstag
          P-3 ─┤
          P-4 ─┘

Paket B   P-5 ──> P-6   (P-6 übernimmt den Schalter aus P-5)

Paket C   P-7          berührt WTConfig, danach alle Stufenskripte anfassen

Paket D   P-8          jederzeit, am besten zum Abschluss
```

**Empfehlung:** Paket A geschlossen in einem Durchgang. Alle vier Punkte sind
kleine, klar umrissene Eingriffe an Stellen, die eine Zusage geben und im
Fehlerfall nicht halten — und alle vier sind gerätefrei über `FakeTransport`
prüfbar. Danach Paket B, weil es einen unbeabsichtigten Schreibzugriff ausschließt.
Paket C erst danach, weil es als einziges eine bestehende Schnittstelle berührt.

**Abnahmekriterien für den gesamten Plan:**

- Die Testsuite läuft weiterhin ohne Gerät und ohne `tmctl.dll`, mit den heutigen
  176 Fällen plus etwa zwölf neuen
- `pyflakes` bleibt ohne Meldung
- Für jeden behobenen Befund existiert ein Test, der ohne die Änderung fehlschlägt
- Kein Docstring verspricht mehr etwas, das der Code im Fehlerfall nicht hält —
  das ist die gemeinsame Klammer über BF-H1, BF-H2, BF-H3 und BF-H4
- Jede Änderung trägt im Quelltext eine Marke `UEBERARBEITET (P-nn)` und ist in
  einem Änderungsdokument beschrieben, wie es für F-01…F-09 bereits geschehen ist

---

## 5 — Was ich nicht umsetzen würde

| Vorschlag aus Befund.md | Begründung |
|---|---|
| `ENABLE_NOOP_WRITE_PROBE` einfach auf `False` setzen | Nimmt dem Bearbeiter die Fähigkeit, die er für die offenen Gerätefragen braucht, und wird beim nächsten Mal wieder von Hand umgestellt. Der Laufzeitparameter aus P-5 löst dasselbe Problem dauerhaft |
| CSV-Zeilen auf Headerlänge auffüllen oder abschneiden | Eine abweichende Werteanzahl heißt, dass die Item-Tabelle nicht mehr die ist, gegen die der Kopf geschrieben wurde. Aufgefüllte Zeilen wären dann falsch statt unvollständig — und niemand würde es der Datei ansehen |
| `pyproject.toml` und README anlegen | Beide existieren. Nur die `dev`-Gruppe fehlt (P-8) |
| `requirements.txt` ergänzen | Doppelte Buchführung neben `pyproject.toml`. Die optionalen Gruppen leisten dasselbe und werden von `pip` durchgesetzt |
| Kopf von `__init__.py` korrigieren | Ist seit Commit `b83e1fd` (M1-1) aktuell und erklärt den Re-Export ausdrücklich |
| `ItemReport` analog zu `RangeReport` einführen | Bricht den Rückgabetyp von `applied()` für einen Nutzen, den das erneute Auslösen bereits liefert. Gehört, wenn überhaupt, in ROADMAP M2-4 |

---

## 6 — Zusammenfassung

Von acht Befunden treffen sechs zu. Drei davon — BF-H1, BF-H2 und BF-H3 — sind
Fälle desselben Musters: der Docstring gibt eine Garantie, der Fehlerpfad hält sie
nicht. In allen drei Fällen ist die Behebung klein, gerätefrei prüfbar und ohne
Schnittstellenbruch möglich; zusammen mit BF-M3 sind das etwa ein Arbeitstag.

BF-H4 beschreibt ein echtes Problem, aber die vorgeschlagene Lösung würde die
laufende Klärungsarbeit am Gerät behindern — der Laufzeitparameter ist der bessere
Weg und steht bereits als Notiz im Code. BF-M1 ist gegen einen veralteten
Projektstand geschrieben und trifft bis auf die fehlende `dev`-Gruppe nicht zu.

Zwei Punkte fehlen in Befund.md: `WT3000.from_transport()` hat dieselbe
REMOTE-Lücke wie `from_config()` — eine Reparatur nur an der beschriebenen Stelle
würde die zweite Tür offen lassen —, und in `tests/` liegt ein Skript, das mit dem
Gerät spricht und schreibt, obwohl die Suite ausdrücklich gerätefrei sein soll.
