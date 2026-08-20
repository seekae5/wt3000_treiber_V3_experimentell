# Aufwärts-Aufrufkette der Schichten — Analyse

**Projekt:** `wt3000-scpi 0.3.0`
**Stand:** Quellstand vom 2026-08-20, Commit `7bfd5e7`, 306 Tests grün (`python3.12 -m pytest`)
**Auftrag:** Die aufwärts gerichtete Aufrufverkettung der Schichten prüfen — insbesondere,
wo der Aufruf von Stufenskripten auf die unteren Schichten 1 und 2 zu Problemen führen
kann, vor allem bei Zugriffen auf `wt3000_core.py` und `wt3000_transport.py`.

**Methode:** Quelltextlesung aller 16 Paketmodule und der sieben ausführbaren Skripte,
ergänzt um Reproduktionen gegen `FakeTransport`. Jeder Befund, der mit **Nachweis**
gekennzeichnet ist, wurde ausgeführt; die Läufe stehen in Abschnitt 7.

**Abgrenzung:** Am Code wurde nichts geändert. Gerätefragen (M0, H-01…H-07) bleiben
außen vor — hier geht es ausschließlich um die Kette *innerhalb* der Software. Befunde,
die [OFFENE_PUNKTE.md](OFFENE_PUNKTE.md) bereits führt, sind als solche gekennzeichnet;
neu ist bei ihnen die konkrete Fundstelle in der Aufrufkette.

---

## 1 — Die Kette, wie sie tatsächlich läuft

Die Soll-Schichtung steht im Kopf von [`__init__.py`](../src/wt3000_scpi/__init__.py)
und wird von [`tests/test_package_layout.py`](../tests/test_package_layout.py) erzwungen:

```
Layer 0   wt3000_transport   Transport-Protocol, TmctlTransport, FakeTransport, WTConfig
Layer 1   wt3000_core        WTSession                    wt3000_common   Parser, Scope, Logging
Layer 2   wt3000_numeric     wt3000_rangeio     wt3000_input
Layer 3   wt3000_itemspec    wt3000_ranging     wt3000_measure    wt3000_sinks
Layer 4   wt3000_device (Fassade)               stage2..stage5b   tools/hardware/*
```

Was die sieben ausführbaren Skripte davon tatsächlich aufrufen:

| Skript | L3 | L2 | **L1 `wt3000_core`** | **L0 `wt3000_transport`** |
|---|---|---|---|---|
| `stage2_read_numeric` | — | `numeric` | `WTSession`, `WTError` | `TmctlTransport`, `WTConfig` |
| `stage3_own_itemtable` | `itemspec` | `numeric` | `WTSession`, `WTError` | `TmctlTransport`, `WTConfig` |
| `stage4_measure` | `itemspec`, `measure`, `sinks` | `numeric` | `WTSession`, `WTError` | `TmctlTransport`, `WTConfig` |
| `stage5_input_config` | — | `input` | `WTSession`, `WTError` | `TmctlTransport`, `WTConfig` |
| `stage5b_range_probe` | `ranging` | `rangeio` | `WTSession`, `WTError` | `TmctlTransport`, `WTConfig` |
| `tools/hardware/probe_voltage_range` | — | `rangeio` | `WTSession`, `WTError` | `TmctlTransport`, `WTConfig` |
| `tools/hardware/probe_current_range` | — | `rangeio` | `WTSession`, `WTError` | `TmctlTransport`, `WTConfig` |
| `wt3000_device` (Fassade, Vergleich) | alle | alle | `WTSession`, `WTError` | `TmctlTransport`, `WTConfig` |

Zwei Eigenschaften dieser Tabelle bestimmen alles Weitere:

1. **Jedes ausführbare Skript baut Transport und Sitzung selbst auf.** Die vier Zeilen
   `WTConfig.from_environment()` → `TmctlTransport(config)` → `WTSession(...)` →
   `enable_remote()` stehen siebenmal im Bestand, in fünf verschiedenen Fassungen.
   Sie sind der eigentliche Gegenstand dieser Analyse.
2. **Kein einziges Skript nennt Layer 0 beim Namen.** `TmctlTransport` und `WTConfig`
   wohnen in `wt3000_transport.py`, werden aber ausnahmslos über die Weiterleitung in
   `wt3000_core.py` bezogen (siehe A-12).

---

## 2 — Der Kernbefund

> **Die Schutzregeln liegen durchweg eine Schicht über dem Knoten, den sie schützen.**

Das ist für die Fassade richtig und für die Stufenskripte gefährlich, denn Layer 4 darf
Layer 2 direkt aufrufen — und tut es. Vier Beispiele desselben Musters:

| Schutzregel | wohnt in | fehlt in |
|---|---|---|
| Existiert das Element? | `wt3000_ranging` über `access.expand_scope()` | `RangeAccess.set_range()` / `get_range()` |
| Ist der Bereichswert eine gültige Stufe? | `RangePlan.validate()`, `wt3000_input._check_allowed()` | `RangeAccess.set_range()` (dokumentiert) |
| Wird der Ausgangszustand garantiert zurückgestellt? | `applied_ranges()`, `ItemAccess.applied()` | `RangeAccess`, `ItemTable` |
| Wird REMOTE auch bei Abbruch zurückgenommen? | `WT3000.__init__` / `close()` | `WTSession` |

Wer von Layer 4 aus an Layer 3 vorbeigreift, verliert die Regel — ohne dass irgendetwas
davon Notiz nimmt. Genau das tun `tools/hardware/*` (direkt auf Layer 2) und in
Teilen `stage5b`. Die Befunde A-01 bis A-03 sind drei Ausprägungen dieses einen Musters.

---

## 3 — Befunde

### 3.1 — Wo die Kette den Gerätezustand verlieren kann

#### A-01 — REMOTE bleibt in Stufe 3 und 4 stehen, wenn ein Nicht-`WTError` aus der Wiederherstellung kommt

