# P-1 — REMOTE beim gescheiterten Verbindungsaufbau abschalten

**Datum:** 2026-08-19
**Bezug:** [PLAN_BEFUNDE_2026-08-19.md](PLAN_BEFUNDE_2026-08-19.md) P-1 · Befunde BF-H1 und Z-1 · [Befund.md](Befund.md)
**Stand vorher:** 176 Tests grün · **Stand nachher:** 182 Tests grün, weiterhin ohne Gerät und ohne `tmctl.dll`, `pyflakes` ohne Meldung

---

## 1 — Das Problem

`WT3000.__init__()` sendete `:COMMunicate:REMote ON` und rief unmittelbar danach
`DeviceInfo.read()` auf. Scheiterte dort eine der beiden Pflichtabfragen —
`:INPut:WIRing?` oder `:INPut:MODUle?` —, verließ die Ausnahme den Konstruktor,
ohne dass `:COMMunicate:REMote OFF` je gesendet wurde.

Das ließ sich durch nichts auffangen: `WT3000.close()` ist die Stelle, die REMote
zurücknimmt, aber bei einem gescheiterten Konstruktor entsteht gar kein Objekt, an
dem `close()` aufrufbar wäre. Das Bedienfeld des Geräts blieb gesperrt zurück, und
zwar nach einem Verbindungsversuch, den der Anwender als *fehlgeschlagen* wahrnimmt —
also gerade dann, wenn er am wenigsten damit rechnet.

Verschärfend gegenüber der Beschreibung in `Befund.md`:

* **`use_remote` steht auf `True`** (`wt3000_transport.py:75`). Der Pfad war damit
  nicht theoretisch, sondern der Normalfall jeder schreibenden Sitzung.
* **Alle drei Erzeugungswege waren betroffen**, nicht nur `from_config()`:
  `from_transport()` räumte gar nicht auf (Befund Z-1, in `Befund.md` nicht
  enthalten), und die direkte Konstruktion `WT3000(transport, …)` ebenso.
* Der Kommentar im Ausnahmepfad von `from_config()` behauptete ausdrücklich, dieser
  Block verhindere, dass das Gerät „in Fernsteuerung stehen" bleibt. Er hat das nie
  getan.

---

## 2 — Was geändert wurde

### 2.1 Aufräumschutz im Konstruktor
[`wt3000_device.py:491–516`](src/wt3000_scpi/wt3000_device.py)

Alles nach `enable_remote()` — `DeviceInfo.read()` und `log_summary()` — läuft jetzt
in einem `try`. Im Fehlerfall wird zuerst die Fernsteuerung zurückgenommen, dann die
ursprüngliche Ausnahme unverändert weitergereicht.

Die Reparatur sitzt bewusst **im Konstruktor** und nicht in `from_config()`. Nur so
sind alle drei Erzeugungswege in einem Zug abgedeckt; eine Reparatur an der in
`Befund.md` genannten Stelle hätte `from_transport()` und die direkte Konstruktion
offen gelassen.

Gefangen wird `BaseException`, nicht `Exception`: ein Strg+C während des
Verbindungsaufbaus ist kein `Exception`, soll das Bedienfeld aber genauso freigeben.
Das entspricht dem, was `from_config()` an seiner Stelle bereits tut.

### 2.2 Neue Methode `_release_remote_after_failure()`
[`wt3000_device.py:752–776`](src/wt3000_scpi/wt3000_device.py)

Das Gegenstück zu `close()` für den Fall, dass der Konstruktor nicht durchläuft.
Bewusst eng gefasst — sie räumt **nur** ab, was der Konstruktor selbst angerichtet
hat:

* **Kein Transport-Close.** Wer den Transport erzeugt hat, schließt ihn auch: bei
  `from_config()` ist das die Fassade, bei `from_transport()` der Aufrufer
  (`owns_transport=False`). Ein Close an dieser Stelle hätte einen mitgebrachten
  Transport unter dem Aufrufer weggezogen.
* **Kein `HOLD OFF`.** Zu diesem Zeitpunkt hat noch keine Messung stattgefunden.
* **Kein erneutes Auslösen.** Ein Fehler beim Aufräumen wird protokolliert, nicht
  weitergereicht — er darf die eigentliche Ursache niemals verdecken. Der Aufruf ist
  deshalb in `except Exception` gefasst, obwohl `disable_remote()` `WTError` bereits
  selbst abfängt: ein Transport, der etwas anderes wirft, soll den Verbindungsfehler
  nicht ersetzen. Die Protokollzeile nennt in diesem Fall die LOCAL-Taste als Ausweg.

