Priorisierte Befunde

### Hoch: `REMOTE` kann nach fehlgeschlagener Initialisierung aktiv bleiben

In `WT3000.__init__()` wird `REMOTE ON` vor `DeviceInfo.read()` gesendet (`wt3000_device.py`, etwa Zeilen 458–471). Scheitert danach eine zwingende Wiring- oder Modulabfrage, fängt `from_config()` die Ausnahme ab und schließt nur den Transport (`wt3000_device.py`, etwa Zeilen 515–530). `WTSession.disable_remote()` wird in diesem Fehlerpfad nicht aufgerufen.

Folge: Das Bedienfeld kann nach einem fehlgeschlagenen Verbindungsaufbau gesperrt bleiben. Der Kommentar im Exception-Pfad behauptet, dies werde verhindert, die Implementierung erfüllt das aber nicht.

Zielrichtung: Initialisierung ebenfalls als Cleanup-geschützten Ablauf behandeln und vor dem Transport-Close bestmöglich `REMOTE OFF` senden.

### Hoch: Restore-Fehler der Item-Tabelle wird unterdrückt

`ItemAccess.applied()` führt den Restore im `finally` aus, fängt einen `WTError` aber nur zum Logging ab (`wt3000_device.py`, etwa Zeilen 286–307). Der Fehler wird nicht erneut ausgelöst und ist auch nicht Teil eines Rückgabeobjekts.

Folge: Ein Aufrufer kann den Kontextmanager normal verlassen, obwohl die Item-Tabelle nicht wiederhergestellt wurde. Das widerspricht der dokumentierten Garantie „Ausgangszustand garantiert zurück“ und ist bei einem Messgerät besonders kritisch.

Zielrichtung: Restore-Fehler nach dem Logging weiterreichen oder – analog zu `RangeReport` – explizit und zwingend auswertbar machen. Falls gleichzeitig im Nutzblock ein Fehler auftrat, sollten beide Fehler erhalten bleiben.

### Hoch: Abweichende Messwertanzahl kann die CSV-Struktur verschieben

`read_numeric_values(..., expected_count=...)` protokolliert eine abweichende Anzahl nur als Warnung (`wt3000_numeric.py`, etwa Zeilen 284–290). `CsvRecorder.write_row()` fügt anschließend nur die tatsächlich vorhandenen Werte ein (`wt3000_measure.py`, etwa Zeilen 146–178).

Bei zu wenigen Werten hat die Datenzeile weniger Spalten als der Header. Insbesondere rutscht `status_flags` unter eine Messwertspalte. Bei zu vielen Werten entstehen zusätzliche, unbenannte Spalten. Das ist keine bloße Diagnoseabweichung, sondern kann Messdaten semantisch verfälschen.

Zielrichtung: Vor dem Schreiben strikt abbrechen oder die Zeile deterministisch auf die Headerlänge auffüllen/abschneiden und die Abweichung explizit kennzeichnen. Für metrologische Daten ist ein Abbruch die sicherere Voreinstellung.

### Hoch: Schreibende Voreinstellung widerspricht der Beschreibung von Stufe 5b

Der Kopf von `stage5b_range_probe.py` beschreibt eine Voreinstellung, die nichts schreibt. Tatsächlich steht `ENABLE_NOOP_WRITE_PROBE = True` (etwa Zeile 43). Dadurch wird die Sitzung schreibfähig geöffnet und ein Set-Kommando gesendet.

Folge: Ein Nutzer kann ein als rein lesend verstandenes Diagnoseprogramm starten und unbeabsichtigt schreiben. Auch ein Setzen auf denselben Wert ist ein echter Gerätezugriff und kann bei Protokoll-, Firmware- oder Kopplungsbesonderheiten Nebenwirkungen haben.

Zielrichtung: Default auf `False` setzen oder die Dokumentation eindeutig an das tatsächliche Verhalten anpassen; eine Schreibprobe sollte über einen expliziten Laufzeitparameter aktiviert werden.

### Mittel: Keine reproduzierbare Installation oder deklarierte Python-Version

Im Repository fehlen `pyproject.toml`, `setup.cfg`, `requirements.txt` und eine README. Der Code benutzt Syntax und Laufzeit-Typaliase wie `bytes | str`, die Python 3.10+ benötigen. Unter dem vorhandenen System-Python 3.9 scheitert bereits der Import in `wt3000_transport.py`.

Folgen:

- Die erforderliche Python-Version ist nicht maschinenlesbar dokumentiert.
- `src` muss manuell über `PYTHONPATH` verfügbar gemacht werden.
- Test- und Entwicklungsabhängigkeiten sind nicht reproduzierbar.
- Es gibt keinen standardisierten Installations- oder Testbefehl.

Zielrichtung: Minimalen `pyproject.toml` mit `requires-python`, Paketfindung im `src`-Layout und optionaler Testgruppe für `pytest` ergänzen; Start- und Sicherheitsinformationen in einer README dokumentieren.

### Mittel: Verbindungsdaten sind als Quellcode-Defaults hinterlegt

`WTConfig` enthält einen benutzerspezifischen DLL-Pfad, eine feste IP sowie Benutzername und Passwort (`wt3000_transport.py`, etwa Zeilen 47–62).

Folge: geringe Portabilität und unnötige Verteilung von Zugangsdaten über Versionsverwaltung. Selbst wenn die Werte nur im Labornetz gelten, sollte ihre Herkunft explizit konfigurierbar sein.

Zielrichtung: neutrale Defaults verwenden und Umgebungsvariablen, Konfigurationsdatei oder verpflichtende Konstruktorparameter vorsehen. Zugangsdaten nicht im Repository pflegen.

### Mittel: Blockheader-Fehler werden nicht einheitlich in Treiberfehler übersetzt

`WTSession._assemble_block()` fängt die Konvertierung der Ziffernanzahl ab, nicht aber alle Fehler beim Lesen des Längenfelds. Ein zu kurzer oder nichtnumerischer Längenheader kann daher als nackter `ValueError` statt als `ProtocolError` austreten (`wt3000_core.py`, etwa Zeilen 128–158).

Folge: Aufrufer, die bewusst nur `WTError` behandeln, können bei beschädigten Antworten unerwartet abbrechen; Cleanup in `finally` bleibt zwar erhalten, aber die Fehlersemantik ist inkonsistent.

Zielrichtung: Headerlänge und Längenfeld vollständig validieren und sämtliche Formatfehler als `ProtocolError` ausgeben.

### Niedrig: Dokumentation und Implementierung sind punktuell auseinander gelaufen

- Der Kopf von `__init__.py` sagt, das Modul importiere bewusst nichts aus dem Paket; tatsächlich re-exportiert es die komplette Fassade und mehrere Fachtypen.
- Kommentare in `stage5b_range_probe.py` widersprechen dem aktivierten Default.
- Mehrere „ZU VERIFIZIEREN“-Hinweise markieren noch ungeklärte Hardwareannahmen, unter anderem Timeout-Einheit, Range-Parameterformat und Firmwareumfang der Filterwerte.
