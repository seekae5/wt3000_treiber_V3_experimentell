# P-7 — Herkunft der Verbindungsparameter konfigurierbar

**Datum:** 2026-08-19
**Bezug:** [PLAN_BEFUNDE_2026-08-19.md](PLAN_BEFUNDE_2026-08-19.md) P-7 · Befund BF-M2 · Befund B-08 aus [AENDERUNGEN_2026-08-18.md](AENDERUNGEN_2026-08-18.md)
**Stand vorher:** 214 Tests grün · **Stand nachher:** 241 Tests grün, `pyflakes` ohne Meldung

**Damit ist Paket C abgeschlossen.** Deckt zugleich die Hälfte von ROADMAP M5-2 ab.

---

## 1 — Das Problem

`WTConfig` trug vier rechnerspezifische Werte im Quelltext:

```python
dll_path: str = r"C:\Users\Persystems\PycharmProjects\WT3000_SCPI\tmctl8020\dll\tmctl64.dll"
ip: str = "192.168.10.20"
user: str = "TEST"
password: str = "1"
```

Der `dll_path` zeigt in ein Benutzerverzeichnis, das auf keinem zweiten Rechner
existiert — die erste Hürde für jeden, der den Treiber als Bibliothek einsetzt.
Und Zugangsdaten, auch harmlose Laborwerte, gehören nicht in die
Versionsverwaltung.

---

## 2 — Die Auflösungskette

Neu ist `WTConfig.from_environment()`. Vier Stufen, die erste die etwas
liefert gewinnt — und zwar **je Feld einzeln**, nicht die Konfiguration als
Ganzes:

| Rang | Quelle | Beispiel |
|------|--------|----------|
| 1 | ausdrücklicher Parameter | `WT3000.connect(ip="10.0.0.5")` |
| 2 | Umgebungsvariable | `WT3000_IP=10.0.0.5` |
| 3 | Konfigurationsdatei | `wt3000.json` |
| 4 | Voreinstellung der Klasse | neutral |

Die feldweise Auflösung ist der Punkt: eine `wt3000.json` mit IP und
Zugangsdaten, dazu ein `WT3000_IP` für einen Testlauf am zweiten Gerät, dazu
ein `timeout_ms` als Parameter — alles gleichzeitig, ohne dass eine Stufe die
andere ganz verdrängt.

**Bewusst eine Klassenmethode und kein Verhalten von `__init__`:** `WTConfig`
bleibt eine reine Datenklasse, und der bloße Import des Moduls liest weder
Umgebung noch Dateisystem. Ein `WTConfig()` ohne Argumente ist seit P-7 **nicht
verbindungsfähig** — es ist der Ausgangspunkt, auf den die Kette ihre Werte legt.

### Die Konfigurationsdatei
`wt3000.json`, gesucht in der Reihenfolge `WT3000_CONFIG` → `./wt3000.json` →
`~/wt3000.json`. Fehlt sie überall, ist das kein Fehler; ein **ausdrücklich
benannter** Pfad, den es nicht gibt, dagegen schon — sonst liefe der Aufrufer
still mit den Voreinstellungen weiter.

Format ist JSON, nicht TOML: `tomllib` gibt es erst ab Python 3.11, das Paket
verlangt aber nur 3.10. JSON ist ohnehin schon das Format der Backups und
Snapshots.

Da JSON keine Kommentare kennt, werden Schlüssel mit führendem `_`
stillschweigend übergangen. Damit lässt sich
[wt3000.example.json](wt3000.example.json) mit Erklärtext ausliefern, ohne dass
eine Kopie davon bei jedem Start eine Warnung auslöst. Unbekannte Schlüssel
*ohne* Unterstrich werden gemeldet — ein Tippfehler soll auffallen.

### `dll_path`: Pfad oder bloßer Name
Neu ist `resolve_dll_path()`, das zwei Fälle unterscheidet:

* **bloßer Dateiname** (`tmctl64.dll`, die Voreinstellung) → wird
  durchgereicht, Windows sucht selbst in `PATH` und im Anwendungsverzeichnis.
  Der übliche Weg bei installierter TMCTL.
* **Pfadangabe** → muss existieren. Sonst lädt `ctypes` irgendetwas oder nichts,
  und die Meldung wäre unbrauchbar.

Die Funktion ist bewusst modulweit und rein, damit sie ohne DLL und ohne Windows
prüfbar ist — `TmctlTransport` ist in der Testsuite seit P-6 stillgelegt.

