# P-4 — Blockheader vollständig validieren

**Datum:** 2026-08-19
**Bezug:** [PLAN_BEFUNDE_2026-08-19.md](PLAN_BEFUNDE_2026-08-19.md) P-4 · Befund BF-M3 · [Befund.md](Befund.md)
**Stand vorher:** 193 Tests grün · **Stand nachher:** 204 Tests grün, weiterhin ohne Gerät und ohne `tmctl.dll`, `pyflakes` ohne Meldung

**Damit ist Paket A des Plans abgeschlossen.**

---

## 1 — Das Problem

`WTSession._assemble_block()` sicherte die Ziffernanzahl des Blockheaders ab
(`#4…` → `int(raw[1:2])` in einem `try`), das **Längenfeld** dahinter aber nicht:

```python
header_length = 2 + digit_count
payload_length = int(raw[2:header_length])   # ungeschützt
```

Zwei nachvollziehbare Auslöser, beide aus einer gestörten Verbindung oder einem
gestörten Gerät:

* Die Antwort bricht nach dem Kopf ab: `b"#4"` → `raw[2:6]` ist leer →
  `int(b"")` → `ValueError`
* Das Längenfeld ist nicht numerisch: `b"#4AB12"` → `ValueError`

Der `ValueError` ist kein `WTError`. Sämtliche Stufenskripte fangen aber genau nur
`WTError` — der Fehler lief also an ihrer Fehlerbehandlung vorbei. Das `finally`
mit der Wiederherstellung greift zwar weiterhin, aber die Fehlersemantik war
inkonsistent: dieselbe Ursache (unbrauchbare Blockantwort) kam einmal als
`ProtocolError` heraus und einmal als nackter `ValueError`.

---

## 2 — Was geändert wurde

Alles in [`wt3000_core.py`](src/wt3000_scpi/wt3000_core.py).

### 2.1 Abgeschnittener Kopf (`:192`)
Vor dem Zugriff wird geprüft, ob `raw` überhaupt `header_length` Bytes hat. Ohne
das liefert der Schnitt stillschweigend zu wenige oder gar keine Bytes. Die Meldung
nennt die angekündigte Ziffernzahl, die tatsächliche Länge und die ersten Bytes.

### 2.2 Nichtnumerisches Längenfeld (`:202`)
Die Umwandlung steht jetzt in einem eigenen `try` mit eigener Meldung — nach
demselben Muster wie die bestehende Absicherung der Ziffernanzahl darüber, also
mit den Rohbytes im Text.

### 2.3 Unplausible Längen (`:221`)
Der Punkt, den der Plan zusätzlich verlangt hat. Zwei Fälle, beide **vor** der
Nachlese-Schleife abgefangen:

**Negative Länge** ist der unangenehmere. `b"#4-100"` ergibt `payload_length = -100`.
Die Schleifenbedingung `len(payload) < payload_length` ist dann sofort falsch, die
Schleife läuft gar nicht erst an — und `payload[:-100]` schneidet am **Ende** statt
am Anfang. Heraus käme ein stillschweigend gekürzter Block, der wie ein Ergebnis
aussieht. Das ist genau die Sorte Fehler, die die Daten überlebt.

**Zu große Länge** führte auf die falsche Spur: die Schleife las 64-mal ins Leere
und meldete dann *„nach 64 Lesevorgaengen immer noch unvollstaendig"* — eine
Meldung, die auf eine langsame Verbindung deutet statt auf den kaputten Kopf. In
der Gegenprobe (Abschnitt 3) ist das nachgestellt: ohne die Vorprüfung kam an
dieser Stelle ein `TmctlError` aus dem simulierten Lesetimeout heraus, also eine
Meldung über die Leitung statt über die Antwort.

Die Obergrenze ist nicht gegriffen, sondern hergeleitet:
`MAX_BLOCK_READS * config.read_buffer_size` — mehr ließe sich in der vorhandenen
Schleife ohnehin nie einsammeln. Bei den Voreinstellungen sind das 64 × 64 KiB =
4 MiB. Die Meldung sagt das auch so.

