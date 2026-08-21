# =============================================================================
# Datei: tools/hardware/probe_capabilities.py
#
# GERAETESKRIPT. Baut eine echte Verbindung auf und FRAGT NUR AB.
#
# Liegt bewusst nicht unter tests/: die Testsuite laeuft ohne Geraet und ohne
# tmctl.dll, und tests/conftest.py setzt das aktiv durch. Aufruf:
#
#     python tools/hardware/probe_capabilities.py
#
# (verlangt ein installiertes Paket - 'pip install -e .' - oder PYTHONPATH=src)
#
# WICHTIG - NICHTS AUS tests/ IMPORTIEREN. Begruendung siehe Kopf von
# probe_setWiring.py: ein einziges 'from tests.conftest import ...' legt
# TmctlTransport still und laesst dieses Skript am Geraet abbrechen.
#
# ZWECK
# -----
# Beantwortet die offenen Fragen aus docs/ANALYSE_FEHLENDE_FUNKTIONEN.md,
# Abschnitt 5 ("Offene Fragen fuer den naechsten Geraete-/Optionscheck") in
# einem Lauf. Ausgangspunkt war Frage 1 (*OPT? und *IDN?); die uebrigen vier
# Fragen sind mitgenommen, soweit sie sich rein lesend beantworten lassen -
# was fuer drei von ihnen ganz und fuer zwei teilweise gilt. Was NICHT lesbar
# ist, sagt das Protokoll ausdruecklich, statt eine Luecke offen zu lassen:
#
#   Frage 1  *OPT? / *IDN?                   -> vollstaendig beantwortet
#   Frage 2  Panel-Sperre LOCKout/KLOCk      -> teilweise (siehe frage_2)
#   Frage 3  '*TRG' allein oder :CBCycle?    -> Konfigurationsteil beantwortet
#   Frage 4  :INTEGrate:RTIMe? als Restzeit  -> vollstaendig beantwortet
#   Frage 5  UPD-Bit als sleep()-Ersatz      -> gemessen statt vermutet
#
# NUR-LESEN IST HIER KEINE ABSICHTSERKLAERUNG, SONDERN GESPERRT
# ------------------------------------------------------------
# Die Sitzung wird mit 'read_only=True' geoeffnet. WTSession._validate()
# weist damit JEDE Nachricht ohne '?' mit ReadOnlyViolation zurueck, bevor sie
# den Transport erreicht. Das ist der Grund, warum dieses Skript im Gegensatz
# zu probe_setWiring.py und probe_voltage_range.py keine Sicherung und keine
# Rueckstellung braucht: es gibt nichts zurueckzustellen, und ein
# versehentlich ergaenztes Schreibkommando faellt sofort auf, statt am Geraet
# zu landen.
#
# Aus demselben Grund fehlt hier die Modulkonstante USE_REMOTE der beiden
# Schreibproben: ':COMMunicate:REMote ON' IST ein Schreibkommando und wuerde
# an der Sperre scheitern. Fuer reine Abfragen braucht es die Fernsteuerung
# nicht - das Geraet beantwortet Queries auch im LOCAL-Zustand.
#
# Eine Folge davon betrifft Frage 2 und 3: die Panel-Sperre und '*TRG' sind
# Schreibvorgaenge. Ihr VERHALTEN kann dieses Skript deshalb nicht pruefen,
# nur ihren aktuellen Zustand und ihre Konfiguration lesen. Was fuer die
# vollstaendige Antwort noch fehlt, steht in der jeweiligen Funktion und geht
# ins Protokoll.
#
# UMGANG MIT NICHT VORHANDENEN GRUPPEN
# ------------------------------------
# Ein Query auf eine Gruppe, deren Option nicht verbaut ist, ist KEIN Fehler
# dieses Skripts, sondern eines seiner Ergebnisse. Fehlt die Option, legt das
# Geraet einen Eintrag in die Fehlerqueue und antwortet nicht - der Query
# laeuft in den Timeout (TmctlError, eine WTError). '_query()' faengt das ab,
# raeumt die nachlaufende Antwort und die Fehlerqueue ab und liefert None.
# Ohne dieses Abraeumen liefe der naechste Query auf eine fremde Antwort auf.
# =============================================================================

from __future__ import annotations

import logging
import time
from datetime import datetime
from pathlib import Path

from wt3000_scpi.wt3000_common import (
    output_dir,
    parse_condition,
    parse_nr3,
    setup_logging,
    strip_response_header,
)
from wt3000_scpi.wt3000_core import (
    TmctlTransport,
    WTConfig,
    WTError,
    WTSession,
    config_file_in_use,
)