### Fehlende IP fällt früh auf
`TmctlTransport.__init__` bricht jetzt vor dem DLL-Laden ab, wenn keine IP
gesetzt ist, und nennt alle drei Wege. Vorher wäre der Adressstring `",,"`
entstanden und `TmcInitialize` mit einem nackten Fehlercode gescheitert.

---

## 3 — Umgestellte Aufrufer

Alle sieben Stellen, die `WTConfig()` ohne Argumente erzeugten:

| Datei | |
|---|---|
| `wt3000_device.py` | `WT3000.connect()` setzt auf `from_environment()` auf; `replace()` entfällt |
| `stage2_read_numeric.py` … `stage5b_range_probe.py` | fünf Stufenskripte |
| `tools/hardware/probe_voltage_range.py` | Geräteskript |

Das war die im Plan benannte **Verträglichkeitsfalle**: hätte man nur die
Voreinstellungen neutralisiert, wären alle Skripte ins Leere gelaufen. Sie
holen ihre Werte jetzt aus derselben Kette.

`WT3000.connect(ip=None, …)` überschreibt die Umgebung nicht — `None` zählt
nicht als Angabe. Ohne diese Regel hätte die Fassade die Kette bei jedem
weggelassenen Argument ausgehebelt.

---

## 4 — Prüfung

26 neue Fälle in [tests/test_config_resolution.py](tests/test_config_resolution.py).
Eine `autouse`-Fixture räumt vorher **alle** `WT3000_*`-Variablen ab und legt
`cwd` und `HOME` ins tmp-Verzeichnis — sonst hinge das Ergebnis davon ab, was
auf dem Rechner des Prüfenden gesetzt ist. Genau die Abhängigkeit, die P-7
beseitigen soll.

Geprüft werden:

* **die Rangfolge** — Parameter schlägt Umgebung schlägt Datei schlägt
  Voreinstellung, jede Stufe einzeln und alle vier gemischt
* **die Voreinstellung ist neutral** — keine IP, kein Benutzer, kein Passwort
* `None` und leere Umgebungsvariablen zählen nicht als Angabe
* Typwandlung für `int` und `bool` (`1/true/ja/on` gegen `0/nein/off`)
* Fehlerfälle: unbrauchbare Zahl, fehlende benannte Datei, kaputtes JSON,
  unbekannte Schlüssel, Kommentarschlüssel
* `resolve_dll_path()` in allen drei Ausgängen
* `describe()` zeigt **kein** Passwort

**Gegenprobe durchgeführt.** Die alten Werte testweise wieder eingetragen:

```
FAILED test_voreinstellung_traegt_keine_zugangsdaten
E         + 192.168.10.20
```

```
241 passed
pyflakes: keine Meldung
```

---

## 5 — Was noch dazugehört

* [.gitignore](.gitignore) schließt `wt3000.json` aus.
* [wt3000.example.json](wt3000.example.json) ist die Vorlage — enthält die
  bisherigen Laborwerte als Beispiel und ist unverändert kopierbar (geprüft).
* [README.md](README.md): neuer Abschnitt *Verbindungsparameter* mit der
  Rangfolge-Tabelle, der Dateisuche, den Variablennamen und der
  `dll_path`-Regel. Der Installationsabschnitt verweist darauf.

---

## 6 — Stand der Pakete

| | | Status |
|---|---|---|
| **Paket A** | P-1 … P-4 — Garantien einhalten | ✅ |
| **Paket B** | P-5, P-6 — Schreibzugriffe sichtbar machen | ✅ |
| **Paket C** | P-7 — Herkunft der Verbindungsparameter | ✅ |
| Paket D | P-8 — `dev`-Gruppe, Interpreter-Hinweis | offen |

Sieben von acht Planpunkten sind umgesetzt. Die Testsuite ist von 176 auf 241
Fälle gewachsen und läuft weiterhin ohne Gerät und ohne `tmctl.dll`.

**Nicht Teil dieses Durchgangs:** die übrigen Laufparameter der Stufenskripte
(`MAX_SAMPLES`, `OUTPUT_DIR`, `FORCE_FULL_RESTORE` …) stehen weiterhin als
Modulkonstanten im Quelltext. Sie sind nicht rechnerspezifisch und gehören
gesammelt in ROADMAP M5-2, wenn die Skripte eine gemeinsame Kommandozeile
bekommen.
