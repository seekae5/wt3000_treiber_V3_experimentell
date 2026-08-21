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

### 0.3 — Realer Gerätecheck (2026-08-21)

**Nicht mehr vermutet, sondern gemessen.** Abschnitt 5 dieser Datei hat fünf
offene Fragen gelistet, die nur am Gerät zu klären waren. Alle fünf wurden am
21.08.2026 gegen das reale Gerät (IP `192.168.10.20`) mit dem neuen
Geräteskript [`tools/hardware/probe_capabilities.py`](../tools/hardware/probe_capabilities.py)
abgefragt — nur-lesend, kein einziges Schreibkommando (Sitzung mit
`read_only=True`). Protokoll liegt lokal unter
`konfiguration/wt3000_probe_capabilities_20260821_124256.txt` (Verzeichnis ist
`.gitignore`t, daher nicht im Repository).

**Steckbrief:** `YOKOGAWA,760304-40-MV,0,F5.01` — Modell `760304-40-MV`,
Firmware `F5.01`. `*OPT?` → `G6,B5,DT,C7,C5,CC`.

| Code | Zustand | Betroffene Gruppen | Folge |
|---|---|---|---|
| G6 | **vorhanden** | `:HARMonics`, `:ACQuisition`, `:CURSor:FFT` | Rang 3 umsetzbar, obwohl G5 fehlt — G6 allein reicht laut Handbuch |
| CC | **vorhanden** | `:CBCycle` | Rang 5 umsetzbar |
| DT | **vorhanden** | `:MEASure:DMeasure`, `:COMPensation:V3A3` | Rang 2 ohne Einschränkung umsetzbar (Delta eingeschlossen) |
| B5, C7 | **vorhanden** | `:HCOPy` | technisch ansprechbar, Einschätzung „kann entfallen" bleibt unverändert |
| C5 | **vorhanden** | USB-Port für Peripheriegeräte (Handbuch zu `*OPT?`) | keine Kommandogruppe aus Abschnitt 0.1 betroffen, nur der Vollständigkeit halber notiert |
| G5 | fehlt | — | ohne Wirkung, G6 deckt `:HARMonics` bereits ab |
| FL | fehlt | `:FLICker` | Rang 10 (Flicker-Teil) an diesem Gerät **nicht ansprechbar** |
| DA | fehlt | `:AOUTput` | Analogausgang an diesem Gerät **nicht ansprechbar** (war schon niedrige Priorität) |
| MTR | fehlt, aber ohne Bedeutung | `:MOTor` | **ANSPRECHBAR** — siehe Motor-Befund unten; `MTR` ist an diesem Gerät kein zuverlässiger Indikator |

**Motor-Befund, Rang 8 — geklärt (Nachtrag 21.08.2026, zweiter Lauf):**
Der Modellcode `760304-40-MV` enthält `-MV` (Handbuch: Motor-Modellvariante),
`*OPT?` meldet **kein** `MTR` — die beiden Indizien widersprachen sich im
ersten Lauf. `frage_1_identitaet_und_optionen()` sendet seither zusätzlich
`:MOTor:PM?` (Handbuch 6-81, ein reiner Query) und trifft damit die
Entscheidung direkt, statt nur aus den beiden Indizien zu schließen. Ergebnis
des zweiten Laufs: `:MOTor:PM?` → `1.0000;"W"` — das Gerät antwortet.
**`:MOTor` ist an diesem Gerät ANSPRECHBAR.** Damit ist auch der Widerspruch
aufgelöst: der Modellcode (`-MV`) war der zuverlässige Indikator, `*OPT?`s
`MTR`-Code war es an diesem Gerät nicht — die theoretische Erwartung aus
Abschnitt 0.1, `*OPT?` melde die "motor evaluation function (MTR)", trägt
hier nicht. **Rang 8 ist damit zur Umsetzung freigegeben,** keine
Modellvariante mehr zu prüfen.