# ---------------------------------------------------------------------------
# Laufparameter
# ---------------------------------------------------------------------------

#: Dauer der UPD-Messung (Frage 5) in Sekunden. Bei der Voreinstellung
# ':RATE 500ms' liegen darin rund 20 Aktualisierungen - genug fuer eine
# Aussage ueber die Streuung, ohne den Lauf lang zu machen.
UPD_PROBE_SECONDS: float = 10.0

#: Pause zwischen zwei ':STATus:CONDition?' waehrend der UPD-Messung.
# Bewusst 0.0: gemessen werden soll die tatsaechlich erreichbare Aufloesung
# des Pollings, und die wird von der Rundlaufzeit des Busses bestimmt, nicht
# von einer selbst gewaehlten Pause. Eine Pause hier verfaelschte genau die
# Groesse, um die es in Frage 5 geht.
UPD_POLL_PAUSE_S: float = 0.0

#: Toleranz, innerhalb derer ein Flankenabstand als "passt zur Update-Rate"
# gilt (Frage 5).
UPD_RATE_TOLERANCE: float = 0.25

#: Bit 0 des Condition-Registers: UPD (Updating). Die fallende Flanke 1->0
# bedeutet laut Handbuch Kap. 7 "Messdaten fertig aktualisiert".
UPD_BIT: int = 1 << 0

#: Abstand der beiden ':INTEGrate:RTIMe?'-Abfragen in Frage 4.
RTIME_ABSTAND_S: float = 2.0

#: Optionscode -> (betroffene Kommandogruppen, Fundstelle in der Analyse).
# Zusammengestellt aus docs/ANALYSE_FEHLENDE_FUNKTIONEN.md Abschnitt 0.1 und
# der Beschreibung zu '*OPT?' im Handbuch (Kap. 6, Seite 6-115).
OPTION_GROUPS: tuple[tuple[str, str, str], ...] = (
    ("G5", ":HARMonics", "Analyse 2.3 / Rang 3 - Oberschwingungen"),
    ("G6", ":HARMonics, :ACQuisition, :CURSor:FFT", "Analyse 2.3+2.7 / Rang 3+10"),
    ("CC", ":CBCycle", "Analyse 2.6 / Rang 5 - Zyklusmessung"),
    ("FL", ":FLICker", "Analyse 2.4 / Rang 10 - Flicker"),
    ("DA", ":AOUTput", "Analyse 2.10 - Analogausgang"),
    ("DT", ":MEASure:DMeasure, :COMPensation:V3A3", "Analyse 2.2 / Rang 2 - Delta"),
    ("B5", ":HCOPy (interner Drucker)", "Analyse 2.9 - kann entfallen"),
    ("C7", ":HCOPy (Netzdrucker), Ethernet", "Analyse 2.9 - kann entfallen"),
    ("MTR", ":MOTor", "Analyse 2.5 / Rang 8 - Motorauswertung"),
)

# Ablage an der Projektwurzel statt an 'Path.cwd()' - siehe
# wt3000_common.output_dir().
OUTPUT_DIR: Path = output_dir("konfiguration")


# ---------------------------------------------------------------------------
# Abfrage mit Abraeumen
# ---------------------------------------------------------------------------


def _query(session: WTSession, command: str, log: logging.Logger) -> str | None:
    """Einen Query absetzen. Liefert None, wenn das Geraet ihn nicht kennt.

    Der Kopf dieser Datei begruendet, warum ein Fehlschlag hier ein Ergebnis
    und kein Abbruchgrund ist. Wichtig ist die Reihenfolge im Fehlerfall:
    erst 'drain_after_failure()' - eine verspaetete Antwort abraeumen, sonst
    beantwortet sie den NAECHSTEN Query und der ganze Lauf ist um eine
    Position verschoben -, dann die Fehlerqueue leeren, sonst steht der
    Eintrag am Ende des Laufs noch drin und faellt der naechsten Sitzung zur
    Last.
    """
    try:
        antwort = strip_response_header(session.query(command))
    except WTError as error:
        log.warning("  %-40s -> nicht beantwortet (%s)", command, error)
        session.drain_after_failure()
        try:
            eintraege = session.read_error_queue()
        except WTError as folge:
            log.warning("  Fehlerqueue nach %s nicht lesbar: %s", command, folge)
            return None
        for eintrag in eintraege:
            if eintrag.split(",", 1)[0].strip().lstrip("+") != "0":
                log.info("  Fehlerqueue dazu: %s", eintrag)
        return None

    log.info("  %-40s -> %s", command, antwort)
    return antwort