**Ort:** [stage3_own_itemtable.py:192–214](../src/wt3000_scpi/stage3_own_itemtable.py#L192),
[stage4_measure.py:211–231](../src/wt3000_scpi/stage4_measure.py#L211)

Beide Skripte haben dieselbe Form:

```python
finally:
    if backup is not None:
        try:
            written = restore_item_table(session, backup, tail)
            ...
        except WTError as exc:          # fängt nur WTError
            ...
    session.disable_remote()            # steht DAHINTER, nicht in einem eigenen finally
```

Verlässt eine Ausnahme, die kein `WTError` ist, den Wiederherstellungsblock, wird
`session.disable_remote()` übersprungen. Sie läuft dann aus dem `with TmctlTransport(...)`
heraus — der Transport wird geschlossen, ein `:COMMunicate:REMote OFF` ist danach nicht
mehr möglich.

**Nachweis:** Reproduktion 7.1. `stage3.main()` bricht mit `KeyError` ab, gesendet wurde
`[':COMMunicate:REMote ON']`, `REMote OFF gesendet? False`.

**Wirkung am Gerät:** Das Bedienfeld bleibt gesperrt. Der Anwender muss am Gerät LOCAL
drücken. Das ist derselbe Zustand, den P-1 für die Fassade beseitigt hat — dort steht seit
[wt3000_device.py:612](../src/wt3000_scpi/wt3000_device.py#L612) ein
`except BaseException:` mit `_release_remote_after_failure()`.

**Stufe 2 ist nicht betroffen:** dort steht `disable_remote()` in einem eigenen,
bedingungslosen `finally` ([stage2_read_numeric.py:158](../src/wt3000_scpi/stage2_read_numeric.py#L158)).
Drei Skripte, dieselbe Aufgabe, zwei Lösungen — die richtige ist die von Stufe 2.

**Vorschlag:** `disable_remote()` in Stufe 3 und 4 in ein eigenes `finally` legen, oder —
besser — die Sitzungsführung ganz an die Fassade abgeben (M5-2). Roadmap: M1-5.

---

#### A-02 — Die Gerätewerkzeuge unter `tools/hardware/` schreiben ohne `finally`

**Ort:** [probe_voltage_range.py:68–79](../tools/hardware/probe_voltage_range.py#L68),
[probe_current_range.py:93–104](../tools/hardware/probe_current_range.py#L93)

```python
original = access.get_range(Quantity.VOLTAGE, ELEMENT)
command  = access.set_range(Quantity.VOLTAGE, ELEMENT, TEST_VALUE)   # 1000 V bzw. 0.5 A
readback = access.get_range(Quantity.VOLTAGE, ELEMENT)
access.set_range(Quantity.VOLTAGE, ELEMENT, original.value, ...)     # kein finally
session.assert_no_error(...)
```

Der Dateikopf sagt zu: *„Ausgangswert wird vor dem Schreiben gelesen und danach
zurückgesetzt."* Das gilt nur auf dem glatten Weg. Zwischen `set_range` und der
Rückstellung liegen ein Query und zwei Protokollausgaben; jede Ausnahme dort — und ein
Strg+C an jeder Stelle — lässt `TEST_VALUE` auf Element 4 stehen. Danach wird auch
`assert_no_error()` übersprungen, der Lauf endet also ohne Prüfung der Fehlerqueue.

Zum Vergleich: Stufe 5b löst dieselbe Aufgabe als Nulleffekt — sie schreibt den bereits
eingestellten Wert und prüft danach per `backup.diff(...)`, dass sich nichts geändert hat
([stage5b_range_probe.py:102–118](../src/wt3000_scpi/stage5b_range_probe.py#L102)).
Die beiden Werkzeuge schreiben dagegen einen *anderen* Wert und haben keine Absicherung.

**Zwei weitere Schwächen derselben Skripte:**

* Sie rufen **nie** `session.enable_remote()` auf, obwohl `WTConfig.use_remote` in der
  Voreinstellung `True` ist. Ob `:INPut` ein `REMote ON` braucht, ist offene Gerätefrage
  H-03/M0-3. Damit vermischt der Versuch, der M0-1 (Parametersyntax) klären soll, genau
  die zwei Ursachen, die er trennen müsste: schlägt die Rückleseprobe fehl, ist nicht
  entscheidbar, ob die Syntax falsch war oder REMOTE fehlte.
* Sie **vergleichen `readback` nicht mit `TEST_VALUE`**. Beide Werte gehen nur ins
  Protokoll; der Rückgabewert von `main()` ist auch dann 0, wenn das Gerät den Wert nicht
  übernommen hat. Der Befund muss von Hand aus dem Log gelesen werden.

**Vorschlag:** `try/finally` um den Schreibteil, `enable_remote()` entsprechend
`config.use_remote` (oder ausdrücklich begründet weglassen, wie es Stufe 5b im Dateikopf
tut), und `values_match(TEST_VALUE, readback.value)` als maschinelles Urteil.
Roadmap: M0-1 — diese Skripte sind das Werkzeug dafür und sollten vor dem Gerätetermin
belastbar sein.

---

#### A-03 — `RangeAccess.set_range()` prüft die Elementnummer nicht

**Ort:** [wt3000_rangeio.py:286](../src/wt3000_scpi/wt3000_rangeio.py#L286) gegen
[wt3000_rangeio.py:206](../src/wt3000_scpi/wt3000_rangeio.py#L206)

`RangeAccess` kennt seine bestückten Elemente (`self._elements`) und hat mit
`expand_scope()` eine Methode, die einen Scope dagegen prüft. `set_range()` und
`get_range()` benutzen sie nicht — sie gehen direkt über `scope_suffix(scope)`.
`expand_scope()` wird ausschließlich aus `wt3000_ranging` heraus aufgerufen (4 Stellen).

**Nachweis:** Reproduktion 7.2. `set_range(Quantity.VOLTAGE, 7, 1000.0)` liefert
`:INPut:VOLTage:RANGe:ELEMent7 1000` und sendet es; `expand_scope(7)` hätte
`WTError: Element 7 existiert nicht (vorhanden: (1, 2, 3, 4))` geworfen.

**Wirkung:** Jeder Layer-4-Aufrufer, der Layer 2 direkt benutzt — beide Werkzeuge unter
`tools/hardware/`, jeder Anwender, der `wt.ranges` aus der Fassade zieht — kann auf ein
nicht vorhandenes Element schreiben. Am Gerät fällt das als Fehlerqueue-Eintrag auf,
also erst bei `assert_no_error()`, oder gar nicht.

Verschärfend: `RangeAccess` wird in `stage5b` und in beiden Werkzeugen mit der
Voreinstellung `elements=DEFAULT_ELEMENTS` = `(1, 2, 3, 4)` erzeugt, also mit einer
Annahme statt mit dem gelesenen Gerätesteckbrief — obwohl `stage5b` ein Feld weiter
`access.get_module()` protokolliert. Das ist S-01 an einer weiteren Stelle.

**Vorschlag:** `set_range()`/`get_range()` über `expand_scope()` führen. Die Prüfung
kostet nichts und gehört zu dem Objekt, das die Elementliste besitzt. Roadmap: M1-3/S-01.

---

### 3.2 — Wo der Fehlervertrag reißt

Alle sieben Skripte fangen **ausschließlich `WTError`**. Das ist die richtige Wahl — sie
ist die dokumentierte Treibergrenze. Sie trägt aber nicht überall.

#### A-04 — Der Konstruktor von `TmctlTransport` hat drei rohe Fehlerwege

**Ort:** [wt3000_transport.py:456–459](../src/wt3000_scpi/wt3000_transport.py#L456)

```python
if isinstance(dll, Path) and hasattr(os, "add_dll_directory"):
    os.add_dll_directory(str(dll.parent))     # OSError / FileNotFoundError
self._tm = ct.WinDLL(str(dll))                # OSError; ausserhalb Windows AttributeError
```

`resolve_dll_path()` ist sorgfältig gebaut und wirft `WTError` mit einer Meldung, die alle
drei Abhilfen nennt. Die beiden Zeilen danach nicht:

* **Nicht-Windows:** `ctypes` hat kein `WinDLL` → `AttributeError`.
* **Windows, DLL vorhanden, aber abhängige DLL fehlt oder falsche Bitness:** `OSError`
  aus `ct.WinDLL` — der praktisch häufigste TMCTL-Installationsfehler.
* `os.add_dll_directory()` auf ein Verzeichnis, das nicht mehr existiert: `OSError`.

Dazu kommt [wt3000_transport.py:511](../src/wt3000_scpi/wt3000_transport.py#L511):
`command.encode("ascii")` wirft `UnicodeEncodeError`, wenn ein Nicht-ASCII-Zeichen in ein
Kommando gerät (z. B. über einen Parameter aus einer Konfigurationsdatei).

**Nachweis:** Reproduktion 7.3.
`NICHT WTError -> AttributeError : module 'ctypes' has no attribute 'WinDLL'`

**Wirkung:** Statt der Zeile `Abbruch: TMCTL-DLL nicht gefunden: … Pfad setzen über
WT3000_DLL_PATH, über 'wt3000.json' oder als Parameter.` bekommt der Anwender einen
Traceback ohne jeden Hinweis auf die Auflösungskette. `raise SystemExit(main())` wird
nicht erreicht, der Rückgabewert 1 kommt aus dem Traceback statt aus dem Skript, und in
der Protokolldatei steht nichts.

**Vorschlag:** Den DLL-Ladeteil in `TmctlTransport.__init__` in `try/except OSError,
AttributeError` fassen und in `WTError` übersetzen — mit derselben Meldungsqualität, die
`resolve_dll_path()` schon hat. Das ist der Spiegelstrich *„erwartbare Tabellen-/Parser-
fehler an der Paketgrenze in `WTError` übersetzen"* aus M1-5, angewendet auf Layer 0.

---

#### A-05 — `FakeTransport` bricht die Zusage, die `Transport` gibt

**Ort:** Zusage in [wt3000_transport.py:396](../src/wt3000_scpi/wt3000_transport.py#L396),
Bruch in [wt3000_transport.py:698](../src/wt3000_scpi/wt3000_transport.py#L698)

Das `Transport`-Protocol sagt wörtlich zu:

> *jeder Fehler auf der Leitung kommt als `TmctlError` heraus, damit die Aufrufer oben nur
> eine Fehlerklasse abfangen müssen*

`FakeTransport._lookup()` wirft für ein nicht hinterlegtes Kommando einen nackten
`KeyError` — mit guter Begründung (*„eine nicht hinterlegte Abfrage soll auffallen"*), aber
eben nicht als `WTError`.

**Nachweis:** Reproduktion 7.4. `stage5b.main()` gegen eine Antworttabelle ohne
`:INPut:POVer` bricht ab mit
`KeyError -> "FakeTransport hat keine Antwort fuer ':INPut:POVer?'."`

Die beiden Absichten kollidieren nicht wirklich — eine fehlende Tabellenzeile ist kein
Leitungsfehler, sondern ein Aufbaufehler des Tests. Sichtbar ist der Unterschied aber nur
in Layer 0. In Layer 4 kommt beides an derselben Stelle an, und dort ist der Fehlervertrag
je nach Transport ein anderer: `TmctlTransport` liefert `TmctlError` (also `WTError`),
`FakeTransport` liefert `KeyError`. Für den vorgesehenen `SocketTransport`
([wt3000_transport.py:775 ff.](../src/wt3000_scpi/wt3000_transport.py#L775)) ist das die
Stelle, an der sich entscheidet, ob `socket.timeout` durchschlägt.

**Wirkung:** Ein Trockenlauf eines Stufenskripts gegen `FakeTransport` — der Weg, den
`test_stage5b_write_probe.py` etabliert hat und der für die übrigen Stufen naheliegt —
verhält sich im Fehlerfall anders als der Lauf am Gerät. Damit prüft er genau die
Fehlerpfade nicht, für die man ihn bauen würde.

**Vorschlag:** Entweder eine eigene `FakeTransportError(WTError)` einführen (dann bleibt
sie auffällig *und* fangbar) oder die Zusage im Protocol-Docstring auf *Leitungsfehler*
einschränken und die Ausnahme benennen. Roadmap: M1-5.

---

#### A-06 — Rohes `int()` / `float()` auf Geräteantworten, an sechs Stellen

**Ort:**

| Stelle | Aufruf |
|---|---|
| [stage2_read_numeric.py:65](../src/wt3000_scpi/stage2_read_numeric.py#L65) | `bits = int(condition)` |
| [stage3_own_itemtable.py:83](../src/wt3000_scpi/stage3_own_itemtable.py#L83) | `int(session.query(":STATus:CONDition?"))` |
| [stage4_measure.py:96](../src/wt3000_scpi/stage4_measure.py#L96) | `float(session.query(":RATE?"))` |
| [stage4_measure.py:105](../src/wt3000_scpi/stage4_measure.py#L105) | `int(session.query(":STATus:CONDition?"))` |
| [wt3000_measure.py:504](../src/wt3000_scpi/wt3000_measure.py#L504) | `int(session.query(":STATus:CONDition?"))` — **in der Messschleife** |
| [wt3000_device.py:810](../src/wt3000_scpi/wt3000_device.py#L810) | `int(self._session.query(":STATus:CONDition?"))` |

`wt3000_common` hält für genau diesen Zweck `parse_nr3()`
([wt3000_common.py:139](../src/wt3000_scpi/wt3000_common.py#L139)) bereit: es entfernt
einen etwaigen Kommandokopf und macht aus einem `ValueError` ein `WTError` mit Kontext.
Keine der sechs Stellen benutzt es.

**Wirkung:** Antwortet das Gerät auf `:STATus:CONDition?` unerwartet — mit Header (weil
jemand `:COMMunicate:HEADer 1` gesetzt hat), leer, oder mit einer Mehrfachantwort —
verlässt ein `ValueError` die Kette. Er passiert `except WTError` in allen sieben Skripten.

Die kritischste der sechs Stellen ist `wt3000_measure.py:504`: sie liegt **innerhalb** der
laufenden Messschleife. Ein `ValueError` dort beendet eine womöglich stundenlange
Messreihe mit einem Traceback statt mit dem sauberen Abbruch, für den `_loop_body` sonst
gebaut ist. Die CSV wird über das `finally` in `run_measurement_loop` immerhin geschlossen.

Bemerkenswert: `stage2` und `stage3` prüfen vorher, dass `:COMMunicate:HEADer` auf `0`
steht, und wären damit gedeckt. `stage5`, `stage5b` und beide Werkzeuge prüfen es
**nicht** — sie verlassen sich für alle Antworten auf `strip_response_header()`. Der
Schutz ist also uneinheitlich über die Skripte verteilt, obwohl `check_protocol_state()`
in der Fassade ([wt3000_device.py:780](../src/wt3000_scpi/wt3000_device.py#L780)) längst
der dafür vorgesehene Ort ist (Befund B-14).

**Vorschlag:** `parse_nr3()` bzw. ein neues `parse_condition()` an allen sechs Stellen.
Roadmap: M1-5/S-05, M1-4.

---

#### A-07 — `write_metadata()` schluckt `WTError` und fragt ohne `drain_after_failure()` weiter

**Ort:** [wt3000_measure.py:321–326](../src/wt3000_scpi/wt3000_measure.py#L321)

```python
for key, command in queries.items():
    try:
        device[key] = session.query(command)
    except WTError as error:
        device[key] = f"<Fehler: {error}>"      # und weiter zur naechsten Abfrage
```

Das ist die einzige Stelle im Bestand, an der ein fehlgeschlagener Query nicht zum Abbruch
führt, sondern die nächste Abfrage nach sich zieht. Genau dafür gibt es
`WTSession.drain_after_failure()` ([wt3000_core.py:265](../src/wt3000_scpi/wt3000_core.py#L265))
— und genau hier wird es nicht aufgerufen. Die Methode ist getestet und im gesamten
Produktivcode ungenutzt (S-03).

**Wirkung:** Läuft `:INPut?` — die längste der elf Abfragen — in einen Timeout und trifft
die verspätete Antwort ein, während schon `:INPut:WIRing?` unterwegs ist, dann landet der
`:INPut?`-Rumpf im Feld `input_wiring` der Metadatendatei. Das Sidecar sieht dann
plausibel aus und ist falsch — und es ist die Datei, aus der eine Messreihe später
interpretiert wird.

**Vorschlag:** `session.drain_after_failure()` in den `except`-Zweig. Das ist der von M1-5
verlangte „begründete Produktivpfad" — und der einzige, den der Bestand heute anbietet.
Roadmap: M1-5/S-03.

---

### 3.3 — Wo die Kette anfängt

#### A-08 — `WTConfig.from_environment()` steht in jedem `main()` vor dem `try` und vor `setup_logging()`

**Ort:** [stage2:104](../src/wt3000_scpi/stage2_read_numeric.py#L104),
[stage3:120](../src/wt3000_scpi/stage3_own_itemtable.py#L120),
[stage4:120](../src/wt3000_scpi/stage4_measure.py#L120),
[stage5:42](../src/wt3000_scpi/stage5_input_config.py#L42),
[stage5b:151](../src/wt3000_scpi/stage5b_range_probe.py#L151), beide Werkzeuge

Die Auflösungskette ist der erste Aufruf von Layer 4 nach Layer 0 — und der einzige, der
außerhalb jedes `try` und vor der Einrichtung des Protokolls liegt. Sie kann drei
`WTError` werfen: nicht lesbare Datei, kein JSON-Objekt, nicht auswertbarer Feldwert
([wt3000_transport.py:180, 261–274](../src/wt3000_scpi/wt3000_transport.py#L261)).

**Nachweis:** Reproduktion 7.5. Mit einer kaputten `wt3000.json` bricht `stage5.main()` ab
mit `WTError -> Konfigurationsdatei … ist nicht lesbar: Expecting property name…` —
als Traceback, ohne Protokolldatei, ohne die Zeile `Abbruch: …`, die das Skript für jeden
anderen `WTError` ausgibt.

**Zweiter Teil desselben Befunds:** Die Diagnose, die Layer 0 während der Auflösung selbst
ausgibt — die Warnung über unbekannte Schlüssel in der Konfigurationsdatei,
[wt3000_transport.py:280](../src/wt3000_scpi/wt3000_transport.py#L280) — fällt aus
demselben Grund neben das Protokoll.

**Nachweis:** Reproduktion 7.6. Die Warnung erscheint über `logging.lastResort` auf
stderr, ohne Zeitstempel und ohne Loggernamen, und steht **nicht** in der Protokolldatei:

```
Konfigurationsdatei …/wt3000.json: unbekannte Schluessel uebergangen: tippfehler_feld
--- Inhalt der Protokolldatei ---
2026-08-20 13:26:45,293 INFO    wt3000.demo        ab hier wird protokolliert
```

Ein Tippfehler in `wt3000.json` — der häufigste Konfigurationsfehler überhaupt — ist im
archivierten Lauf also unsichtbar.

**Vorschlag:** `setup_logging()` vor `WTConfig.from_environment()` ziehen (der Dateiname
des Protokolls hängt nur vom Zeitstempel und von `output_dir()` ab, nicht von der Config)
und die Auflösung in das `try` aufnehmen. Beides sind Umstellungen von je zwei Zeilen und
gelten für alle sieben Skripte gleichermaßen.

---

#### A-09 — Kein `main()` nimmt eine `WTConfig` entgegen

Nur `stage5b.main(enable_write_probe=False)` hat überhaupt einen Parameter. Alle anderen
`main()` beziehen ihre gesamte Eingabe aus verstecktem Prozesszustand: Umgebungsvariablen,
Arbeitsverzeichnis (über `config_search_paths()` **und** unabhängig davon über
`find_project_root()`), und Modulkonstanten im Dateikopf.

**Wirkung, zweifach:**

* **Reproduzierbarkeit.** Aus dem Aufruf `python -m wt3000_scpi.stage4_measure` lässt sich
  nicht ablesen, gegen welches Gerät gemessen wurde. Das Protokoll hilft nur begrenzt:
  `WTConfig.describe()` wird von keinem Stufenskript aufgerufen. Die Fassade macht es
  besser — `WT3000.connect()` nimmt `ip`, `dll_path`, `timeout_ms` und `use_remote` als
  Parameter entgegen.
* **`use_remote` als stiller Schalter.** `config.use_remote` steuert in Stufe 2, 3 und 4,
  ob `:COMMunicate:REMote ON` hinausgeht — also ob das Bedienfeld während des Laufs
  gesperrt ist. Der Wert kommt aus der Umgebung oder aus `wt3000.json`; ein Anwender, der
  ihn dort einmal gesetzt hat, sieht am Aufruf nicht mehr, dass er wirkt. Für eine
  Integrationsmessung über Stunden ist genau das die Entscheidung, die
  [wt3000_transport.py:100–107](../src/wt3000_scpi/wt3000_transport.py#L100) selbst als
  *„an der Aufrufstelle zu dokumentieren"* bezeichnet.

**Vorschlag:** `main(config: WTConfig | None = None)` überall; `None` heißt weiterhin
`from_environment()`. Das kostet eine Zeile je Skript, macht alle fünf Stufen testbar
(A-11) und ist die Vorarbeit für die gemeinsame Kommandozeile. Roadmap: M5-2.

---

#### A-10 — `OUTPUT_DIR` wird zur Importzeit ausgewertet, und zwei Stufen machen es anders

**Ort:** [stage4:73](../src/wt3000_scpi/stage4_measure.py#L73),
[stage5:30](../src/wt3000_scpi/stage5_input_config.py#L30),
[stage5b:62](../src/wt3000_scpi/stage5b_range_probe.py#L62), beide Werkzeuge —
gegen [stage2:109](../src/wt3000_scpi/stage2_read_numeric.py#L109) und
[stage3:125](../src/wt3000_scpi/stage3_own_itemtable.py#L125)

Fünf Skripte legen `OUTPUT_DIR: Path = output_dir(...)` als Modulkonstante an, zwei rufen
`output_dir()` innerhalb von `main()`. Zwei Folgen:

* **Der Import tut etwas.** `output_dir()` läuft über `find_project_root()`, das vom
  Arbeitsverzeichnis aus aufwärts `exists()` auf drei Marker prüft. Das ist ein
  Dateisystemzugriff beim bloßen Import — in leichtem Widerspruch zur Zusage von
  `test_stufenskripte_fuehren_beim_import_nichts_aus`
  ([test_package_layout.py:122](../tests/test_package_layout.py#L122)): *„Layer 4 darf
  erst über `main()` aktiv werden, nicht beim Import."*
* **Zwei Suchen nach oben, die auseinanderlaufen können.** `config_search_paths()` sucht
  aufwärts nach `wt3000.json`; `find_project_root()` sucht aufwärts nach `pyproject.toml`
  **oder** `.git` **oder** `wt3000.json` ([wt3000_common.py:209](../src/wt3000_scpi/wt3000_common.py#L209)).
  Im Normalfall ist das dasselbe Verzeichnis. Wird ein Skript aus einem Unterprojekt mit
  eigener `pyproject.toml` gestartet, liest es die Konfiguration von weiter oben und legt
  die Ausgabe weiter unten ab — genau die Sorte Abweichung, wegen der beide Funktionen
  überhaupt entstanden sind.

**Vorschlag:** `output_dir()` einheitlich in `main()` aufrufen (die Konstante bleibt als
Vorgabewert erhalten), und im Protokollkopf beide aufgelösten Pfade ausgeben — Herkunft
der Konfiguration und Ziel der Ausgabe.

---

### 3.4 — Was die Kette nicht absichert

#### A-11 — Die fünf Stufenskripte sind genau die Module ohne erzwungene Importrichtung

**Ort:** [test_package_layout.py:25](../tests/test_package_layout.py#L25) und
[:108](../tests/test_package_layout.py#L108)

`test_importrichtung_zeigt_nach_unten` ist über `sorted(LAYERS)` parametrisiert. `LAYERS`
enthält 11 Einträge, das Paket hat 16 Module. Die fehlenden fünf sind exakt die
Stufenskripte:

```
Module gesamt      : 16
In LAYERS geprueft : 11
NICHT geprueft     : ['stage2_read_numeric', 'stage3_own_itemtable', 'stage4_measure',
                      'stage5_input_config', 'stage5b_range_probe']
```

**Nachweis:** Reproduktion 7.7.

**Wirkung:** Ein Stufenskript darf heute `wt3000_device` importieren, oder ein anderes
Stufenskript, ohne dass ein Test anschlägt. Der `LAYERS`-Kommentar hält für die Fassade
ausdrücklich fest, dass sie *„aus keinem Stufenskript und aus keinem zweiten
Layer-4-Modul"* importieren darf — für die Stufenskripte selbst gilt diese Regel nicht,
obwohl sie dieselbe Schicht bewohnen. Der Test, der die Schichtung trägt, lässt genau die
Module aus, um die es in dieser Analyse geht.

Der zweite Test greift zwar: `test_kein_absoluter_geschwisterimport` läuft über alle
`*.py` (`modul_dateien()`) — die Stufenskripte sind also gegen absolute Importe
abgesichert, nur nicht gegen die Richtung.

**Vorschlag:** Fünf Einträge in `LAYERS` ergänzen. Die heutigen Importe sind bereits
korrekt (Abschnitt 1), der Test wäre also sofort grün — er sichert dann nur den Zustand.
Aufwand: fünf Zeilen.

---

#### A-12 — Layer 0 wird ausschließlich über die Weiterleitung in `wt3000_core` erreicht

**Ort:** [wt3000_core.py:21–48](../src/wt3000_scpi/wt3000_core.py#L21)

Eine Suche über den gesamten Quellbaum:

| Ort | importiert direkt aus `wt3000_transport` |
|---|---|
| `wt3000_core.py` | die Weiterleitung selbst |
| `__init__.py` | nur `FakeTransport` |
| 6 Testmodule | ja |
| **alle 7 ausführbaren Skripte** | **nein** — über `wt3000_core` |
| **`wt3000_device.py`** ([:53](../src/wt3000_scpi/wt3000_device.py#L53)) | **nein** — über `wt3000_core` |

Kein produktives Modul außer der Weiterleitung selbst nennt Layer 0 beim Namen. Die
Weiterleitung ist bewusst gebaut und gut begründet — sie hat bei M1-2 die bestehenden
Importe wortgleich weiterlaufen lassen. Nach der Umstellung ist sie aber niemals
zurückgebaut worden, und damit gilt heute:

* Die Trennung von Layer 0 und Layer 1, die M1-2 eingeführt hat, ist an der Aufrufstelle
  unsichtbar. Wer `stage4_measure.py` liest, sieht `from .wt3000_core import
  TmctlTransport, WTConfig` und muss wissen, dass beide eine Schicht tiefer wohnen.
* `LAYERS["wt3000_device"]` erlaubt `wt3000_transport` ausdrücklich — die Fassade benutzt
  die Erlaubnis nicht.
* Der Tag, an dem die Weiterleitung fällt (ein naheliegender Aufräumschritt), bricht acht
  Dateien auf einmal. Für die fünf Stufenskripte würde **kein** Test das vorher melden
  (A-11).

**Vorschlag:** Entweder die Weiterleitung als dauerhaften Teil der Schnittstelle
festschreiben — dann gehört das in den `__all__`-Kommentar von `wt3000_core` als Zusage,
nicht als Übergangsbegründung — oder die acht Importe auf `wt3000_transport` umstellen und
`__all__` in `wt3000_core` auf die eigenen Namen kürzen. Der zweite Weg macht die
Schichtung am Dateikopf lesbar; das war der erklärte Zweck von M1-2.

---

#### A-13 — Vier von fünf Stufenskripten sind nicht durchspielbar wie Stufe 5b

[`test_stage5b_write_probe.py`](../tests/test_stage5b_write_probe.py) zeigt, dass ein
`main()` vollständig gegen `FakeTransport` laufen kann. Die Vorrichtung braucht drei
Ersetzungen im Modulnamensraum:

```python
monkeypatch.setattr(stage5b, "TmctlTransport", lambda _config: transport)
monkeypatch.setattr(stage5b, "OUTPUT_DIR",     tmp_path)
monkeypatch.setattr(stage5b, "setup_logging",  lambda _pfad: None)
```

Für Stufe 4, Stufe 5 und beide Werkzeuge trägt dasselbe Rezept unverändert. Für **Stufe 2
und Stufe 3** trägt es nicht: sie haben kein `OUTPUT_DIR`, sondern rufen `output_dir()`
innerhalb von `main()` auf (A-10) — dort wäre `stage2.output_dir` zu ersetzen, ein
anderer Name.

Ergebnis: Von den fünf Stufenskripten ist heute genau eines geprüft. Die vier ungeprüften
sind die, die schreiben — Item-Tabelle (Stufe 3, 4) und `:NUMeric:HOLD` (Stufe 4). Die
Befunde A-01 und A-06 sitzen alle in dieser ungeprüften Menge; A-01 ließe sich mit
derselben Vorrichtung als Test formulieren, mit dem Prüfsatz *„nach `main()` steht
`:COMMunicate:REMote OFF` in `transport.written`"* — unabhängig davon, wie der Lauf
ausgegangen ist.

**Vorschlag:** `OUTPUT_DIR`-Konstante in Stufe 2 und 3 nachziehen (A-10), dann die
Vorrichtung aus `test_stage5b_write_probe.py` in `conftest.py` heben und für alle fünf
Stufen anwenden. Roadmap: M5-4.

---

### 3.5 — Kleinere Befunde

#### A-14 — Stufe 2 sperrt das Bedienfeld und öffnet eine zweite Verbindung, ohne etwas zu schreiben

**Ort:** [stage2_read_numeric.py:122–125](../src/wt3000_scpi/stage2_read_numeric.py#L122)
und [:166–184](../src/wt3000_scpi/stage2_read_numeric.py#L166)

Der Dateikopf sagt: *„Diese Stufe verändert die Item-Tabelle NICHT."* Trotzdem öffnet sie
die Sitzung mit `read_only=False` und sendet `:COMMunicate:REMote ON`. Stufe 5 löst
dieselbe Aufgabe — reines Lesen — mit `read_only=True` und einer ausdrücklichen Warnung,
dass `use_remote` ignoriert wird ([stage5:59](../src/wt3000_scpi/stage5_input_config.py#L59)).
Für einen Lauf, der nichts schreibt, ist Stufe 5 die richtige Haltung.

Dazu kommt: Das äußere `finally` baut eine **zweite** TMCTL-Verbindung auf, um
`restore_to_device()` aufzurufen. Da Stufe 2 nichts geschrieben hat, findet dieser Aufruf
keine Abweichung und schreibt nichts (`EXERCISE_RESTORE_WRITE` ist `False`). Jeder Lauf
kostet damit einen zusätzlichen `TmcInitialize`, ein `REMote ON`/`OFF`-Paar und ein
`:NUMeric:NORMal?` — für eine Wiederherstellung, die nichts wiederherstellt. Stufe 3 und 4
machen es richtig und stellen in derselben Sitzung zurück, mit der ausdrücklichen
Begründung *„die Verbindung steht noch, das ist zuverlässiger als ein zweiter Aufbau"*.

**Vorschlag:** `read_only=True` in Stufe 2, solange `EXERCISE_RESTORE_WRITE` auf `False`
steht; das zweite Verbindungspaar entfällt dann mit.

---

#### A-15 — „Schreibt nichts" deckt die Fehlerqueue nicht

**Ort:** [wt3000_core.py:277–284](../src/wt3000_scpi/wt3000_core.py#L277),
aufgerufen aus [stage5:94](../src/wt3000_scpi/stage5_input_config.py#L94) und
[stage5b:191](../src/wt3000_scpi/stage5b_range_probe.py#L191)

Beide Skripte tragen im Kopf die Zusage „SCHREIBT NICHTS" und setzen sie mit
`read_only=True` durch. `assert_no_error()` → `read_error_queue()` sendet aber bis zu
20 mal `:STATus:ERRor?`, und der Docstring hält selbst fest: *„`:STATus:ERRor?` entfernt
den Eintrag."* Ein reiner Lesevorgang verändert damit den Gerätezustand — er leert die
Fehlerqueue, die eine parallele Sitzung oder ein späterer Anwender noch gebraucht hätte.

Das ist kein Fehler, sondern eine Grenze der Zusage. Sie ist heute nirgends benannt.
`read_only` sperrt SCPI-Set-Kommandos; „ändert nichts am Gerät" ist etwas anderes.

**Vorschlag:** Den Dateikopf von Stufe 5 und 5b um einen Satz ergänzen, und im Docstring
von `read_only` festhalten, was die Sperre abdeckt und was nicht.

---

#### A-16 — `WTSession` verlangt eine ganze `WTConfig` für drei Zahlen

**Ort:** [wt3000_core.py:112](../src/wt3000_scpi/wt3000_core.py#L112)

`WTSession.__init__(transport, config, read_only)` benutzt aus `config` genau drei Felder:
`read_buffer_size` ([:216](../src/wt3000_scpi/wt3000_core.py#L216)), `drain_timeout_ms`
und `timeout_ms` ([:268, :272](../src/wt3000_scpi/wt3000_core.py#L268)). Die übrigen sechs
Felder beschreiben eine DLL, eine IP und Zugangsdaten — Dinge, die Layer 1 nichts angehen.

Für den vorgesehenen `SocketTransport` bedeutet das: Der Aufrufer muss ein `WTConfig` mit
einem `dll_path` bauen, den niemand benutzt. Die Fassade zeigt das schon heute — sie legt
bei `from_transport()` ohne Config ein leeres `WTConfig()` an
([wt3000_device.py:574](../src/wt3000_scpi/wt3000_device.py#L574)), nur damit `WTSession`
etwas bekommt.

Das ist kein akuter Befund, sondern eine Fuge, die vor dem Bau des zweiten Transports zu
entscheiden ist: entweder `WTSession` bekommt die drei Werte einzeln, oder `WTConfig`
trennt Transportparameter von Sitzungsparametern. Roadmap: M1-2 (offene Fugen), M1-5.

---

#### A-17 — Vier Stellen, an denen die Dokumentation dem Code nicht mehr entspricht

Für jeden, der die Aufrufkette anhand der Dokumentation nachvollzieht, sind das
Stolperstellen:

| Stelle | Aussage | Stand im Code |
|---|---|---|
| [README.md:304](../README.md#L304) | *„`wt3000_rangeio` sendet `1000`, `wt3000_input` sendet `1000V`. Höchstens eine Form kann richtig sein"* | `wt3000_input` sendet seit der Stilllegung von `format_voltage()` ebenfalls `format_nrf()` — siehe [wt3000_input.py:370–390](../src/wt3000_scpi/wt3000_input.py#L370) und den Kommentar in [:779](../src/wt3000_scpi/wt3000_input.py#L779) *(„am Geraet belegt: '1000', nicht '1000V'")*. Der Widerspruch besteht nicht mehr. |
| README.md, 6 Links | `(ROADMAP.md)`, `(AENDERUNGEN_2026-08-18.md)`, `(WT3000_Commands_Overview.md)` | Die Dateien liegen seit Commit `0a415a2` unter `MarkDowns/`. Alle sechs Links gehen ins Leere. `OFFENE_PUNKTE.md` ist in der Dokumentationstabelle gar nicht aufgeführt. |
| [README.md:70](../README.md#L70), [:272](../README.md#L272) | *„241 Tests"* | 306 |
| [wt3000_numeric.py:3](../src/wt3000_scpi/wt3000_numeric.py#L3) | Dateikopf: *„Layer 3 — Messwert-Layer"* | `__init__.py` und `LAYERS` ordnen das Modul Layer 2 zu. Gleiches Muster in [wt3000_measure.py:140](../src/wt3000_scpi/wt3000_measure.py#L140) (*„Layer 4 — der Datensatz"*, tatsächlich Layer 3). |

---

## 4 — Sitzungsposition der sieben ausführbaren Skripte

Dieselben vier Aufrufe nach Layer 0/1, siebenmal verschieden:

| Skript | `read_only` | `enable_remote()` | `disable_remote()` | Wiederherstellung |
|---|---|---|---|---|
| `stage2` | `False` ⚠ A-14 | wenn `use_remote` | eigenes `finally` ✔ | **zweite Verbindung** ⚠ A-14 |
| `stage3` | `False` | wenn `use_remote` | nach `try/except` ⚠ **A-01** | dieselbe Sitzung ✔ |
| `stage4` | `False` | wenn `use_remote` | nach `try/except` ⚠ **A-01** | dieselbe Sitzung ✔ |
| `stage5` | `True` ✔ | nein, mit Warnung ✔ | nicht nötig | schreibt nicht |
| `stage5b` | `not --write-probe` ✔ | **nie**, begründet ✔ | nicht nötig | Nulleffekt + `diff` ✔ |
| `probe_voltage_range` | `False` | **nie**, unbegründet ⚠ A-02 | **nie** | **ohne `finally`** ⚠ **A-02** |
| `probe_current_range` | `False` | **nie**, unbegründet ⚠ A-02 | **nie** | **ohne `finally`** ⚠ **A-02** |
| `WT3000` (Fassade) | `True` (Vorgabe) ✔ | nur wenn `not read_only` ✔ | `close()` + `except BaseException` ✔ | `applied_ranges()` / `applied()` ✔ |

Die Fassade ist in jeder Spalte die beste Fassung. Sie ist gleichzeitig die einzige, die
kein Stufenskript benutzt — was der historische Grund ist (die Stufen sind älter), aber
kein bleibender.

---

## 5 — Was trägt

Damit die Befundliste nicht das falsche Bild ergibt — folgendes ist beim Nachvollziehen
der Kette ausdrücklich aufgefallen:

* **`_assemble_block()`** ([wt3000_core.py:167–239](../src/wt3000_scpi/wt3000_core.py#L167))
  hält seine Zusage vollständig: jeder Formfehler einer Blockantwort — fehlender Header,
  abgeschnittener Kopf, unplausible Länge, Ziffern die keine sind — verlässt die Methode
  als `ProtocolError`. Das ist die einzige Stelle im Bestand, an der die Übersetzung nach
  `WTError` lückenlos durchgezogen ist, und sie ist der Maßstab für A-04 bis A-06.
* **`_validate()`** prüft die Query-Regeln vor dem Senden, nicht danach. Ein
  `ReadOnlyViolation` erreicht die Leitung nie.
* **Die Auflösungskette** in `WTConfig` ist sorgfältig und gut begründet; die
  Aufwärtssuche nach `wt3000.json` und die dateirelative Auflösung von `dll_path` lösen
  reale Startverzeichnis-Fehler. Der Befund A-08 betrifft nicht die Kette, sondern ihre
  Position im Ablauf.
* **`run_measurement_loop()`** trennt Lebenszyklus der Senke (`finally`) von der Schleife
  sauber; `sink.close()` ist auch bei Strg+C zugesagt und wird eingehalten.
* **`test_stage5b_write_probe.py`** ist die richtige Bauform für Stufenskript-Tests und
  sollte das Muster für die übrigen vier sein (A-13).

---

## 6 — Vorgeschlagene Reihenfolge

Sortiert nach Verhältnis von Gerätewirkung zu Aufwand, nicht nach Abschnittsnummer:

| # | Befund | Aufwand | Warum zuerst |
|---|---|---|---|
| 1 | **A-02** — `try/finally` in beide `tools/hardware/`-Skripte | XS | Sie schreiben einen Messbereich am eingemessenen Gerät, ohne Rückstellgarantie. Und sie sind das Werkzeug für den anstehenden Gerätetermin. |
| 2 | **A-01** — `disable_remote()` in Stufe 3 und 4 in ein eigenes `finally` | XS | Gesperrtes Bedienfeld; Stufe 2 zeigt die Lösung eine Datei weiter. |
| 3 | **A-08** — `setup_logging()` vor `from_environment()`, Auflösung ins `try` | XS | Der häufigste Konfigurationsfehler ist heute weder gefangen noch protokolliert. |
| 4 | **A-11** — fünf `LAYERS`-Einträge nachziehen | XS | Sofort grün; sichert danach genau die Module, um die es hier geht. |
| 5 | **A-04**, **A-06** — rohe Fehlerwege in `WTError` übersetzen | S | Macht `except WTError` in allen sieben Skripten erst zu dem, wofür es dasteht. Roadmap M1-5. |
| 6 | **A-03** — `set_range()`/`get_range()` über `expand_scope()` | S | Schließt den in Abschnitt 2 beschriebenen Grundriss an einer Stelle, an der es nichts kostet. Roadmap M1-3. |
| 7 | **A-07** — `drain_after_failure()` in `write_metadata()` | S | Der einzige Ort im Bestand, an dem ein fehlgeschlagener Query von einem weiteren gefolgt wird. Roadmap M1-5/S-03. |
| 8 | **A-09**, **A-10**, **A-13** — `main(config=None)`, `OUTPUT_DIR` vereinheitlichen, Testvorrichtung heben | M | Zusammen ein Schritt; danach sind alle fünf Stufen prüfbar und A-01 wird zum Test statt zur Notiz. Roadmap M5-2/M5-4. |
| 9 | **A-12** — Weiterleitung entscheiden | M | Kein akuter Fehler, aber der Punkt, an dem die Schichtung wieder ablesbar wird. |
| 10 | **A-17** — Dokumentation nachziehen | XS | Sechs tote Links und eine Einschränkung, die es nicht mehr gibt. |

A-05, A-14, A-15 und A-16 sind Entscheidungen, keine Reparaturen — sie gehören in die
jeweiligen Roadmap-Punkte (M1-5, M1-2), nicht in einen eigenen Schritt.

---

## 7 — Anhang: Reproduktionen

Alle Läufe stammen vom 2026-08-20, Commit `7bfd5e7`, mit `python3.12` und
`PYTHONPATH=src`. Keiner braucht ein Gerät.

### 7.1 — A-01: REMOTE bleibt stehen

Die Layer-3-Schritte werden ersetzt, damit `main()` bis in das `finally` läuft; der
Restore wirft einen Nicht-`WTError`:

```python
s3.probe_item_write_capability = lambda *a, **k: (_ for _ in ()).throw(WTError("Abbruch"))
s3.restore_item_table          = lambda *a, **k: (_ for _ in ()).throw(KeyError("Nicht-WTError"))
```

```
main() bricht ab mit: KeyError -> 'simulierter Nicht-WTError beim Restore'
Gesendete Set-Kommandos: [':COMMunicate:REMote ON']
REMote OFF gesendet?    False
```

### 7.2 — A-03: `set_range()` ohne Elementprüfung

```
elements: (1, 2, 3, 4)
set_range auf Element 7 -> :INPut:VOLTage:RANGe:ELEMent7 1000
expand_scope(7)  -> WTError : Element 7 existiert nicht (vorhanden: (1, 2, 3, 4))
```

### 7.3 — A-04: Konstruktorfehler ist kein `WTError`

```
config: 1.2.3.4, ohne Anmeldung, DLL tmctl64.dll
NICHT WTError -> AttributeError : module 'ctypes' has no attribute 'WinDLL'
```

### 7.4 — A-05: `KeyError` aus `FakeTransport` verlässt `main()`

`stage5b.main()` gegen eine Antworttabelle ohne `:INPut:POVer`:

```
main() bricht ab mit: KeyError -> "FakeTransport hat keine Antwort fuer ':INPut:POVer?'.
                                   Eintrag in 'responses' ergaenzen oder den Aufruf pruefen."
```

### 7.5 — A-08: kaputte `wt3000.json`

```
main() bricht ab mit: WTError -> Konfigurationsdatei /…/wt3000.json ist nicht lesbar:
                                 Expecting property name enclosed in double quotes: line 1 column 3
```

### 7.6 — A-08: Warnung der Auflösungskette fehlt im Protokoll

`wt3000.json` mit einem Schlüssel `tippfehler_feld`, Ablauf wie in jedem Stufenskript
(erst `from_environment()`, dann `setup_logging()`):

```
Konfigurationsdatei …/wt3000.json: unbekannte Schluessel uebergangen: tippfehler_feld
2026-08-20 13:26:45,293 INFO    wt3000.demo        ab hier wird protokolliert
--- Inhalt der Protokolldatei ---
2026-08-20 13:26:45,293 INFO    wt3000.demo        ab hier wird protokolliert
```

### 7.7 — A-11: Deckung von `LAYERS`

```
Module gesamt      : 16
In LAYERS geprueft : 11
NICHT geprueft     : ['stage2_read_numeric', 'stage3_own_itemtable', 'stage4_measure',
                      'stage5_input_config', 'stage5b_range_probe']

  stage2_read_numeric   importiert ['wt3000_common', 'wt3000_core', 'wt3000_numeric']
  stage3_own_itemtable  importiert ['wt3000_common', 'wt3000_core', 'wt3000_itemspec', 'wt3000_numeric']
  stage4_measure        importiert ['wt3000_common', 'wt3000_core', 'wt3000_itemspec',
                                    'wt3000_measure', 'wt3000_numeric', 'wt3000_sinks']
  stage5_input_config   importiert ['wt3000_common', 'wt3000_core', 'wt3000_input']
  stage5b_range_probe   importiert ['wt3000_common', 'wt3000_core', 'wt3000_rangeio', 'wt3000_ranging']
```

---

## 8 — Verweise

* [OFFENE_PUNKTE.md](OFFENE_PUNKTE.md) — S-01 (Elementliste), S-03 (`drain_after_failure`),
  S-05 (Fehlersemantik) und S-06 (Ablaufwissen in den Stufenskripten) sind die
  allgemeinen Fassungen von A-03, A-07, A-04/A-05/A-06 und A-09/A-10/A-13.
* [ROADMAP.md](ROADMAP.md) — M1-3, M1-4, M1-5, M5-2, M5-4.
* [AENDERUNGEN_2026-08-19_M1-1.md](AENDERUNGEN_2026-08-19_M1-1.md) — P-1 hat den
  REMOTE-Fall für die Fassade gelöst; A-01 ist derselbe Fall in den Stufenskripten.
