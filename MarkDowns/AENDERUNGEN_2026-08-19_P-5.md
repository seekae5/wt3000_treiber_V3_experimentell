# P-5 — Schreibprobe in Stufe 5b wird zum Laufzeitparameter

**Datum:** 2026-08-19
**Bezug:** [PLAN_BEFUNDE_2026-08-19.md](PLAN_BEFUNDE_2026-08-19.md) P-5 · Befund BF-H4
**Stand vorher:** 206 Tests grün · **Stand nachher:** 214 Tests grün, `pyflakes` ohne Meldung

**Damit ist Paket B abgeschlossen.**

---

## 1 — Das Problem

Der Kopf von `stage5b_range_probe.py` sagte *„Voreinstellung: dieses Skript
SCHREIBT NICHTS"*, die Modulkonstante stand aber auf

```python
ENABLE_NOOP_WRITE_PROBE: bool = True   # muss derzeit noch auf True stehen ...
                                       # -> Modifizierbar machen
```

Wer das Skript als reines Diagnoseprogramm startete, schrieb also — und der
Bearbeiter hatte im selben Atemzug notiert, dass der Schalter beweglich werden
muss.

**Warum der naheliegende Weg der falsche wäre:** `Befund.md` schlug vor, die
Konstante einfach auf `False` zu setzen. Das nimmt genau die Fähigkeit weg, die
für die offenen Gerätefragen M0-1 bis M0-3 gebraucht wird — und die Zeile stünde
beim nächsten Messtermin wieder auf `True`. Das Problem ist nicht der Wert,
sondern dass eine Arbeitseinstellung im Quelltext wohnt.

---

## 2 — Was geändert wurde

### 2.1 Die Modulkonstante ist entfallen
An ihre Stelle tritt ein Parameter:

```python
def main(enable_write_probe: bool = False) -> int:
```

Ohne Argument öffnet die Sitzung mit `read_only=True`, und `WTSession` lehnt dann
jedes Nicht-Query-Kommando ab. Die Voreinstellung ist damit nicht nur
dokumentiert, sondern durch die Sitzungssperre erzwungen.

### 2.2 Kommandozeile
```bash
python -m wt3000_scpi.stage5b_range_probe                 # liest nur
python -m wt3000_scpi.stage5b_range_probe --write-probe   # sendet EIN Kommando
```

`argparse` mit `--write-probe`. Ein Tippfehler (`--writeprobe`) führt zum
Abbruch, nicht stillschweigend zu „nur Lesen".

Neu ist außerdem `_parse_args(argv=None)` als eigene Funktion — so lässt sich die
Kommandozeile prüfen, ohne einen Unterprozess zu starten.

### 2.3 Der Schalter ist unangenehm gemacht
Vor dem ersten Gerätezugriff stehen fünf Warnzeilen im Protokoll, die den
angetasteten Knoten im Klartext nennen:

```
SCHREIBPROBE AKTIV (--write-probe)
  Ein Set-Kommando auf ':INPut:VOLTage:RANGe:ELEMent1' geht hinaus.
  Geschrieben wird der bereits eingestellte Wert - Nulleffekt.
  Der Ausgangszustand wird vorher gesichert und danach geprueft.
```

### 2.4 Dateikopf und ROADMAP
Der Kopf zeigt jetzt beide Aufrufformen und begründet, warum der Schalter ein
Aufrufparameter ist und keine Konstante. In [ROADMAP.md](ROADMAP.md) verwies
M0-3 noch auf `ENABLE_NOOP_WRITE_PROBE = True` — dort steht jetzt der
Kommandozeilenaufruf.

---

## 3 — Prüfung

**Stufenskripte waren bis hierher vollständig ungetestet**, weil sie eine echte
Verbindung aufbauen. Mit `FakeTransport` (M1-2) lässt sich `main()` nun
durchspielen — acht neue Fälle in
[tests/test_stage5b_write_probe.py](tests/test_stage5b_write_probe.py):