# ---------------------------------------------------------------------------
# Frage 1 - *IDN? und *OPT?
# ---------------------------------------------------------------------------


def frage_1_identitaet_und_optionen(
    session: WTSession, log: logging.Logger
) -> tuple[str | None, frozenset[str]]:
    """'*IDN?' und '*OPT?' abfragen und gegen die Optionstabelle halten.

    Rueckgabe: (Modellcode oder None, Menge der Optionscodes).

    Zur Reihenfolge: '*OPT?' steht ABSICHTLICH als letzter Query dieses
    Abschnitts. Das Handbuch (6-115) sagt dazu: "The *OPT? query must be the
    last query of the program message. An error occurs if there is a query
    after this query." Gemeint ist die einzelne Programmnachricht, und
    WTSession sendet ohnehin genau einen Query je Nachricht - _validate()
    weist mehr als ein '?' zurueck. Die Regel ist hier also schon durch die
    Bauart eingehalten; die Reihenfolge kostet nichts und haelt das Skript
    auch dann richtig, wenn spaeter jemand Queries buendelt.

    Zur Motorfrage: die Analyse (Rang 8) geht davon aus, die Motor-Variante
    sei NUR ueber den Modellcode aus '*IDN?' erkennbar, nicht ueber '*OPT?'.
    Die Handbuchbeschreibung zu '*OPT?' nennt daneben aber ausdruecklich die
    "motor evaluation function (MTR)" als gemeldete Option. Welcher der
    beiden Wege am konkreten Geraet traegt, wird hier nicht laenger nur
    abgeleitet: ':MOTor:PM?' - ein Query aus der Gruppe selbst, siehe
    Handbuch 6-81 ("Queries all settings related to the motor output") -
    entscheidet direkt und unabhaengig von beiden Indizien. Antwortet das
    Geraet, ist die Gruppe ansprechbar; bleibt die Antwort aus (Timeout,
    genau wie bei einer fehlenden Option ueblich), ist sie es nicht. Modell-
    code und '*OPT?' werden trotzdem weiter ausgewertet und protokolliert -
    sie sind der Grund, warum ueberhaupt geprueft wird, auch wenn der
    direkte Query am Ende das letzte Wort hat.
    """
    log.info("--- Frage 1: Identitaet und verbaute Optionen ---")

    identitaet = _query(session, "*IDN?", log)
    modell: str | None = None
    if identitaet:
        teile = [t.strip() for t in identitaet.split(",")]
        while len(teile) < 4:
            teile.append("")
        modell = teile[1] or None
        log.info("  Hersteller: %s", teile[0] or "?")
        log.info("  Modell:     %s", teile[1] or "?")
        log.info("  Seriennr.:  %s  (laut Handbuch immer 0)", teile[2] or "?")
        log.info("  Firmware:   %s", teile[3] or "?")
    else:
        log.error("  *IDN? ohne Antwort - ohne sie ist der Rest nur halb belastbar")

    rohantwort = _query(session, "*OPT?", log)
    if rohantwort is None:
        log.error("  *OPT? ohne Antwort - die Optionsfrage bleibt offen")
        return modell, frozenset()

    # '0' heisst laut Handbuch: keine einzige Option verbaut.
    codes = frozenset(
        teil.strip().upper().lstrip("/")
        for teil in rohantwort.split(",")
        if teil.strip() and teil.strip() != "0"
    )
    log.info("  Erkannte Optionscodes: %s", ", ".join(sorted(codes)) or "<keine>")

    log.info("  Auswirkung auf die Kommandogruppen aus Analyse 0.1:")
    for code, gruppen, fundstelle in OPTION_GROUPS:
        log.info(
            "    %-4s %-10s %-42s %s",
            code,
            "VORHANDEN" if code in codes else "fehlt",
            gruppen,
            fundstelle,
        )

    unbekannt = codes - {code for code, _, _ in OPTION_GROUPS}
    if unbekannt:
        log.info(
            "  Weitere gemeldete Optionen ohne Bezug zu Abschnitt 0.1: %s",
            ", ".join(sorted(unbekannt)),
        )

    # Motorvariante: zwei Indizien und der direkte Entscheid, siehe Docstring.
    modell_tokens = {t.strip().upper() for t in (modell or "").split("-")}
    motor_per_modell = "MV" in modell_tokens
    motor_per_opt = "MTR" in codes
    log.info(
        "  Motor-Indizien: *IDN?-Modellcode sagt %s, *OPT? sagt %s",
        "MV vorhanden" if motor_per_modell else "kein MV",
        "MTR vorhanden" if motor_per_opt else "kein MTR",
    )
    if motor_per_modell != motor_per_opt:
        log.warning("  Die beiden Indizien widersprechen sich - der direkte Query entscheidet:")

    motor_antwort = _query(session, ":MOTor:PM?", log)
    motor_ansprechbar = motor_antwort is not None
    log.info(
        "  BEFUND Rang 8: ':MOTor:PM?' %s - Gruppe ':MOTor' ist an diesem "
        "Geraet %s.",
        "beantwortet" if motor_ansprechbar else "nicht beantwortet (Timeout)",
        "ANSPRECHBAR" if motor_ansprechbar else "NICHT ansprechbar",
    )
    if motor_ansprechbar and not motor_per_opt:
        log.info(
            "  Damit ist auch das Indiz aus '*OPT?' eingeordnet: MTR fehlt in "
            "der Optionsliste, obwohl die Gruppe antwortet - MTR ist an "
            "diesem Geraet offenbar kein zuverlaessiger Indikator, der "
            "Modellcode ('-MV') war es hier."
        )
    elif not motor_ansprechbar and motor_per_modell:
        log.info(
            "  Damit ist auch das Indiz aus '*IDN?' eingeordnet: das Modell "
            "traegt '-MV', die Gruppe antwortet trotzdem nicht - der "
            "Modellcode allein war hier kein zuverlaessiger Indikator."
        )

    return modell, codes