**Frage 2 (Panel-Sperre), Teilfrage (a) — beantwortet:** `:COMMunicate:LOCKout?`,
`:SYSTem:KLOCk?` und `:SYSTem:SLOCk?` sind alle drei ansprechbar und stehen
aktuell auf `0` (aus). Teilfrage (b) — Verhalten bei Verbindungsabbruch — ist
ein Schreibvorgang und bleibt offen; **vorerst zurückgestellt (Nutzerentscheidung
2026-08-21), kann bis auf Weiteres ignoriert werden.**

**Frage 3 (CBCycle Trigger/Sync) — Konfigurationsteil beantwortet:**
Sync-Quelle `U1` (interner Messkanal, keine externe Beschaltung nötig),
Slope `RISE`, Trigger-Modus `AUTO` (läuft frei, wartet nicht auf ein Ereignis),
Trigger-Quelle `U1`, Level `10.0 %`, Timeout `10 s`, Zustand `RESet`. In der
Werkseinstellung dieses Geräts ist also **keine externe Verkabelung nötig**.
Offen bleibt weiterhin nur der Wirkungsteil — ob `*TRG` allein einen
synchronisierten Start auslöst (Schreibkommando, eigenes Skript nötig).

**Frage 4 (`:INTEGrate:RTIMe?`) — Hypothese am Gerät bestätigt:** zwei Abfragen
im Abstand von 2 s liefern denselben Wert
(`2006,1,1,0,0,0;2006,1,1,1,0,0`). `:INTEGrate:TIMer?` steht auf `0,0,0`
(nicht konfiguriert), Modus `NORM`, Zustand `RES` (kein Lauf aktiv). Die
Analyseannahme aus Abschnitt 5 trägt am realen Gerät nicht — RTIMe ist die
Start-/Stoppzeit, kein Restzeitzähler. Empfehlung unverändert: Fortschritt =
`:INTEGrate:TIMer?` minus NUMeric-Item `TIME`.

**Frage 5 (UPD-Bit) — gemessen statt vermutet, mit klarem Ergebnis:** bei
`:RATE?` = `1.000 s` wurden in 10 s **3556 Proben** auf `:STATus:CONDition?`
genommen (Rundlaufzeit 1,3 ms min / 2,8 ms Mittel / 125,0 ms max). **UPD=1 in
0 von 3556 Proben (0,0 %)** — über zehn volle Aktualisierungszyklen hinweg
keine einzige 1→0-Flanke. **Antwort auf Frage 5: reines Polling auf das
UPD-Bit trägt M3-3 an diesem Gerät NICHT als alleinigen `sleep()`-Ersatz.**
Die Hochphase ist entweder kürzer, als selbst eine Rundlaufzeit von wenigen
Millisekunden auflösen kann, oder das Bit verhält sich bei dieser
Aktualisierungsrate anders als im Handbuchbeispiel unterstellt. Für M3-3
bleiben zwei Wege: über `:STATus:FILTer1 FALL` + `:STATus:EESE` und
Service-Request gehen (Schreibzugriff nötig, noch nicht geprüft) — oder direkt
mit einer Dublettenerkennung als Rückfallebene planen, statt sie nur als
Absicherung vorzusehen.

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