`disable_remote()` selbst blieb unverändert — es war für diesen Einsatz bereits
richtig gebaut: es prüft `_remote_active`, sendet also nichts, wenn nie eingeschaltet
wurde, fängt `WTError` ab und setzt das Flag im `finally` zurück.

### 2.3 Kommentar in `from_config()` berichtigt
[`wt3000_device.py:569–584`](src/wt3000_scpi/wt3000_device.py)

Der Block behält sein `except BaseException` mit `transport.close()` — das bleibt
richtig, weil nur dieser Weg den Transport besitzt. Der Kommentar sagt jetzt, was der
Block tatsächlich leistet, und verweist für die Fernsteuerung auf den Konstruktor.

Zur Reihenfolge: Der Konstruktor schaltet REMote ab, **bevor** die Ausnahme in
`from_config()` ankommt. Ein `REMote OFF` nach `transport.close()` wäre ins Leere
gegangen.

---

## 3 — Prüfung

Sechs neue Fälle in [tests/test_device_facade.py](tests/test_device_facade.py),
alle gerätefrei über `FakeTransport`. `fail_commands={":INPut:WIRing?"}` lässt genau
die Pflichtabfrage scheitern, um die es geht.

| Test | prüft |
|---|---|
| `..._gescheiterter_verbindungsaufbau_gibt_das_bedienfeld_frei` | `REMote ON` **und** `REMote OFF` stehen im Protokoll, in dieser Reihenfolge |
| `..._meldet_weiter_die_urspruengliche_ursache` | Das Aufräumen verdeckt die Ursache nicht — die Meldung nennt weiterhin `WIRing` |
| `..._ohne_remote_sendet_kein_off` | Nur-Lesen-Sitzung: ohne vorheriges ON wird auch kein OFF gesendet |
| `test_from_config_gibt_bedienfeld_frei_und_schliesst_den_transport` | Zweiter Erzeugungsweg, über `monkeypatch` auf `TmctlTransport`: OFF **und** geschlossener Transport |
| `test_strg_c_waehrend_des_verbindungsaufbaus_...` | `KeyboardInterrupt` gibt das Bedienfeld ebenfalls frei |
| `test_erfolgreicher_aufbau_sendet_kein_vorzeitiges_off` | Gegenprobe: im Regelfall springt der Aufräumpfad nicht an |

**Gegenprobe durchgeführt.** Mit vorübergehend ausgebautem Aufräumschutz fallen drei
der sechs Tests durch:

```
FAILED test_gescheiterter_verbindungsaufbau_gibt_das_bedienfeld_frei
FAILED test_from_config_gibt_bedienfeld_frei_und_schliesst_den_transport
FAILED test_strg_c_waehrend_des_verbindungsaufbaus_gibt_das_bedienfeld_frei
```

mit der Meldung

```
assert ':COMMunicate:REMote OFF' in [':COMMunicate:REMote ON', '*IDN?', ':INPut:WIRing?']
```

Die drei übrigen bestehen auch ohne die Korrektur — sie sind Negativkontrollen und
sollen genau das tun.

```
182 passed
pyflakes: keine Meldung
```

---

## 4 — Was offen bleibt

* **Am Gerät nachzuvollziehen:** ob das WT3000 die Fernsteuerung beim Trennen der
  Ethernet-Verbindung von sich aus zurücknimmt. Falls ja, war der Fehler in der
  Praxis folgenlos — die Zusage im Code gilt dann trotzdem erst ab jetzt. Falls
  nein, war das Bedienfeld nach jedem misslungenen Verbindungsaufbau gesperrt.
  Passt gut zu einem der Messtermine aus ROADMAP M0.
* **Nicht Teil von P-1:** die übrigen Punkte aus Paket A des Plans — P-2
  (unterdrückter Restore-Fehler in `ItemAccess.applied()`), P-3 (CSV-Zeile gegen den
  Kopf absichern) und P-4 (Blockheader vollständig validieren). Alle drei sind
  weiterhin offen.