# ---------------------------------------------------------------------------
# Frage 2 - Panel-Sperre
# ---------------------------------------------------------------------------


def frage_2_panel_sperre(session: WTSession, log: logging.Logger) -> None:
    """Zustand der drei Sperrwege lesen.

    TEILANTWORT, und das mit Absicht. Die Frage in Abschnitt 5 hat zwei
    Haelften:

      (a) "Welcher der beiden Wege ist tatsaechlich gewuenscht?" - dafuer muss
          belegt sein, dass beide Wege am Geraet ueberhaupt existieren und
          welchen Zustand sie gerade haben. Das leistet dieser Abschnitt.

      (b) "Wie verhaelt er sich beim Verbindungsabbruch - bleibt die Sperre
          haengen, wenn die Python-Sitzung abstuerzt?" - das ist NICHT lesbar.
          Es braucht ein Schreibkommando, einen absichtlich abgebrochenen
          Prozess und eine zweite Sitzung, die danach nachsieht. Dieses Skript
          ist nur-lesend (siehe Dateikopf) und kann das nicht leisten.

    Fuer (b) waere ein eigenes Schreibskript noetig, gebaut wie
    probe_setWiring.py: Ausgangszustand lesen, sperren, Prozess hart beenden,
    in einer ZWEITEN Sitzung den Zustand erneut lesen. Es steht bewusst nicht
    hier - eine haengende Panel-Sperre ist genau der Zustand, den man nicht
    versehentlich hinterlaesst, und dieses Skript soll unbeaufsichtigt laufen
    duerfen.

    Ein Nebenbefund faellt trotzdem ab: steht eine der Sperren JETZT schon auf
    ON, ohne dass gerade jemand sie gesetzt hat, ist (b) damit praktisch
    beantwortet - dann ueberdauert sie die Sitzung, die sie gesetzt hat.
    """
    log.info("--- Frage 2: Panel-Sperre (Teilantwort, siehe Docstring) ---")

    zustaende = (
        (":COMMunicate:LOCKout?", "Local Lockout auf Busebene (LLO)"),
        (":SYSTem:KLOCk?", "Tastensperre am Geraet"),
        (":SYSTem:SLOCk?", "SHIFT-Dauerzustand"),
    )
    aktiv: list[str] = []
    for befehl, bedeutung in zustaende:
        antwort = _query(session, befehl, log)
        if antwort is None:
            log.info("    %s: Kommando nicht beantwortet", bedeutung)
            continue
        an = antwort.strip().upper() in {"1", "ON", "TRUE"}
        log.info("    %s: %s", bedeutung, "AN" if an else "aus")
        if an:
            aktiv.append(befehl.rstrip("?"))

    if aktiv:
        log.warning(
            "  BEFUND zu Teilfrage (b): %s steht schon VOR diesem Lauf auf AN. "
            "Eine Sperre ueberdauert also die Sitzung, die sie gesetzt hat - "
            "jede Umsetzung von Rang 7 braucht die Ruecknahme im 'finally', "
            "so wie 'disable_remote()' es heute schon macht.",
            ", ".join(aktiv),
        )
    else:
        log.info(
            "  Alle drei Wege sind aus und alle drei sind abfragbar - "
            "Teilfrage (a) ist damit entscheidbar. Teilfrage (b), das "
            "Verhalten beim Verbindungsabbruch, bleibt offen und braucht ein "
            "eigenes Schreibskript (siehe Docstring)."
        )