| Rang | Baustein | Option nötig? | Warum | Am Gerät (0.3, 21.08.2026) |
|---|---|---|---|---|
| 0 | `*OPT?` in `DeviceInfo` auswerten | keine (Common Command) | Voraussetzung für alle optionsgebundenen Punkte unten — sollte vor Rang 3, 5, 8, 10 stehen, damit keine Arbeit an nicht vorhandener Hardware entsteht | Abfrage funktioniert und ist geprüft (`probe_capabilities.py`) — Übernahme in `DeviceInfo` selbst steht noch aus |
| 1 | `IntegratorControl` (`:INTEGrate`) — Wh/Ah-Messung steuern | **nein** | Kernfunktion eines Leistungsmessgeräts, heute nicht steuerbar | unverändert; `:INTEGrate:STATe?` antwortet (`RES`) |
| 2 | `ComputationConfig` (`:MEASure`, insb. Averaging) | **nein** (außer Delta-Teil, siehe unten) | Betrifft praktisch jede Messung, nicht nur Spezialfälle | Delta-Teil **freigegeben** — `DT` ist verbaut |
| 3 | `HarmonicsConfig` (`:HARMonics`) | **`/G5` oder `/G6`** | Einer der Hauptanwendungsfälle des WT3000 — aber erst nach `*OPT?`-Check angehen | **freigegeben** — `G6` ist verbaut (obwohl `G5` fehlt) |
| 4 | Steuerbares Mess-Objekt + Trigger (`*TRG`/`GET`, `STATus:CONDition?`-Polling auf UPD-Bit) | **nein** | Grundlage für 2.1, 2.6 und robuste Automatisierung; Ereignismechanismus jetzt am Handbuch belegt (Abschnitt 0.2), nicht mehr nur Vermutung | UPD-Polling **widerlegt** (0 Treffer in 3556 Proben) — Weg über EESE/SRQ oder Dublettenerkennung nötig |
| 5 | `:CBCycle` (zyklus-/ereignisgetriggerte Messung) | **`/CC`** | Für synchrone/getriggerte Anwendungsfälle jenseits der freilaufenden Schleife | **freigegeben** — `CC` ist verbaut, Werksconfig braucht keine externe Verkabelung |
| 6 | Erweiterter `SessionBackup` (inkl. Averaging/Harmonics/Motor) | folgt den Gruppen, die er sichert | Sicherheitsnetz, sobald 2–3 neue schreibbare Gruppen existieren | unverändert |
| 7 | Panel-Sperre (`COMMunicate:LOCKout` und/oder `SYSTem:KLOCk`) | **nein** | Kleiner Aufwand, spürbarer Schutz bei unbeaufsichtigten Läufen; beide Kommandos jetzt im Detail bekannt (Abschnitt 3) | alle drei Wege ansprechbar, aktuell aus; Verhalten bei Verbindungsabbruch **vorerst zurückgestellt** |
| 8 | `:MOTor` (Motor-Wirkungsgrad) | **Modellvariante `-MV`**, keine Nachrüstoption | Nur falls das konkrete Gerät die MV-Variante ist — per `*IDN?` (Modellcode) klärbar, nicht per `*OPT?` | **freigegeben** — `:MOTor:PM?` antwortet (`1.0000;"W"`); Modellcode war der zuverlässige Indikator, `*OPT?`s `MTR` nicht |
| 9 | `:STORe`/`:FILE` (geräteseitige Datenverwaltung) | **nein** | Ergänzung, kein Ersatz für die vorhandene Python-Messschleife; `STORe:SMODe INTEGrate` koppelt Speicherung direkt an Integrationszyklen | unverändert |
| 10 | `:FLICker`, `:ACQuisition` (Rohabtastdaten), `:IMAGe` | `/FL` bzw. `/G6` (IMAGe optionsfrei) | Nischenfälle — nur bei konkretem Bedarf | `:FLICker` **entfällt** (`FL` fehlt); `:ACQuisition` **freigegeben** (`G6` verbaut) |
| — | `:WAVeform` (Anzeige-Wellenform, 1002 Punkte) | **nein** (Korrektur ggü. erster Fassung) | Optionsfrei, aber weiterhin niedrige Priorität laut ROADMAP „bewusst nicht enthalten" | unverändert |
| — | `:AOUTput`, `:HCOPy` | `/DA` bzw. `/B5`/`/C7` | Für einen programmatischen Treiber kaum relevant, entfallen kann geprüft werden | `:AOUTput` **entfällt** (`DA` fehlt); `:HCOPy` technisch ansprechbar (`B5`+`C7` verbaut), Einschätzung „kann entfallen" bleibt |