| Test | prüft |
|---|---|
| `test_voreinstellung_sendet_kein_einziges_set_kommando` | **der Kern:** `main()` ohne Argument hinterlässt kein einziges Nicht-Query-Kommando |
| `test_voreinstellung_liest_trotzdem_den_bereichszustand` | ohne Schreibprobe bleibt das Skript voll brauchbar |
| `test_voreinstellung_schreibt_das_backup_auf_platte` | die JSON-Sicherung entsteht auch im Lesebetrieb |
| `test_write_probe_sendet_genau_ein_set_kommando` | mit Schalter: genau eines, auf `:INPut:VOLTage:RANGe:ELEMent1` |
| `test_write_probe_meldet_sich_vor_dem_ersten_kommando` | die Warnung steht vor dem Zugriff und nennt den Knoten |
| `test_ohne_schalter_bleibt_die_kommandozeile_lesend` | `_parse_args([])` → `False` |
| `test_der_schalter_setzt_das_flag` | `_parse_args(["--write-probe"])` → `True` |
| `test_unbekannter_schalter_bricht_ab` | `--writeprobe` endet in `SystemExit` |

Der Transport wird **im Modul** ersetzt, nicht global — `TmctlTransport` ist
seit P-6 in der Testsuite stillgelegt, und daran soll sich auch dieser Test
nicht vorbeimogeln.

**Gegenprobe durchgeführt.** Voreinstellung testweise auf `True` gesetzt (der
alte Zustand):

```
FAILED test_voreinstellung_sendet_kein_einziges_set_kommando
```

```
214 passed
pyflakes: keine Meldung
```

---

## 4 — Ein Nebenbefund aus dem Test

`test_write_probe_meldet_sich_vor_dem_ersten_kommando` schlug zunächst fehl,
obwohl die Warnungen nachweislich im Protokoll standen. Ursache: `main()` ruft
`setup_logging()`, und das leert die Handler des Root-Loggers — **einschließlich
des Mitschnitts, den pytest für `caplog` installiert**. Alles nach dem Aufruf
fehlte deshalb in `caplog.records`. Isoliert nachgestellt und bestätigt.

Das ist kein neuer Fehler: der Docstring von `setup_logging()` warnt seit F-08
ausdrücklich davor (*„Wer den Treiber als Bibliothek in eine groessere Anwendung
einbaut, ruft diese Funktion NICHT auf … sonst werden deren Handler mit
entfernt"*). Hier ist die Warnung erstmals eingetreten — pytest ist die größere
Anwendung.

Im Test wird `setup_logging` deshalb stillgelegt; geprüft wird die Schreibsperre,
nicht die Protokolleinrichtung. **Für die Bibliothek bleibt das offen** und
gehört zu ROADMAP M5-2, wenn die Stufenskripte eine gemeinsame Kommandozeile
bekommen: dann sollte die Protokolleinrichtung dort einmal am Einstiegspunkt
stattfinden und nicht in jedem `main()`.

---

## 5 — Stand der Pakete

| | | Status |
|---|---|---|
| **Paket A** | P-1 … P-4 — Garantien einhalten | ✅ abgeschlossen |
| **Paket B** | P-5, P-6 — Schreibzugriffe sichtbar machen | ✅ abgeschlossen |
| Paket C | P-7 — Herkunft der Verbindungsparameter | offen |
| Paket D | P-8 — Werkzeuge und Doku nachziehen | offen |

Sechs der acht Planpunkte sind umgesetzt, die Testsuite ist von 176 auf 214
Fälle gewachsen und läuft weiterhin ohne Gerät.

**Nicht Teil dieses Durchgangs**, wie im Plan festgehalten: dieselbe Umstellung
für die übrigen Stufenskripte. Dort stehen die Laufparameter ebenfalls als
Modulkonstanten (`EXERCISE_RESTORE_WRITE`, `FORCE_FULL_RESTORE`, `MAX_SAMPLES`,
`OUTPUT_DIR` …). Das gehört gesammelt in M5-2 — sonst entstehen fünf
verschiedene Kommandozeilen.