# ---------------------------------------------------------------------------
# Frage 3 - Trigger fuer synchronisierten Start
# ---------------------------------------------------------------------------


def frage_3_trigger(session: WTSession, log: logging.Logger, optionen: frozenset[str]) -> None:
    """Klaeren, ob ':CBCycle' eine externe Quelle braucht.

    Die Frage lautet: reicht '*TRG'/'GET' allein fuer einen synchronisierten
    Start, oder braucht ':CBCycle' zusaetzlich eine externe Triggerquelle?

    Der zweite Teil ist lesbar und wird hier beantwortet:
    ':CBCycle:SYNChronize:SOURce?' sagt, ob die Synchronisierung an einem
    Messkanal (U<x>/I<x>) oder am externen Takteingang (EXTernal) haengt, und
    ':CBCycle:TRIGger:MODE?' sagt, ob ueberhaupt auf ein Triggerereignis
    gewartet wird (NORMal) oder frei durchgelaufen wird (AUTO). Steht die
    Quelle auf U1 und der Modus auf AUTO, ist keine externe Beschaltung
    noetig - das war der eigentliche Zweifel.

    Der erste Teil ist NICHT lesbar: '*TRG' ist ein Schreibkommando ohne '?'
    und scheitert in dieser Sitzung an der Nur-Lesen-Sperre. Ob es allein
    genuegt, entscheidet sich ausserdem erst an der WIRKUNG (loest es eine
    Einzelmessung aus?) und nicht an einer Antwort. Das gehoert in dasselbe
    Schreibskript wie Frage 2 (b).
    """
    log.info("--- Frage 3: Trigger und Synchronisierung ---")

    if "CC" not in optionen:
        log.info(
            "  Option /CC ist nicht verbaut - die :CBCycle-Gruppe ist an "
            "diesem Geraet nicht ansprechbar. Damit ist die Frage fuer diese "
            "Einheit entschieden: Rang 5 der Prioritaetenliste faellt weg, ein "
            "synchronisierter Start muss ohne :CBCycle auskommen."
        )
        log.info(
            "  Die Abfragen laufen trotzdem, um den Befund zu BELEGEN statt "
            "ihn nur aus '*OPT?' abzuleiten:"
        )

    quelle = _query(session, ":CBCycle:SYNChronize:SOURce?", log)
    _query(session, ":CBCycle:SYNChronize:SLOPe?", log)
    modus = _query(session, ":CBCycle:TRIGger:MODE?", log)
    _query(session, ":CBCycle:TRIGger:SOURce?", log)
    _query(session, ":CBCycle:TRIGger:LEVel?", log)
    _query(session, ":CBCycle:TIMEout?", log)
    _query(session, ":CBCycle:STATe?", log)

    if quelle is None and modus is None:
        log.info(
            "  Keine Antwort auf die :CBCycle-Abfragen - deckt sich mit einem "
            "fehlenden /CC. Belegt: die Gruppe ist an dieser Einheit nicht "
            "nutzbar."
        )
        return

    braucht_extern = (quelle or "").strip().upper().startswith("EXT")
    wartet_auf_trigger = (modus or "").strip().upper().startswith("NORM")
    log.info(
        "  BEFUND: Sync-Quelle %s -> %s; Trigger-Modus %s -> %s",
        quelle or "?",
        "EXTERNE Beschaltung noetig" if braucht_extern else "interner Messkanal genuegt",
        modus or "?",
        "wartet auf ein Triggerereignis" if wartet_auf_trigger else "laeuft frei (AUTO)",
    )
    log.info(
        "  Offen bleibt der Wirkungsteil - ob '*TRG' allein ausreicht. "
        "Schreibkommando, siehe Docstring."
    )


# ---------------------------------------------------------------------------
# Frage 4 - :INTEGrate:RTIMe? als Fortschrittsanzeige
# ---------------------------------------------------------------------------


