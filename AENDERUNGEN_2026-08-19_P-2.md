# P-2 — Misslungene Wiederherstellung der Item-Tabelle wird gemeldet

**Datum:** 2026-08-19
**Bezug:** [PLAN_BEFUNDE_2026-08-19.md](PLAN_BEFUNDE_2026-08-19.md) P-2 · Befund BF-H2 · [Befund.md](Befund.md)
**Stand vorher:** 182 Tests grün · **Stand nachher:** 186 Tests grün, weiterhin ohne Gerät und ohne `tmctl.dll`, `pyflakes` ohne Meldung

---

## 1 — Das Problem

`ItemAccess.applied()` verspricht im Docstring *„Ausgangszustand garantiert
zurueck"*. Die Wiederherstellung lief zwar im `finally` — also auch bei Strg+C —,
ein Fehler dabei wurde aber nur protokolliert und dann verschluckt:

```python
except WTError as error:
    _log.error("Wiederherstellung der Item-Tabelle fehlgeschlagen: %s - Backup: %s", ...)
    # kein raise
```

Damit konnte ein Aufrufer den Kontextmanager **ohne Ausnahme** verlassen, obwohl die
Item-Tabelle noch auf der Zieltabelle stand. Es gab auch keinen zweiten Weg, das zu
erfahren: `applied()` gibt die `ItemTable` heraus, kein Report-Objekt mit einem
Statusfeld. Wer nicht zufällig ins Protokoll sah, hat es nicht gemerkt — und maß
weiter gegen eine Tabelle, die er für zurückgesetzt hielt.

Das stärkste Argument liefert das Projekt selbst: `applied_ranges()` in
[`wt3000_ranging.py:641`](src/wt3000_scpi/wt3000_ranging.py) löst in derselben
Situation seit jeher erneut aus. Zwei Kontextmanager mit demselben Zweck, derselben
Struktur und verschiedenem Verhalten im Fehlerfall — der schwächere war der neuere.

---

## 2 — Was geändert wurde

Alles in [`wt3000_device.py:326–366`](src/wt3000_scpi/wt3000_device.py).

### 2.1 Der Fehler wird weitergereicht
Nach dem Protokolleintrag folgt jetzt ein `raise` — wortgleich zum Vorbild in
`applied_ranges()`. Die beiden Abläufe verhalten sich damit gleich.

### 2.2 Gegenprobe nach dem Zurückschreiben
Neu ist ein `self.verify(backup)` unmittelbar nach dem Restore. Das schließt die
zweite, unauffälligere Hälfte derselben Lücke: das Gerät quittiert Set-Kommandos
nicht, ein Zurückschreiben kann also ohne jeden Fehler durchlaufen und trotzdem
nicht gewirkt haben.

Findet die Gegenprobe Abweichungen, werden sie einzeln protokolliert und als
`WTError` gemeldet. **Hier weiche ich bewusst vom Plantext ab**, der nur
Protokollieren vorsah: `applied_ranges()` kann sich damit begnügen, weil es einen
`RangeReport` herausgibt, in dem der Aufrufer nach dem Block nachsehen kann. Bei
`applied()` gibt es kein solches Objekt — eine bloß protokollierte Abweichung wäre
also wieder unbemerkbar gewesen, dieselbe Falle eine Ebene tiefer. Im Erfolgsfall
steht eine Info-Zeile im Protokoll, wie es Stufe 3 und Stufe 4 von Hand tun.

### 2.3 Fehlerverkettung
Ohne Zusatzaufwand: eine im `finally` ausgelöste Ausnahme trägt eine bereits
unterwegs befindliche automatisch als `__context__` mit. Schlägt also erst der
Nutzblock fehl und dann die Wiederherstellung, zeigt der Traceback beide. Damit ist
die Anforderung aus `Befund.md` erfüllt — *„sollten beide Fehler erhalten bleiben"* —
ohne Abhängigkeit von Python 3.11 (`add_note`), was bei `requires-python = ">=3.10"`
auch nicht ginge.

