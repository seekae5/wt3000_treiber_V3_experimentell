# Kommentar-Aufräumung in `wt3000_input.py`

**Datum:** 2026-08-19
**Art:** reine Aufräumarbeit — **keine Verhaltensänderung**
**Vorbild:** [AENDERUNGEN_2026-08-19_kommentare-core.md](AENDERUNGEN_2026-08-19_kommentare-core.md), gleiches Prinzip
**Stand:** 204 Tests grün (unverändert), `pyflakes` ohne Meldung

| | vorher | nachher |
|---|---|---|
| Zeilen | 1557 | **1523** |
| davon Kommentarzeilen | 189 (12 %) | **156 (10 %)** |
| Meilenstein-Marker | 18 | **0** |

**Nachweis:** der AST beider Fassungen ist nach Entfernen aller Docstrings
identisch. Ein einziger Docstring wurde angefasst (`restore_input_snapshot`),
inhaltlich unverändert.

---

## Vorbemerkung zum Umfang

Der Gewinn ist hier klein — 34 Zeilen gegenüber 173 in `wt3000_core.py`. Das war
erwartbar und ich hatte es vorher so eingeschätzt: diese Datei enthielt **keinen
Archivblock**, und ihr Kommentaranteil lag mit 12 % ohnehin im normalen Bereich.
Der eigentliche Ertrag ist deshalb nicht die Zeilenzahl, sondern dass die
**18 Meilenstein-Präfixe verschwunden sind** — der Leser stolpert nicht mehr
über `UEBERARBEITET (INPUT-13)`, um dann festzustellen, dass darunter eine
geltende Regel steht.

---

## Was entfernt wurde

### Meilenstein-Präfixe — alle 18
`UEBERARBEITET (INPUT-13)` (7×), `UEBERARBEITET/NEU (M0-1)` (6×),
`UEBERARBEITET (F-05)` (2×), `NEU (ROADMAP M1-1)`, `UEBERARBEITET (Punkt 4,
src-Layout)`. Was sie erklärten, steht jetzt in Gegenwartsform da — oder gar
nicht mehr, wo es reine Vorgeschichte war.

### Fehlergeschichten, die in den Änderungsdokumenten stehen
Drei Blöcke waren Erzählungen darüber, *was einmal kaputt war*:

* Der 15-Zeilen-Block über den Wegfall von `_token_match()` → auf 8 Zeilen
  gekürzt. Geblieben ist die **geltende Regel**: eine Regel für Vergleich,
  Wiederherstellung und Rückleseproben, Normalisierung auf die Langform, kein
  freies Präfixmatching (mit der SIGMA/SIGMB-Begründung).
* Die beiden F-05-Blöcke in `set_sync_source()` und `_set_mode()` → von 12 bzw.
  8 auf je 4 Zeilen. Geblieben ist, **warum** erst normalisiert und dann geprüft
  wird — dass das Gerät Kurzformen meldet und `restore_input_snapshot()` sie
  wieder hereinreicht. Die Vorgeschichte steht in
  [AENDERUNGEN_2026-08-18.md](AENDERUNGEN_2026-08-18.md).
* Der Messmodus-Block in `restore_input_snapshot()` → von 5 auf 2 Zeilen.
  Geblieben ist die operative Anweisung: `GROUP_MODE` muss der Aufrufer
  freigeben.

### Archäologie bei den Bereichs-Settern
Beim **Spannungsbereich** ist die Frage am Gerät geklärt — dort sind
`# Vorher: format_voltage(value),` und der `NEU (M0-1)`-Vermerk entfallen. Übrig
bleibt eine Zeile: `format_nrf(value),  # am Geraet belegt: '1000', nicht '1000V'`.

### Kopfzeile
„Deckt die **bisher fehlenden** Stellgrößen ab" → „Abgedeckte Stellgrößen".
Ebenso der Satz „Ändert nichts an wt3000_core.py, …" — das war eine Aussage über
einen Bearbeitungsschritt, nicht über das Modul.

---

## Was bewusst geblieben ist

### Der stillgelegte Block `format_voltage()` / `format_current()` — **nicht gelöscht**

Das ist der wichtigste Unterschied zu `wt3000_core.py`. Dort trug der
Archivblock die Anweisung *„Beim naechsten Aufraeumen ersatzlos zu loeschen"* —
unbedingt, also ausgeführt. Hier lautet die Bedingung:

> *bis der Geraetetermin auch den Sensor- und den Direktstromknoten bestaetigt hat*

Diese Bedingung ist **nicht erfüllt**. In der [ROADMAP.md](ROADMAP.md) ist M0-1
nicht als umgesetzt markiert, und am Gerät belegt ist bisher nur der
Spannungsknoten. Fällt bei den ausstehenden Proben doch die Einheitenform an,
wird der Code wieder gebraucht.

Der Block bleibt also stehen — umformuliert von einer Änderungsnotiz zu einem
stehenden Hinweis (`STILLGELEGT, nicht geloescht - offener Punkt ROADMAP M0-1`)
mit klarer Abbruchbedingung in beide Richtungen.

### Alle vier `ZU VERIFIZIEREN`-Marken
Unverändert vier, vorher wie nachher. Sie bezeichnen offene **Gerätefragen**
(Line-Filter-Umfang, Wiring-Units über zwei hinaus, Direktstrom- und
Sensorsyntax), keine Historie. Die beiden M0-1-Marken habe ich gestrafft und mit
dem ROADMAP-Verweis versehen, statt ihn im Fließtext zu verstecken.

### Die metrologischen Warnungen
Unangetastet: die GRUNDREGEL im Dateikopf, `# Skalierung EIN/AUS zuletzt, damit
nie ein Zwischenzustand mit falschem Faktor entsteht`, `# Auto-Range NACH dem
Bereich`, die Reihenfolgebegründungen in `restore_input_snapshot()`. Das sind
Sicherheitsregeln, die man dem Code nicht ansieht.

### Sämtliche Docstrings
Als API-Dokumentation. Einzige Ausnahme: in `restore_input_snapshot()` stand ein
`UEBERARBEITET (INPUT-13)`-Absatz im Docstring — er ist in Gegenwartsform
umformuliert, inhaltlich unverändert.

---

## Nicht gemacht

Die in der letzten Sitzung besprochene **Aufteilung der Datei** (`models` /
`access` / `snapshot`) ist hier nicht enthalten. Sie gehört hinter die
Parser-Bereinigung B-03, wie besprochen — und eine Aufräumung, die nur Kommentare
anfasst, lässt sich getrennt prüfen. Der AST-Vergleich oben wäre nach einer
Aufteilung nicht mehr möglich.