def frage_4_integrate_restzeit(session: WTSession, log: logging.Logger) -> None:
    """Pruefen, ob ':INTEGrate:RTIMe?' eine Rest-/Fortschrittszeit liefert.

    Die Frage in Abschnitt 5 unterstellt, RTIMe koenne waehrend einer
    laufenden Wh-Messung einen Fortschrittswert fuer eine UI liefern. Das
    Handbuch sagt etwas anderes (6-74): "Queries the integration start and
    stop times for real-time integration mode" - RTIMe ist das WANDUHR-Paar
    aus Start- und Stoppzeit des Echtzeit-Integrationsmodus, in der Form
    2005,1,1,0,0,0. Kein Zaehler, keine Restzeit.

    Dieser Abschnitt haelt die Antwort des Geraets dagegen, statt es bei der
    Handbuchstelle zu belassen: er fragt zweimal im Abstand ab. Zaehlt der
    Wert nicht herunter, ist die Annahme widerlegt.

    Die brauchbare Groesse fuer eine Fortschrittsanzeige ist eine andere:
    ':INTEGrate:TIMer?' liefert die eingestellte Gesamtdauer, und die
    VERSTRICHENE Integrationszeit ist ein NUMeric-Item mit der Funktion TIME
    (Handbuch zu ':NUMeric:FORMat': "<NR1> format only for the elapsed time of
    integration (TIME)"). Rest = TIMer - TIME. Dieses Item einzutragen waere
    ein Schreibvorgang und passiert hier nicht; der Hinweis steht im
    Protokoll, damit die Umsetzung von Rang 1 nicht wieder bei RTIMe landet.
    """
    log.info("--- Frage 4: :INTEGrate:RTIMe? als Restzeit ---")

    _query(session, ":INTEGrate:MODE?", log)
    zustand = _query(session, ":INTEGrate:STATe?", log)
    _query(session, ":INTEGrate:TIMer?", log)

    erste = _query(session, ":INTEGrate:RTIMe?", log)
    time.sleep(RTIME_ABSTAND_S)
    zweite = _query(session, ":INTEGrate:RTIMe?", log)

    if erste is None and zweite is None:
        log.warning("  ':INTEGrate:RTIMe?' nicht beantwortet - Frage bleibt offen")
    elif erste == zweite:
        log.info(
            "  BEFUND: RTIMe ist nach %.0f s unveraendert (%s). Bestaetigt das "
            "Handbuch - RTIMe ist die Start-/Stoppzeit des Echtzeitmodus und "
            "kein Restzeitzaehler. Die Annahme aus Abschnitt 5 traegt nicht.",
            RTIME_ABSTAND_S,
            erste,
        )
    else:
        log.warning(
            "  BEFUND: RTIMe hat sich veraendert (%s -> %s). Das widerspricht "
            "der Handbuchbeschreibung und ist vor der Umsetzung von Rang 1 "
            "genauer anzusehen.",
            erste,
            zweite,
        )

    log.info(
        "  Integrationszustand laut ':INTEGrate:STATe?': %s "
        "(RESet/READy/STARt/STOP/ERRor/TIMeup)",
        zustand or "?",
    )
    log.info(
        "  Fuer eine Fortschrittsanzeige gilt stattdessen: Rest = "
        "':INTEGrate:TIMer?' minus NUMeric-Item TIME (verstrichene "
        "Integrationszeit). Siehe Docstring."
    )


# ---------------------------------------------------------------------------
# Frage 5 - UPD-Bit als Ersatz fuer sleep()
# ---------------------------------------------------------------------------