### 2.4 Was bewusst nicht gemacht wurde
Das in `Befund.md` alternativ vorgeschlagene **Report-Objekt analog zu `RangeReport`**.
Es würde den Rückgabetyp von `applied()` brechen — der Kontextmanager liefert heute
die `ItemTable`, und die braucht der Nutzblock. Der Nutzen über das erneute Auslösen
hinaus wäre gering. Falls die Auswertung später doch gewünscht ist, gehört sie in
ROADMAP M2-4, wo die drei Sicherungsformate ohnehin zusammengeführt werden.

### 2.5 Dokumentation
Docstring von `applied()` sagt jetzt, was „garantiert" im Fehlerfall bedeutet.
[README.md](README.md) im Abschnitt *Sicherheitskonzept* um zwei Sätze ergänzt.

---

## 3 — Prüfung

Vier neue Fälle in [tests/test_device_facade.py](tests/test_device_facade.py). Dafür
zwei kleine Gerätemodelle, die die beiden Arten des Misslingens nachstellen — das
Kommando kommt gar nicht durch, oder es kommt durch und wirkt nicht:

| Modell | Verhalten |
|---|---|
| `BreakableItemTransport` | ab `break_writes = True` scheitert jeder Schreibzugriff auf die Tabelle mit `TmctlError` — der abgerissene Verbindungsweg |
| `IgnoringItemTransport` | ab `ignore_writes = True` werden Schreibzugriffe angenommen, aber nicht übernommen — der stille Fehlschlag |

| Test | prüft |
|---|---|
| `test_misslungener_restore_wird_gemeldet_statt_verschluckt` | Nutzblock läuft sauber, Restore scheitert → `WTError` verlässt den `with` |
| `test_stiller_restore_ohne_wirkung_wird_von_der_gegenprobe_gefunden` | Restore ohne Fehler, Zustand trotzdem falsch → Gegenprobe meldet es; Beleg: `transport.number == 4` statt 3 |
| `test_fehler_im_nutzblock_und_im_restore_bleiben_beide_erhalten` | `__context__` trägt die `ZeroDivisionError` aus dem Nutzblock |
| `test_gelungener_restore_wird_durch_die_gegenprobe_bestaetigt` | Regelfall: keine Ausnahme, „Restore-Kontrolle" im Protokoll |

**Gegenprobe durchgeführt.** Mit vorübergehend zurückgebautem `finally` fallen alle
vier durch:

```
FAILED test_misslungener_restore_wird_gemeldet_statt_verschluckt
FAILED test_stiller_restore_ohne_wirkung_wird_von_der_gegenprobe_gefunden
FAILED test_fehler_im_nutzblock_und_im_restore_bleiben_beide_erhalten
FAILED test_gelungener_restore_wird_durch_die_gegenprobe_bestaetigt
```

Die bestehenden `applied()`-Tests laufen unverändert durch — die Gegenprobe schlägt
im Regelfall nicht an.

```
186 passed
pyflakes: keine Meldung
```

---

## 4 — Auswirkung auf bestehenden Code

**Keine.** `ItemAccess.applied()` wird bisher nirgends im Projekt aufgerufen —
Stufe 3 und Stufe 4 bauen den Ablauf weiter von Hand nach und benutzen
`restore_item_table()` unmittelbar. Die einzige Erwähnung außerhalb der Tests steht
in der README.

Für künftige Aufrufer ist es eine **Verhaltensänderung**: ein Fehlschlag der
Wiederherstellung kommt ab jetzt als Ausnahme heraus. Das ist der Zweck der
Änderung, gehört aber beim Umstellen von Stufe 3 und Stufe 4 auf die Fassade
beachtet.

---

## 5 — Was offen bleibt

* **Paket A des Plans** ist zur Hälfte erledigt. Offen: P-3 (CSV-Zeile gegen den
  Kopf absichern) und P-4 (Blockheader vollständig validieren).
* **Nebenbefund, nicht behoben:** `applied_ranges()` meldet zwar Fehler beim
  Zurückschreiben, aber Abweichungen der eigenen Restore-Kontrolle
  (`report.restore_problems`) nur ins Protokoll. Dort ist das vertretbar, weil der
  `RangeReport` nach dem Block auswertbar bleibt — es setzt aber voraus, dass der
  Aufrufer hineinsieht. Ob das reicht, ist eine Entscheidung wie B-02 im
  Analysedokument und gehört zu ROADMAP M2-4, nicht in diesen Durchgang.