### 2.4 `MAX_BLOCK_READS` als Konstante (`:78`)
Die 64 stand als nackte Zahl in der Schleife. Sie wird jetzt an drei Stellen
gebraucht — Schleifengrenze, Obergrenze der Nutzlast und beide Meldungstexte — und
steht deshalb als Modulkonstante, aufgenommen in `__all__` wie
`MAX_PROGRAM_MESSAGE_BYTES` auch. Die Meldung beim Abbruch nennt jetzt zusätzlich,
wie viele Bytes von wie vielen angekommen sind.

---

## 3 — Prüfung

Elf neue Fälle in [tests/test_fake_transport.py](tests/test_fake_transport.py),
alle über den echten Weg `query_block()` statt über die private Methode.

Die vom Plan geforderten vier Eingaben plus vier weitere, als
parametrisierter Test:

| Antwort | Fall |
|---|---|
| `b"#"` | Ziffernanzahl fehlt |
| `b"#X0012"` | Ziffernanzahl ist keine Zahl |
| `b"#0"` | unbestimmte Länge |
| `b"#4"` | Längenfeld fehlt ganz |
| `b"#412"` | Längenfeld abgeschnitten |
| `b"#4AB12"` | Längenfeld ist keine Zahl |
| `b"#4-100…"` | negative Länge |
| `b"#9999999999…"` | unplausibel große Länge |

Dazu drei benannte Fälle: der still gekürzte Block bei negativer Länge, die
Meldung bei zu großer Länge, und eine Gegenprobe, dass ein gültiger Block
unverändert durchgeht.

**Gegenprobe durchgeführt.** Mit vorübergehend ausgebauten Prüfungen fallen sieben
der elf durch:

```
FAILED ...[Laengenfeld fehlt ganz]
FAILED ...[Laengenfeld abgeschnitten]
FAILED ...[Laengenfeld ist keine Zahl]
FAILED ...[negative Laenge]
FAILED ...[unplausibel grosse Laenge]
FAILED test_negative_laenge_liefert_keinen_still_gekuerzten_block
FAILED test_zu_grosse_laenge_nennt_den_kopf_und_nicht_die_leitung
```

Die vier übrigen — `b"#"`, `b"#X0012"`, `b"#0"` und der gültige Block — bestehen
auch ohne die Korrektur. Sie waren von der bestehenden Absicherung der
Ziffernanzahl bereits gedeckt und sind hier als Vollständigkeitskontrolle mit
aufgenommen.

```
204 passed
pyflakes: keine Meldung
```

---

## 4 — Auswirkung auf bestehenden Code

**Keine für den Regelfall.** Ein gültiger Block läuft unverändert durch, die
Zusatzprüfungen kosten drei Vergleiche je Blockabfrage.

Für den Fehlerfall ist es eine Verbesserung ohne Umstellungsaufwand: wo vorher ein
`ValueError` an `except WTError` vorbeilief, kommt jetzt ein `ProtocolError` —
und den fangen alle Stufenskripte bereits.

---

## 5 — Stand von Paket A

| Nr. | Befund | Status |
|---|---|---|
| P-1 | REMOTE nach gescheitertem Verbindungsaufbau | ✅ umgesetzt |
| P-2 | Restore-Fehler der Item-Tabelle unterdrückt | ✅ umgesetzt |
| P-3 | CSV-Zeile gegen den Spaltenkopf | ✅ umgesetzt |
| P-4 | Blockheader vollständig validieren | ✅ umgesetzt |

Von 176 auf 204 Tests, alle weiterhin ohne Gerät. Für jeden der vier Befunde
existiert mindestens ein Test, der ohne die Korrektur fehlschlägt — das war das
Abnahmekriterium des Plans.

**Als Nächstes stünde Paket B an:** P-5 (Schreibprobe in Stufe 5b zum
Laufzeitparameter machen) und P-6 (das schreibende Geräteskript aus `tests/`
herausnehmen). Beide betreffen unbeabsichtigte Schreibzugriffe, nicht die
Datenintegrität.