def frage_5_upd_takt(session: WTSession, log: logging.Logger) -> None:
    """Das UPD-Bit ueber mehrere Sekunden pollen und den Takt vermessen.

    Frage aus Abschnitt 5: "Wie zuverlaessig/schnell schaltet das UPD-Bit in
    der Praxis um - reicht es als alleiniger Ersatz fuer sleep(), oder braucht
    M3-3 trotzdem eine Dublettenerkennung als Rueckfallebene?"

    Gemessen wird ueber ':STATus:CONDition?' und NICHT ueber ':STATus:EESR?'.
    Beide sehen dasselbe Bit, aber EESR? LOESCHT das Register beim Lesen -
    eine zweite Stelle im Programm, die dazwischen liest, bekaeme dann nichts
    mehr. Das Condition-Register ist ein Momentanzustand und vertraegt
    beliebig viele Leser. Ausserdem braeuchte der Weg ueber EESR erst
    ':STATus:FILTer1 FALL' und ':STATus:EESE 1' - zwei Schreibkommandos, die
    diese Sitzung nicht senden darf.

    Ausgewertet werden drei Groessen, und erst alle drei zusammen ergeben die
    Antwort:

      Rundlaufzeit    wie lange ein einzelner Query dauert. Sie ist die
                      Aufloesungsgrenze: ist die UPD-Hochphase kuerzer, kann
                      Polling die Flanke grundsaetzlich nicht sehen.
      Trefferquote    Anteil der Proben mit UPD=1. Ist er 0, war das Fenster
                      nie zu erwischen - dann ist die Frage mit "nein, Polling
                      allein reicht nicht" beantwortet.
      Flankenabstand  Abstand zweier 1->0-Flanken. Passt er zu ':RATE?',
                      traegt das Bit den Takt; liegt ein Abstand beim
                      Doppelten der Rate, wurde eine Flanke verpasst - genau
                      der Fall, fuer den es die Dublettenerkennung braucht.
    """
    log.info("--- Frage 5: UPD-Bit (Condition-Register Bit 0) ---")

    rate_roh = _query(session, ":RATE?", log)
    rate: float | None = None
    if rate_roh is not None:
        try:
            rate = parse_nr3(rate_roh, ":RATE")
            log.info("  Eingestellte Update-Rate: %.3f s", rate)
        except WTError as error:
            log.warning("  ':RATE?' nicht auswertbar: %s", error)

    log.info("  Polle %.1f s lang ':STATus:CONDition?' ...", UPD_PROBE_SECONDS)

    proben = 0
    hoch = 0
    flanken: list[float] = []
    dauern: list[float] = []
    vorher: bool | None = None
    ende = time.perf_counter() + UPD_PROBE_SECONDS

    try:
        while time.perf_counter() < ende:
            start = time.perf_counter()
            bits = parse_condition(session.query(":STATus:CONDition?"))
            fertig = time.perf_counter()

            proben += 1
            dauern.append(fertig - start)
            upd = bool(bits & UPD_BIT)
            if upd:
                hoch += 1
            # Fallende Flanke 1->0: laut Handbuch das Ende der Aktualisierung.
            if vorher and not upd:
                flanken.append(fertig)
            vorher = upd

            if UPD_POLL_PAUSE_S:
                time.sleep(UPD_POLL_PAUSE_S)
    except WTError as error:
        # Der Abbruch beendet nur diesen Abschnitt: was bis hierher gemessen
        # wurde, wird trotzdem ausgewertet - eine halbe Messreihe ist mehr als
        # keine, solange das Protokoll sagt, dass sie halb ist.
        log.warning("  Polling nach %d Proben abgebrochen: %s", proben, error)
        session.drain_after_failure()

    if not proben:
        log.error("  Keine einzige Probe zustande gekommen - Frage bleibt offen")
        return

    mittel = sum(dauern) / len(dauern)
    log.info(
        "  %d Proben, Rundlaufzeit min %.1f ms / mittel %.1f ms / max %.1f ms",
        proben,
        min(dauern) * 1000,
        mittel * 1000,
        max(dauern) * 1000,
    )
    log.info("  UPD=1 in %d von %d Proben (%.1f %%)", hoch, proben, 100.0 * hoch / proben)

    if not flanken:
        log.warning(
            "  BEFUND: keine einzige 1->0-Flanke in %.1f s. Bei einer "
            "Rundlaufzeit von %.1f ms ist die UPD-Hochphase zu kurz, um sie "
            "durch Pollen zuverlaessig zu treffen. Antwort auf Frage 5: "
            "Polling auf UPD allein traegt M3-3 NICHT - entweder ueber "
            "FILTer/EESE und Service-Request gehen (braucht Schreibzugriff) "
            "oder eine Dublettenerkennung als Rueckfallebene vorsehen.",
            UPD_PROBE_SECONDS,
            mittel * 1000,
        )
        return

    abstaende = [b - a for a, b in zip(flanken, flanken[1:])]
    if not abstaende:
        log.warning(
            "  BEFUND: nur eine Flanke in %.1f s - zu wenig fuer eine Aussage "
            "ueber den Takt. Messdauer erhoehen (UPD_PROBE_SECONDS) oder "
            "gleich die Dublettenerkennung vorsehen.",
            UPD_PROBE_SECONDS,
        )
        return

    log.info(
        "  %d Flanken, Abstand min %.3f s / mittel %.3f s / max %.3f s",
        len(flanken),
        min(abstaende),
        sum(abstaende) / len(abstaende),
        max(abstaende),
    )

    if rate is None:
        log.info(
            "  BEFUND: Flanken sind da und regelmaessig messbar, aber ohne "
            "gelesene ':RATE?' fehlt der Abgleich mit dem Sollwert."
        )
        return

    verpasst = [d for d in abstaende if d > rate * (1.0 + UPD_RATE_TOLERANCE)]
    if verpasst:
        log.warning(
            "  BEFUND: %d von %d Flankenabstaenden liegen ueber der "
            "Update-Rate + %.0f %% (laengster %.3f s bei Rate %.3f s). Es "
            "werden Flanken verpasst. Antwort auf Frage 5: UPD-Polling ist "
            "brauchbar, ersetzt sleep() aber nicht allein - M3-3 braucht die "
            "Dublettenerkennung als Rueckfallebene.",
            len(verpasst),
            len(abstaende),
            UPD_RATE_TOLERANCE * 100,
            max(abstaende),
            rate,
        )
    else:
        log.info(
            "  BEFUND: alle %d Flankenabstaende liegen innerhalb der "
            "Update-Rate +/- %.0f %% (Rate %.3f s). Antwort auf Frage 5: das "
            "UPD-Bit traegt den Takt zuverlaessig und kann das blinde sleep() "
            "in M3-3 ersetzen. Eine Dublettenerkennung bleibt als Absicherung "
            "gegen Bus-Aussetzer sinnvoll, ist aber nicht der tragende "
            "Mechanismus.",
            len(abstaende),
            UPD_RATE_TOLERANCE * 100,
            rate,
        )


