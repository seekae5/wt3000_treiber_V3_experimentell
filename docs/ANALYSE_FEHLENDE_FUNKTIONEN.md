# Analyse — was der Bibliothek fehlt, um "vollständige Messungen" zu erlauben

**Anlass:** Auswertung von `WT3000_networking.pdf` (Yokogawa IM 760301-17E, Vol 2/3,
Communication Interface User's Manual) im Hinblick auf fehlende
Funktionen/Klassen/Methoden für einen Anwender, der unterschiedlichste Messungen mit
dem WT3000 durchführen will. **Kein Code geändert oder geschrieben** — reine
Stichpunktsammlung.

---

## 0 — Zur Quellenlage (wichtig für die Einordnung)

**Update:** Die anfangs übergebene PDF war auf 15 Seiten gekürzt (nur Titelei,
Inhaltsverzeichnis, Kapitel 1 GP-IB). Inzwischen liegt die **vollständige Datei
mit 184 Seiten** vor — Kapitel 5–7 (Befehlssyntax, alle 24 SCPI-Kommandogruppen
im Detail, Statusberichte) wurden jetzt vollständig gelesen und ausgewertet.
Die folgende Analyse ist damit direkt am Handbuch geprüft, nicht mehr nur aus
`WT3000_Commands_Overview.md` und Code-Abgleich abgeleitet (Abschnitt 1
bleibt trotzdem korrekt und wird hier bestätigt).

* Diese Datei **wiederholt die ROADMAP nicht**, sondern sortiert dieselbe Lücke
  entlang von **Anwendungsfällen** (welche Messung will der Nutzer machen?) statt
  entlang von Meilensteinen — als zusätzliche Einordnungshilfe.
* Referenz bleibt zusätzlich [`ROADMAP.md`](ROADMAP.md), insbesondere M2-1
  („Fehlende Gerätegruppen") und M3 („Messung starten und stoppen").

### 0.1 — Wichtigster neuer Befund: viele Gruppen sind optionsabhängig

Das Handbuch nennt bei mehreren Kommandogruppen ausdrücklich eine
**Gerätehardware-Option**, ohne die die Kommandos einen Fehler zurückgeben:

| Gruppe | benötigte Option | Betrifft aus Abschnitt 2 |
|---|---|---|
| `:HARMonics` | `/G5` (Harmonic-Messung) oder `/G6` (Advanced Computation) | 2.3 |
| `:ACQuisition` (Rohabtastdaten) | `/G6` | 2.7 |
| `:CBCycle` | `/CC` | 2.6 |
| `:FLICker` | `/FL` | 2.4 |
| `:MOTor` | Motor-Version `-MV` (Modellvariante, keine Nachrüstoption) | 2.5 |
| `:AOUTput` | `/DA` | 2.10 |
| `:HCOPy` | `/B5` (interner Drucker) bzw. `/C7` (Netzwerkdrucker) | 2.9 |
| `MEASure:DMeasure`, `MEASure:COMPensation:V3A3` | `/DT` (Delta-Berechnung) | 2.2 |
| `:CURSor:FFT`, `:DISPlay:FFT` | `/G6` | 2.7 |

**Ohne Option installiert schlägt das jeweilige Kommando fehl — Software-seitige
Implementierung allein reicht nicht.** Vor jeder Umsetzung dieser Gruppen muss
also erst geklärt sein, welche Optionen das konkrete Gerät hat.

**Das lässt sich jetzt konkret und ohne Rätselraten klären:** `*OPT?` liefert
genau die installierten Optionen als kommagetrennte Liste (Beispiel aus dem
Handbuch: `*OPT? -> G6,B5,DT,FQ,DA,V1,C2,C7,C5,CC,FL`; keine Option → `"0"`).
**Das ist die direkte, bereits am Gerät verfügbare Lösung für ROADMAP M1-3
(„Optionen und Firmware erfassen (prüfen)")** — kein offener Punkt mehr, nur
noch eine ausstehende Umsetzung: `*OPT?` einmal beim Verbindungsaufbau
abfragen und in `DeviceInfo` ablegen, danach jede optionsabhängige Gruppe
dagegen prüfen, bevor sie angesprochen wird.

**Gegenbeispiel — keine Option nötig:** `:INTEGrate` (Abschnitt 2.1, größte
Lücke), `:MEASure` (Averaging, Effizienz, Frequenz — Abschnitt 2.2, bis auf
die zwei oben genannten Delta-Kommandos), `:STORe`, `:STATus`, `:SYSTem`,
`:COMMunicate`, `:RATE` und — überraschend — auch **`:WAVeform`** (die
Anzeige-Wellenform mit fest 1002 Punkten) sind **basisfunktionalität ohne
Optionsvoraussetzung**. Das ist eine Korrektur gegenüber der ersten Fassung
dieser Analyse: Wellenformzugriff ist nicht per se optionsgebunden — nur der
hochauflösende **Rohabtast**-Zugriff über `:ACQuisition` braucht `/G6`. Ein
einfacher Wellenform-Schnappschuss über `:WAVeform:SEND?` wäre also ohne
Optionsrisiko umsetzbar, falls das je gebraucht wird (weiterhin niedrige
Priorität, siehe ROADMAP Abschnitt 5 „Bewusst nicht enthalten").

### 0.2 — Zweiter neuer Befund: dokumentierter Mechanismus für Ereigniserkennung

Kapitel 7 (Statusberichte) beschreibt das **Extended Event Register** im
Detail. Bit 0 heißt **UPD (Updating)**: *„Set to 1 when the measured data is
being updated. The falling edge of UPD (1→0) signifies the end of the
updating."* In Kapitel 5.5 steht dazu bereits ein vollständiges
Programmierbeispiel: Transitionsfilter auf `FALL` setzen
(`:STATus:FILTer1 FALL`), Enable-Register setzen (`:STATus:EESE 1`), auf den
Service-Request warten, dann lesen.

**Das ist die konkrete, am Handbuch belegte Antwort auf ROADMAP M0-5
(„Erkennung eines neuen Datensatzes") und M3-3 („Gerätetakt statt blindem
sleep")** — nicht länger nur eine Vermutung, sondern ein vom Hersteller
dokumentiertes Muster. Am Gerät zu prüfen bleibt nur noch die **reale
Zeitcharakteristik** (wie zuverlässig/schnell schaltet UPD tatsächlich um),
nicht mehr, ob ein solcher Mechanismus überhaupt existiert.

Weitere Bits desselben Registers, die für spätere Module aus Abschnitt 2
nützlich sind: Bit 1 `ITG` (Integration läuft), Bit 2 `ITM` (Integrations-Timer
läuft), Bit 3 `SRB` (Store/Recall aktiv), Bit 6 `ACS` (Medienzugriff — relevant
für `:FILE`/`:STORe`), Bit 7 `PLLE` (PLL-Quelle fehlt — relevant für
Harmonics-Synchronisation).

**Bestätigt aus dem GP-IB-Kapitel, ergänzend zur ROADMAP nutzbar:**
* Gerät unterstützt Serial Poll (`SR1`) und Remote/Local-Umschaltung über
  Standard-Busnachrichten — stützt den in ROADMAP M0-5/M3-3 erwogenen Weg,
  Statusabfrage statt blindem `sleep()` für Mess-Timing zu nutzen.
* `LLO` (Local Lockout) sperrt die LOCAL-Taste am Gerät serverseitig — mögliche
  Ergänzung für eine Langzeitmessung, damit niemand versehentlich am Panel
  eingreift (siehe Abschnitt 3).
* `GET` (Group Execute Trigger) ist bus-äquivalent zu `*TRG` — bereits als
  Common Command in `WT3000_Commands_Overview.md` gelistet, aber im Code noch
  nicht genutzt (relevant für synchronisierten Messstart, siehe M3-2).
* `DCL`/`SDC` (Device/Selected Device Clear) löschen Programmnachricht und
  Ausgabepuffer — deckt sich mit `drain_after_failure()`/`WTError`-Härtung aus
  M1-5; kein neuer Befund, nur Bestätigung des geplanten Wegs.

---

## 1 — Abgleich: welche SCPI-Kommandogruppen sind im Code schon belegt?

Anhand tatsächlich verwendeter Kommandostrings (nicht nur Modulnamen):

| Gruppe | Im Code verwendet? | Wo |
|---|---|---|
| `:INPut` | ja, umfangreich | `wt3000_input.py`, `wt3000_rangeio.py` |
| `:NUMeric` | ja, umfangreich | `wt3000_numeric.py`, `wt3000_itemspec.py` |
| `:COMMunicate` (Teilmenge: HEADer, REMote, VERBose) | ja | `wt3000_core.py`, `wt3000_transport.py` |
| `:STATus` (Teilmenge: CONDition, ERRor) | ja | `wt3000_core.py` |
| `:HOLD` | ja | `wt3000_measure.py`, `wt3000_device.py` |
| `:RATE` (Update-Rate) | ja | `wt3000_input.py` |
| `:ACQuisition`, `:AOUTput`, `:CBCycle`, `:CURSor`, `:DISPlay`, `:FILE` (Gerät-intern), `:FLICker`, `:HARMonics`, `:HCOPy`, `:IMAGe`, `:INTEGrate`, `:MEASure`, `:MOTor`, `:STORe`, `:SYSTem`, `:WAVeform` | **nein — kein einziger Kommandostring dieser Gruppen im Quellcode** | — |

→ 16 von 22 SCPI-Kommandogruppen des Geräts werden vom Treiber heute überhaupt
nicht angesprochen. Das ist der Kern der Lücke, unabhängig davon, wie man sie
gliedert.

---

## 2 — Lücken nach Anwendungsfall (nicht nach Meilenstein)

### 2.1 Energie-/Wh-Ah-Messung (klassischer Leistungsmessgerät-Anwendungsfall)
* Fehlt vollständig: **Integrationssteuerung** — `:INTEGrate` (`STARt`, `STOP`,
  `RESet`, `MODE`, `TIMer`, `RTIMe`, `ACAL`)
* Fehlende Klasse: z. B. `IntegratorControl`/`EnergyMeter` mit
  `start()`/`stop()`/`reset()`, Moduswahl (normalisiert vs. kontinuierlich),
  Timer-Konfiguration, Restzeit-Abfrage
* Ohne dieses Modul kann der Treiber **keine** Wh/Ah-Messung steuern — nur
  Momentanwerte lesen. Das ist die größte funktionale Lücke gegenüber einem
  „vollständigen" Leistungsmessgerätetreiber.
* Abhängigkeit: ROADMAP M3-2 (Gerätesteuerung), am Gerät zu verifizieren
  **(prüfen)**

### 2.2 Berechnete/abgeleitete Messgrößen
* Fehlt: `:MEASure`-Gruppe — `AVERaging`, `COMPensation`, `DMeasure` (DC-Anteil),
  `EFFiciency` (Wirkungsgrad, z. B. für Wandler-/Antriebsmessungen), `FREQuency`
  (Frequenzmessquelle), `FUNCtion` (benutzerdefinierte Rechenkanäle),
  `SQFormula`, `SYNChronize`
* Fehlende Klasse: z. B. `ComputationConfig` — strukturierter Zugriff auf
  Averaging-Ein/Aus und -Zeitkonstante, Effizienzformel-Auswahl,
  Frequenzmessquelle je Element
* Priorität hoch: Averaging ist in der Praxis fast immer aktiv; ohne
  Softwarezugriff muss der Anwender es panelseitig vorkonfigurieren und darf es
  während der Messung nie prüfen/ändern

### 2.3 Oberschwingungsanalyse (Harmonics)
* Fehlt vollständig: `:HARMonics`-Gruppe — `FBANd` (Bandbreite), `IEC`
  (Normkonformität, Gruppierung), `ORDer` (min/max Ordnung), `PLLSource`,
  `PLLWarning`, `THD`-Formel
* Fehlende Klasse: `HarmonicsConfig` mit strukturiertem Snapshot/Restore
  analog zu `RangeAccess`
* Der WT3000 wird häufig gerade wegen Oberschwingungsmessung eingesetzt
  (Netzqualität, Normprüfung) — ohne dieses Modul deckt der Treiber einen der
  Hauptanwendungsfälle des Geräts gar nicht ab

### 2.4 Flicker-Messung (IEC 61000-3-3)
* Fehlt vollständig: `:FLICker`-Gruppe (Pst/Plt-Grenzwerte, Editionswahl,
  Start/Reset, Status)
* Nischenanwendung gegenüber 2.1–2.3, aber ein eigener Prüfstandard — nur
  relevant, falls Zielgruppe Normprüfungen macht. **Niedrige Priorität**, außer
  der Anwenderkreis braucht es ausdrücklich

### 2.5 Motor-Wirkungsgrad (sofern Motor-Option verbaut)
* Fehlt vollständig: `:MOTor`-Gruppe (`PM`, `POLE`, `SPEed`, `TORQue`,
  `SYNChronize`, `FILTer`)
* Abhängig von Geräteoption — vor Implementierung klären, ob die konkrete
  Einheit die Motor-Option besitzt (siehe `DeviceInfo`-Erweiterung, M1-3)
* **(prüfen)** ob Option vorhanden, sonst zurückstellen

### 2.6 Zyklusbasierte/synchronisierte Messung (CBCycle)
* Fehlt vollständig: `:CBCycle`-Gruppe (zyklusweise Messung mit Trigger,
  Sync-Quelle, Zeitlimit) — eigener Modus jenseits der freilaufenden
  `:NUMeric`-Schleife
* Relevant für Anwender, die z. B. netzsynchron oder ereignisgetriggert messen
  wollen, nicht nur zeitgetaktet
* Ergänzt/nutzt vermutlich `*TRG`/`GET` aus Abschnitt 0

### 2.7 Rohdaten-/Wellenformerfassung
* Fehlt vollständig: `:ACQuisition`- und `:WAVeform`-Gruppe (Sample-Rate,
  Blockformat, Start/Endpunkt, Byte-Order, Datenabruf)
* In ROADMAP Abschnitt 5 („Bewusst nicht enthalten") **explizit
  zurückgestellt** — „andere Datenmengen und Kommandogruppen; erst bei
  konkreter Messaufgabe". Diese Analyse bestätigt nur, dass die Lücke besteht,
  ändert aber nichts an der bewussten Priorisierung
* Passend dazu auch `:CURSor` (Cursor-Auswertung auf Wellenform/FFT) — nur
  relevant, sobald Wellenformzugriff überhaupt kommt

### 2.8 Setup-/Datenverwaltung auf dem Gerät selbst
* Fehlt vollständig: `:STORe` (geräteseitige Datenlogging-Funktion —
  Alternative/Ergänzung zur Python-Messschleife, läuft unabhängig vom PC
  weiter), `:FILE` (Speicherkarten-/USB-Dateiverwaltung des Geräts,
  Setup-Speicherung), `:SYSTem` (Datum/Uhrzeit, Tastensperre `KLOCk`/`SLOCk`)
* Deckt sich mit ROADMAP M2-2 („Setup-Speicher des Geräts") — hier zusätzlich
  konkretisiert: `:SYSTem:KLOCk`/`:SLOCk` könnten dieselbe Rolle wie `LLO`
  aus Abschnitt 0 spielen (Panel während automatisierter Messung sperren)
* `:SYSTem:DATE`/`:TIME` relevant, falls Zeitstempel vom Gerät statt vom PC
  stammen sollen (Abgleich von PC- und Geräte-Uhrzeit)

### 2.9 Dokumentation/Screenshot der Messung
* Fehlt: `:IMAGe` (Bildschirmfoto sichern/übertragen), `:HCOPy` (Druckausgabe)
* `:IMAGe` niedrige, aber nicht triviale Priorität — nützlich für
  automatisierte Prüfprotokolle mit Screenshot-Beleg. `:HCOPy` (Drucker) für
  einen programmatischen Treiber kaum relevant — **kann entfallen**

### 2.10 Analogausgang
* Fehlt: `:AOUTput`-Gruppe — nur relevant, falls die BNC-Analogausgänge des
  Geräts extern weiterverarbeitet werden (z. B. Regelkreis, Datenlogger).
  **Niedrige Priorität**, Nischenfall

---

## 3 — Querschnittliche Bausteine (nicht an eine SCPI-Gruppe gebunden)

* **Steuerbares Mess-Objekt** — bereits in ROADMAP M3-1 geplant
  (`Measurement.start()/stop()/wait()/is_running`); wird durch 2.1/2.6 noch
  wichtiger, weil Integration und Zyklusmessung dieselbe Art von
  Start/Stopp-Semantik brauchen wie die freilaufende Schleife
* **Gemeinsamer Gerätesnapshot** (ROADMAP M2-4, `SessionBackup`) — sollte,
  sobald 2.2/2.3/2.5 existieren, auch Averaging-, Harmonics- und
  Motor-Konfiguration mit sichern/wiederherstellen, nicht nur `:INPut` und
  Item-Tabelle
* **Panel-Sperre während automatisierter Läufe** — neue, bisher nirgends
  geplante Ergänzung: `COMMunicate:LOCKout` (`LLO`) oder
  `SYSTem:KLOCk`/`:SLOCk` als eigene Methode, z. B. `wt.device.lock_panel()` /
  `unlock_panel()` — schützt eine unbeaufsichtigte Langzeitmessung vor
  versehentlicher Bedienung. Sollte am Gerät geprüft werden, welcher der drei
  Wege (`LLO` auf Busebene, `SYSTem:KLOCk`, `SYSTem:SLOCk`) das gewünschte
  Verhalten liefert **(prüfen)**
* **Synchronisierter Trigger** — `*TRG`/`GET` als expliziter Methodenaufruf
  (z. B. `session.trigger()`), aktuell nirgends im Code referenziert, aber
  Voraussetzung für 2.6 und ggf. 2.1 (Integration exakt zu einem Zeitpunkt
  starten)

---

## 4 — Priorisierte Kurzfassung

| Rang | Baustein | Option nötig? | Warum |
|---|---|---|---|
| 0 | `*OPT?` in `DeviceInfo` auswerten | keine (Common Command) | Voraussetzung für alle optionsgebundenen Punkte unten — sollte vor Rang 3, 5, 8, 10 stehen, damit keine Arbeit an nicht vorhandener Hardware entsteht |
| 1 | `IntegratorControl` (`:INTEGrate`) — Wh/Ah-Messung steuern | **nein** | Kernfunktion eines Leistungsmessgeräts, heute nicht steuerbar |
| 2 | `ComputationConfig` (`:MEASure`, insb. Averaging) | **nein** (außer Delta-Teil, siehe unten) | Betrifft praktisch jede Messung, nicht nur Spezialfälle |
| 3 | `HarmonicsConfig` (`:HARMonics`) | **`/G5` oder `/G6`** | Einer der Hauptanwendungsfälle des WT3000 — aber erst nach `*OPT?`-Check angehen |
| 4 | Steuerbares Mess-Objekt + Trigger (`*TRG`/`GET`, `STATus:CONDition?`-Polling auf UPD-Bit) | **nein** | Grundlage für 2.1, 2.6 und robuste Automatisierung; Ereignismechanismus jetzt am Handbuch belegt (Abschnitt 0.2), nicht mehr nur Vermutung |
| 5 | `:CBCycle` (zyklus-/ereignisgetriggerte Messung) | **`/CC`** | Für synchrone/getriggerte Anwendungsfälle jenseits der freilaufenden Schleife |
| 6 | Erweiterter `SessionBackup` (inkl. Averaging/Harmonics/Motor) | folgt den Gruppen, die er sichert | Sicherheitsnetz, sobald 2–3 neue schreibbare Gruppen existieren |
| 7 | Panel-Sperre (`COMMunicate:LOCKout` und/oder `SYSTem:KLOCk`) | **nein** | Kleiner Aufwand, spürbarer Schutz bei unbeaufsichtigten Läufen; beide Kommandos jetzt im Detail bekannt (Abschnitt 3) |
| 8 | `:MOTor` (Motor-Wirkungsgrad) | **Modellvariante `-MV`**, keine Nachrüstoption | Nur falls das konkrete Gerät die MV-Variante ist — per `*IDN?` (Modellcode) klärbar, nicht per `*OPT?` |
| 9 | `:STORe`/`:FILE` (geräteseitige Datenverwaltung) | **nein** | Ergänzung, kein Ersatz für die vorhandene Python-Messschleife; `STORe:SMODe INTEGrate` koppelt Speicherung direkt an Integrationszyklen |
| 10 | `:FLICker`, `:ACQuisition` (Rohabtastdaten), `:IMAGe` | `/FL` bzw. `/G6` (IMAGe optionsfrei) | Nischenfälle — nur bei konkretem Bedarf |
| — | `:WAVeform` (Anzeige-Wellenform, 1002 Punkte) | **nein** (Korrektur ggü. erster Fassung) | Optionsfrei, aber weiterhin niedrige Priorität laut ROADMAP „bewusst nicht enthalten" |
| — | `:AOUTput`, `:HCOPy` | `/DA` bzw. `/B5`/`/C7` | Für einen programmatischen Treiber kaum relevant, entfallen kann geprüft werden |

---

## 5 — Offene Fragen für den nächsten Geräte-/Optionscheck

* **Zuerst zu klären, jetzt trivial:** `*OPT?` und `*IDN?` einmal am
  tatsächlichen Gerät abfragen — beantwortet in einem Aufruf, welche der in
  Abschnitt 0.1 gelisteten optionsgebundenen Gruppen (`/G5`, `/G6`, `/CC`,
  `/FL`, `/DA`, `/DT`, `/B5`, `/C7`) überhaupt ansprechbar sind und ob es sich
  um die Motor-Variante `-MV` handelt (Modellcode aus `*IDN?`, z. B.
  `760304-04-MV`). Damit erübrigt sich das bisherige Rätselraten für Rang 3,
  5, 8 und 10 der Prioritätenliste.
* Welcher der beiden Panel-Sperr-Wege (`COMMunicate:LOCKout` vs.
  `SYSTem:KLOCk`) ist tatsächlich gewünscht, und wie verhält er sich beim
  Verbindungsabbruch (bleibt die Sperre hängen, wenn die Python-Sitzung
  abstürzt, bevor sie sie wieder aufhebt)? Syntax beider Kommandos ist jetzt
  bekannt (Abschnitt 3), nur das Verhalten am realen Gerät fehlt noch.
* Reicht `*TRG`/`GET` (laut Handbuch „same operation as when SINGLE is
  pressed") allein für synchronisierten Start, oder braucht
  `:CBCycle:TRIGger`/`:SYNChronize` zusätzlich eine externe Triggerquelle?
* Liefert `:INTEGrate:RTIMe?` einen belastbaren Fortschritts-/Restzeitwert für
  eine UI-Anzeige während einer laufenden Wh-Messung?
* Wie zuverlässig/schnell schaltet das UPD-Bit (Abschnitt 0.2) in der Praxis
  um — reicht es als alleiniger Ersatz für `sleep()`, oder braucht M3-3
  trotzdem eine Dublettenerkennung als Rückfallebene?