---

## 5 — Offene Fragen für den nächsten Geräte-/Optionscheck

**Update 21.08.2026:** Alle fünf Fragen dieses Abschnitts wurden gegen das
reale Gerät geprüft — Details, Rohwerte und Protokollpfad stehen in
Abschnitt 0.3. Zusammenfassung je Frage:

* ~~`*OPT?` und `*IDN?` am Gerät abfragen~~ — **beantwortet.** Modell
  `760304-40-MV`, Firmware `F5.01`, verbaute Optionen `G6, B5, DT, C7, C5, CC`.
  Damit ist auch geklärt, welche der optionsgebundenen Gruppen aus Abschnitt
  0.1 an diesem Gerät ansprechbar sind (siehe Tabelle in 0.3 und die
  „Am Gerät"-Spalte oben) — kein Rätselraten mehr für Rang 3, 5, 8, 10. Der
  anfängliche Widerspruch bei Rang 8 (Motor) ist im zweiten Lauf per
  `:MOTor:PM?` direkt aufgelöst worden, siehe 0.3.
* Panel-Sperr-Weg (`COMMunicate:LOCKout` vs. `SYSTem:KLOCk`/`SLOCk`) —
  **Teilfrage (a) beantwortet:** alle drei Wege existieren am Gerät, sind
  ansprechbar und stehen aktuell auf aus. **Teilfrage (b)** — Verhalten bei
  Verbindungsabbruch — bleibt technisch offen (braucht ein Schreibskript mit
  hartem Prozessabbruch), ist aber **vorerst zurückgestellt** (Entscheidung
  vom 21.08.2026) **und kann bis auf Weiteres ignoriert werden.**
* Reicht `*TRG`/`GET` allein für synchronisierten Start, oder braucht
  `:CBCycle` zusätzlich eine externe Triggerquelle? — **Konfigurationsteil
  beantwortet:** Werkseinstellung ist Sync-Quelle `U1` (interner Messkanal)
  und Trigger-Modus `AUTO` (frei laufend) — keine externe Beschaltung nötig.
  Der Wirkungsteil (löst `*TRG` allein eine Messung aus?) bleibt offen,
  braucht ein Schreibkommando und ist von geringerer Priorität, seit der
  Konfigurationsteil geklärt ist.
* ~~Liefert `:INTEGrate:RTIMe?` einen belastbaren Fortschritts-/Restzeitwert?~~
  — **beantwortet: nein.** Zwei Abfragen im Abstand von 2 s liefern denselben
  Wert; RTIMe ist die Start-/Stoppzeit des Echtzeitmodus, kein Zähler.
  Fortschritt muss stattdessen aus `:INTEGrate:TIMer?` minus NUMeric-Item
  `TIME` berechnet werden.
* ~~Wie zuverlässig/schnell schaltet das UPD-Bit um?~~ — **beantwortet:
  unzuverlässig genug, um allein nicht zu genügen.** 0 von 3556 Proben in 10 s
  trafen UPD=1. M3-3 braucht entweder den EESE/`FILTer`+Service-Request-Weg
  (noch ungeprüft, Schreibzugriff nötig) oder eine Dublettenerkennung als
  tragenden Mechanismus statt nur als Rückfallebene.

**Verbleibend offen:**
1. Wirkungsteil von `*TRG`/`GET` (löst es tatsächlich eine synchronisierte
   Messung aus?) — echtes Schreibkommando, braucht ein eigenes Skript;
   niedrige Priorität, seit der Konfigurationsteil geklärt ist.

Teilfrage (b) der Panel-Sperre ist davon ausdrücklich ausgenommen — zurückgestellt, siehe oben.
Rang 8 (Motor) ist mit dem zweiten Lauf (siehe 0.3) vollständig geklärt und
aus dieser Liste entfernt.