# ---------------------------------------------------------------------------
# Ablauf
# ---------------------------------------------------------------------------


def main() -> int:
    """Alle fuenf Fragen abarbeiten. Rueckgabe: 0 = ok."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = OUTPUT_DIR / f"wt3000_probe_capabilities_{timestamp}.txt"

    setup_logging(log_file)
    log = logging.getLogger("wt3000.probe_capabilities")
    log.info("Protokolldatei: %s", log_file)
    log.info("Nur-Lesen-Lauf - dieses Skript sendet kein einziges Schreibkommando")

    try:
        # Aufloesungskette INNERHALB des try und HINTER setup_logging - siehe
        # Begruendung in stage2_read_numeric.main() (Befund A-08).
        log.info("Konfigurationsdatei: %s", config_file_in_use() or "<keine, Voreinstellungen>")
        config = WTConfig.from_environment()
        log.info("Verbindung: %s", config.describe())

        with TmctlTransport(config) as transport:
            # read_only=True ist die Sperre, nicht nur eine Absichtserklaerung -
            # siehe Dateikopf.
            session = WTSession(transport, config, read_only=True)

            # Der Treiber setzt ':COMMunicate:HEADer 0' voraus. Setzen kann
            # dieser Lauf es nicht (Schreibkommando), und er muss es auch
            # nicht: alle Antworten laufen durch strip_response_header(). Der
            # Hinweis steht trotzdem im Protokoll, damit ein abweichender
            # Zustand nicht erst beim Auswerten auffaellt.
            header = _query(session, ":COMMunicate:HEADer?", log)
            if header is not None and header.strip().upper() not in {"0", "OFF"}:
                log.warning(
                    "':COMMunicate:HEADer' steht auf %r statt '0'. Dieser Lauf "
                    "kommt damit zurecht, die Stufenskripte brechen dabei ab.",
                    header,
                )

            _, optionen = frage_1_identitaet_und_optionen(session, log)
            frage_2_panel_sperre(session, log)
            frage_3_trigger(session, log, optionen)
            frage_4_integrate_restzeit(session, log)
            frage_5_upd_takt(session, log)

            # Am Ende, nicht zwischendurch: '_query()' raeumt die Queue nach
            # jedem fehlgeschlagenen Query bereits ab. Was HIER noch steht,
            # stammt aus einem Query, der beantwortet WURDE und trotzdem einen
            # Eintrag erzeugt hat - das waere ein Befund fuer sich und darf
            # deshalb nicht still verschwinden.
            reste = session.read_error_queue()
            offen = [e for e in reste if e.split(",", 1)[0].strip().lstrip("+") != "0"]
            if offen:
                log.warning("Fehlerqueue am Ende nicht leer: %s", offen)
            else:
                log.info("Fehlerqueue am Ende leer")

        log.info("Fertig. Auswertung siehe %s", log_file)

    except WTError as error:
        log.error("Abbruch: %s", error)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
