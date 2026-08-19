# =============================================================================
# Datei: wt3000_device.py
# NEU (ROADMAP M1-1): Layer 4 - die Fassade.
#
# Hintergrund. Bis hierher musste jeder Anwender Transport, Sitzung,
# InputConfig, RangeAccess und die Wiring-Units von Hand zusammenstecken - so,
# wie es die fuenf Stufenskripte jeweils erneut vormachen. Besonders die
# Verdrahtung der Wiring-Units war eine Stolperfalle: wer
#     RangeAccess(session, allow_changes=True)
# ohne 'sigma_members' anlegt, bekommt bei jedem SIGMA-Scope einen Fehler, und
# zwar erst mitten im Ablauf. Die Zuordnung steht am Geraet zur Verfuegung -
# sie zu erfragen war nur nirgends vorgesehen.
#
# Diese Datei ist der einzige Einstiegspunkt, den ein Anwender braucht:
#
#     from wt3000_scpi import WT3000, Quantity
#
#     with WT3000.connect(ip="192.168.10.20") as wt:
#         wt.device.log_summary()
#         print(wt.input.get_wiring())
#         print(wt.ranges.dump(Quantity.VOLTAGE))
#
# Fuenf Zeilen, danach ist sauber getrennt. Schreibend geht es nur, wenn beide
# Schloesser bewusst geoeffnet werden - die Voreinstellung ist read_only:
#
#     with WT3000.connect(read_only=False, allow_changes=True) as wt:
#         ...
#
# SCHICHTUNG. Layer 4 darf aus allen tieferen Schichten importieren und wird
# von keiner importiert. Die Stufenskripte bleiben unveraendert bestehen; sie
# sind ab jetzt Beispiele fuer den Weg ohne Fassade, nicht mehr der einzige.
#
# BEWUSST NICHT hier erledigt (jeweils eigener Meilenstein):
#   M1-3  DeviceInfo ist auf das reduziert, was die Verdrahtung der
#         Fachobjekte braucht. Die Bereichstabellen nach Modultyp und
#         InputConfig._elements_of('ALL') (Befund B-12) haengen weiter an
#         Konstanten.
#   M1-4  ensure_protocol_state() - der Sollzustand wird hier geprueft
#         (check_protocol_state), aber nicht hergestellt.
#   M1-5  drain_after_failure() wird weiterhin nirgends aufgerufen (B-04).
# =============================================================================

from __future__ import annotations

import logging
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from pathlib import Path
from types import TracebackType

from .wt3000_common import DEFAULT_ELEMENTS
from .wt3000_core import TmctlTransport, Transport, WTConfig, WTError, WTSession
from .wt3000_input import InputConfig, WiringUnit
from .wt3000_itemspec import (
    ItemSpec,
    apply_item_table,
    build_item_table,
    probe_extra_items,
    probe_item_write_capability,
    restore_item_table,
    save_backup_bundle,
    verify_item_table,
)
from .wt3000_measure import (
    CsvRecorder,
    LoopStatistics,
    NumericHold,
    build_standard_profile,
    run_measurement_loop,
    write_metadata,
)
from .wt3000_numeric import ItemTable, NumericItem, NumericValue, read_numeric_values
from .wt3000_rangeio import RangeAccess, sigma_members_from_units
from .wt3000_ranging import RangeBackup, RangePlan, RangeReport, applied_ranges

__all__ = ["DeviceInfo", "ItemAccess", "MeasureControl", "WT3000"]

_log = logging.getLogger("wt3000.device")


# ---------------------------------------------------------------------------
# Geraetesteckbrief
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DeviceInfo:
    """Was beim Verbinden einmalig ueber das Geraet erhoben wird.

    Bewusst klein gehalten (ROADMAP M1-1): hier steht genau das, was die
    Fassade braucht, um die Fachobjekte zu verdrahten. Der vollstaendige
    Steckbrief - Optionen, Bereichstabellen nach Modultyp, Modellpruefung -
    ist M1-3 und gehoert dann hier hinein, nicht an eine zweite Stelle.
    """

    #: Rohantwort auf '*IDN?'. 'unbekannt', wenn die Abfrage fehlgeschlagen ist.
    identity: str
    #: Hersteller, Modell, Seriennummer, Firmware - aus identity zerlegt.
    manufacturer: str
    model: str
    serial: str
    firmware: str
    #: Verdrahtungsmuster in Elementreihenfolge, z.B. ('V3A3', 'P1W2').
    wiring: tuple[str, ...]
    #: Wiring-Units mit Elementzuordnung.
    wiring_units: tuple[WiringUnit, ...]
    #: Elementnummer -> Modultyp (30, 2 oder 0 = nicht bestueckt).
    modules: dict[int, int] = field(default_factory=dict)
    #: Bestueckte Elemente, aufsteigend.
    elements: tuple[int, ...] = DEFAULT_ELEMENTS
    #: Scope-Abbildung fuer RangeAccess, z.B. {'SIGMA': (1,2,3), 'SIGMB': (4,)}.
    sigma_members: dict[str, tuple[int, ...]] = field(default_factory=dict)
    #: True, wenn die Elementliste angenommen werden musste statt gelesen.
    elements_assumed: bool = False

    # -- Erzeugen -----------------------------------------------------------

    @classmethod
    def read(cls, session: WTSession) -> "DeviceInfo":
        """Steckbrief vom Geraet lesen. Reine Queries, veraendert nichts.

        Die Fehlerbehandlung ist mit Absicht zweigeteilt:

        '*IDN?' ist rein informativ - schlaegt es fehl, wird das protokolliert
        und weitergearbeitet. Verdrahtung und Modultypen dagegen tragen die
        Verdrahtung der Fachobjekte; ohne sie muesste die Fassade die
        Elementzuordnung raten, und geraten wird in diesem Treiber nichts.
        Ein Fehler dort kommt deshalb als WTError heraus.
        """
        identity = "unbekannt"
        try:
            identity = session.query("*IDN?")
        except WTError as error:
            _log.warning("*IDN? fehlgeschlagen: %s - Steckbrief bleibt unvollstaendig", error)

        parts = [p.strip() for p in identity.split(",")]
        while len(parts) < 4:
            parts.append("")

        # Rein lesende Sicht: dieses Objekt benutzt die vorhandenen Parser aus
        # wt3000_input, statt ':INPut:MODUle?' ein viertes Mal selbst zu
        # zerlegen (vgl. Befund B-03).
        reader = InputConfig(session, allow_changes=False)

        wiring = reader.get_wiring()
        units = tuple(reader.get_wiring_units())
        modules = reader.get_modules()

        populated = tuple(sorted(e for e, kind in modules.items() if kind != 0))
        assumed = False
        if not populated:
            _log.warning(
                "Kein bestuecktes Element gemeldet (:INPut:MODUle? -> %s) - "
                "es wird mit %s weitergearbeitet",
                modules,
                DEFAULT_ELEMENTS,
            )
            populated = DEFAULT_ELEMENTS
            assumed = True

        return cls(
            identity=identity,
            manufacturer=parts[0],
            model=parts[1],
            serial=parts[2],
            firmware=parts[3],
            wiring=wiring,
            wiring_units=units,
            modules=modules,
            elements=populated,
            sigma_members=sigma_members_from_units(units),
            elements_assumed=assumed,
        )

    # -- Auswerten ----------------------------------------------------------

    def describe(self) -> list[str]:
        """Steckbrief als Zeilenliste - fuer Protokoll und Konsole."""
        lines = [
            f"Geraet:      {self.model or '?'} ({self.manufacturer or '?'})",
            f"Seriennr.:   {self.serial or '?'}    Firmware: {self.firmware or '?'}",
            f"Verdrahtung: {', '.join(self.wiring) or '?'}",
            f"Elemente:    {self.elements}"
            + ("  (angenommen, nicht gelesen)" if self.elements_assumed else ""),
        ]
        for element in sorted(self.modules):
            kind = self.modules[element]
            label = {30: "30-A-Element", 2: "2-A-Element", 0: "nicht bestueckt"}.get(
                kind, f"Typ {kind}"
            )
            lines.append(f"  Element {element}: {label}")
        for unit in self.wiring_units:
            lines.append(
                f"  Unit {unit.name or '-'}: {unit.pattern} auf Elementen {unit.elements}"
            )
        return lines

    def log_summary(self) -> None:
        """Steckbrief ins Protokoll schreiben."""
        for line in self.describe():
            _log.info("%s", line)

    def has_element(self, element: int) -> bool:
        """True, wenn dieses Element bestueckt ist."""
        return element in self.elements


# ---------------------------------------------------------------------------
# Item-Tabelle als Objekt
# ---------------------------------------------------------------------------


class ItemAccess:
    """Bindet die Ablauffunktionen aus wt3000_itemspec an eine Sitzung.

    Die Funktionen dort sind bewusst frei und ohne Zustand geblieben - sie
    nehmen alle eine 'session' als ersten Parameter. Diese Klasse ist die
    Stelle, an der die Sitzung genau einmal eingesetzt wird, damit der
    Aufrufer sie nicht durch jeden Aufruf durchreichen muss.
    """

    def __init__(self, session: WTSession, allow_changes: bool = False) -> None:
        self._session = session
        self._allow_changes = allow_changes

    @property
    def allow_changes(self) -> bool:
        """True, wenn dieses Objekt schreiben darf."""
        return self._allow_changes

    def _require_writable(self) -> None:
        if not self._allow_changes:
            raise WTError(
                "Schreibzugriff auf die Item-Tabelle abgelehnt: WT3000 wurde ohne "
                "allow_changes=True geoeffnet."
            )

    # -- Lesen --------------------------------------------------------------

    def read(self) -> ItemTable:
        """Aktuelle Item-Tabelle vom Geraet lesen."""
        return ItemTable.read_from_device(self._session)

    @staticmethod
    def standard_profile() -> tuple[ItemSpec, ...]:
        """Das Messprofil dieses Aufbaus (aus wt3000_measure)."""
        return build_standard_profile()

    @staticmethod
    def build(specs: Sequence[ItemSpec]) -> ItemTable:
        """Aus einer Spec-Liste die Zieltabelle erzeugen."""
        return build_item_table(list(specs))

    def verify(self, target: ItemTable) -> list[str]:
        """Ist-Tabelle mit der Anforderung vergleichen. Leer = in Ordnung."""
        return verify_item_table(self._session, target)

    def capture_tail(self, backup: ItemTable, target: ItemTable) -> list[NumericItem]:
        """Items jenseits von NUMber sichern, die die Zieltabelle ueberschreibt."""
        return probe_extra_items(
            self._session,
            first_index=len(backup.items) + 1,
            last_index=len(target.items),
        )

    # -- Schreiben ----------------------------------------------------------

    def apply(self, target: ItemTable, backup: ItemTable | None = None) -> None:
        """Zieltabelle schreiben und verifizieren.

        Vor dem Schreiben der ganzen Tabelle geht genau EIN Item als Probe
        hinaus. Faellt die durch, ist ein einziges Item veraendert statt
        aller - das ist der Grund fuer den Umweg.
        """
        self._require_writable()
        probe_item_write_capability(self._session, target, backup or self.read())
        apply_item_table(self._session, target)
        problems = self.verify(target)
        if problems:
            for problem in problems:
                _log.error("Verifikation: %s", problem)
            raise WTError(f"{len(problems)} Abweichung(en) beim Verifizieren der Item-Tabelle")

    def restore(
        self, backup: ItemTable, tail: Sequence[NumericItem] = (), force: bool = False
    ) -> int:
        """Gesicherten Zustand wiederherstellen. Rueckgabe: Anzahl Kommandos."""
        self._require_writable()
        return restore_item_table(self._session, backup, list(tail), force=force)

    @contextmanager
    def applied(
        self,
        specs: Sequence[ItemSpec] | ItemTable,
        backup_file: Path | None = None,
        force_restore: bool = False,
    ) -> Iterator[ItemTable]:
        """Tabelle setzen, Block ausfuehren, Ausgangszustand garantiert zurueck.

        Das Gegenstueck zu 'applied_ranges()' fuer die Item-Tabelle: derselbe
        try/finally-Ablauf, den Stufe 3 und Stufe 4 heute jeweils von Hand
        nachbauen - sichern, Tail sichern, Schreibprobe, anwenden,
        verifizieren, Nutzblock, wiederherstellen.

        Die Wiederherstellung laeuft im finally und damit auch bei Strg+C.

        UEBERARBEITET (P-2, siehe PLAN_BEFUNDE_2026-08-19.md): Was 'garantiert'
        hier bedeutet, ist jetzt auch im Fehlerfall wahr. Wer diesen Block ohne
        Ausnahme verlaesst, darf sich darauf verlassen, dass die Item-Tabelle
        wieder im Ausgangszustand steht. Misslingt die Wiederherstellung, kommt
        eine WTError heraus - siehe die Begruendung im finally.
        """
        self._require_writable()

        target = specs if isinstance(specs, ItemTable) else self.build(specs)
        backup = self.read()
        tail = self.capture_tail(backup, target)
        if backup_file is not None:
            save_backup_bundle(backup_file, backup, tail)

        try:
            self.apply(target, backup)
            yield target
        finally:
            # UEBERARBEITET (P-2, siehe PLAN_BEFUNDE_2026-08-19.md): Der Fehler
            # wurde hier bisher nur protokolliert und dann verschluckt. Ein
            # Aufrufer konnte den Kontextmanager also normal verlassen, obwohl
            # die Item-Tabelle nicht wiederhergestellt war - genau das, was der
            # Docstring ausschliesst. 'applied_ranges()' in wt3000_ranging.py
            # macht es an derselben Stelle seit jeher richtig und loest erneut
            # aus; die beiden Ablaeufe verhalten sich jetzt gleich.
            #
            # Zur Fehlerverkettung: eine im finally ausgeloeste Ausnahme traegt
            # eine bereits unterwegs befindliche automatisch als '__context__'
            # mit. Schlaegt also erst der Nutzblock fehl und dann die
            # Wiederherstellung, zeigt der Traceback beide - ohne Zutun und
            # ohne Abhaengigkeit von Python 3.11.
            try:
                self.restore(backup, tail, force=force_restore)

                # Gegenprobe. 'applied_ranges()' protokolliert das Ergebnis
                # nur, weil es einen RangeReport herausgibt, in dem der
                # Aufrufer danach nachsehen kann. Hier gibt es kein solches
                # Objekt - dieser Kontextmanager liefert die ItemTable. Eine
                # bloss protokollierte Abweichung waere deshalb wieder
                # unbemerkbar, also dieselbe Falle eine Ebene tiefer. Sie wird
                # gemeldet.
                problems = self.verify(backup)
                if problems:
                    for problem in problems:
                        _log.error("Restore-Kontrolle: %s", problem)
                    raise WTError(
                        f"{len(problems)} Abweichung(en) nach der Wiederherstellung "
                        "der Item-Tabelle"
                    )
                _log.info("Restore-Kontrolle: Ausgangszustand exakt wiederhergestellt")

            except WTError as error:
                location = backup_file if backup_file is not None else "nicht gesichert"
                _log.error(
                    "Wiederherstellung der Item-Tabelle fehlgeschlagen: %s - Backup: %s",
                    error,
                    location,
                )
                raise


# ---------------------------------------------------------------------------
# Messung
# ---------------------------------------------------------------------------


class MeasureControl:
    """Messwerte lesen und aufzeichnen.

    ZUM UMFANG: die Messschleife ist weiterhin blockierend und bricht nur ueber
    Strg+C oder ein gesetztes Limit ab. Sie hier anzubinden macht sie
    erreichbar, nicht steuerbar - das ist M3-1 (Aufzeichnung als Objekt mit
    start()/stop()) und ausdruecklich nicht Teil von M1-1.
    """

    def __init__(self, session: WTSession, items: ItemAccess, read_only: bool = True) -> None:
        self._session = session
        self._items = items
        self._read_only = read_only

    # -- Einzelwerte --------------------------------------------------------

    def read_values(self, table: ItemTable | None = None) -> list[NumericValue]:
        """Einen Datensatz als Werteliste lesen (Reihenfolge = Item-Reihenfolge)."""
        expected = len(table.items) if table is not None else None
        return read_numeric_values(self._session, expected_count=expected)

    def read_mapped(self, table: ItemTable | None = None) -> dict[str, NumericValue]:
        """Einen Datensatz auf sprechende Namen abgebildet lesen."""
        used = table if table is not None else self._items.read()
        return used.map_values(self.read_values(used))

    def hold(self, enabled: bool = True) -> NumericHold:
        """Context Manager fuer ':NUMeric:HOLD'.

        In einer Nur-Lesen-Sitzung wird HOLD abgeschaltet statt einen Fehler
        auszuloesen: HOLD ist ein Set-Kommando, und read_only heisst, dass
        nichts gesendet wird. Die Werte sind dann ungefroren - der Zeitstempel
        wird unschaerfer, die Messung bleibt gueltig.
        """
        if enabled and self._read_only:
            _log.warning("Nur-Lesen-Sitzung: HOLD wird nicht benutzt (Set-Kommando)")
            enabled = False
        return NumericHold(self._session, enabled=enabled)

    # -- Aufzeichnung -------------------------------------------------------

    def record(
        self,
        csv_path: Path,
        table: ItemTable,
        interval_s: float = 1.0,
        max_samples: int | None = None,
        max_duration_s: float | None = None,
        use_hold: bool = True,
        record_condition: bool = True,
        log_every: int = 0,
        delimiter: str = ",",
        metadata_path: Path | None = None,
        parameters: dict | None = None,
    ) -> LoopStatistics:
        """Messschleife in eine CSV schreiben.

        Blockiert bis zum Erreichen eines Limits oder bis Strg+C. Ohne Limit
        laeuft sie unbegrenzt weiter - das ist Absicht, aber beim Einbau in
        fremden Code selten gewollt.
        """
        if use_hold and self._read_only:
            _log.warning("Nur-Lesen-Sitzung: Messschleife laeuft ohne HOLD")
            use_hold = False

        if metadata_path is not None:
            write_metadata(
                metadata_path,
                self._session,
                table,
                parameters={
                    "sample_interval_s": interval_s,
                    "max_samples": max_samples,
                    "max_duration_s": max_duration_s,
                    "use_hold": use_hold,
                    "record_condition": record_condition,
                    "csv_file": csv_path.name,
                    **(parameters or {}),
                },
            )

        column_names = [item.key for item in table.items]
        with CsvRecorder(csv_path, column_names, delimiter=delimiter) as recorder:
            return run_measurement_loop(
                session=self._session,
                table=table,
                recorder=recorder,
                interval_s=interval_s,
                max_samples=max_samples,
                max_duration_s=max_duration_s,
                use_hold=use_hold,
                record_condition=record_condition,
                log_every=log_every,
            )


# ---------------------------------------------------------------------------
# Die Fassade
# ---------------------------------------------------------------------------


class WT3000:
    """Ein verbundenes WT3000 - der einzige Einstiegspunkt des Treibers.

    Erzeugt wird ausschliesslich ueber die Klassenmethoden:

        WT3000.connect(ip="192.168.10.20")          # rein lesend
        WT3000.from_config(WTConfig(ip="..."), read_only=False, allow_changes=True)
        WT3000.from_transport(FakeTransport({...}))  # geraetefrei, fuer Tests

    ZWEI SCHLOESSER, unveraendert aus den Fachmodulen uebernommen:

        read_only=True      die Sitzung lehnt jedes Nicht-Query-Kommando ab
        allow_changes=False InputConfig/RangeAccess/ItemAccess lehnen jeden
                            Schreibaufruf schon vor dem Senden ab

    Beide stehen in der Voreinstellung zu. Wer messen und nichts veraendern
    will - der Normalfall - braucht keinen der beiden Schalter anzufassen.
    Ausserdem bleiben die Gruppen aus 'DEFAULT_PROTECTED' auch bei
    allow_changes=True gesperrt und muessen einzeln ueber
    'wt.input.unlocked(...)' freigegeben werden.
    """

    def __init__(
        self,
        transport: Transport,
        config: WTConfig | None = None,
        read_only: bool = True,
        allow_changes: bool = False,
        owns_transport: bool = True,
    ) -> None:
        if allow_changes and read_only:
            raise WTError(
                "allow_changes=True zusammen mit read_only=True ist widerspruechlich: "
                "die Sitzung wuerde jedes Set-Kommando ohnehin ablehnen. "
                "Fuer Schreibzugriff read_only=False setzen."
            )

        self._config = config if config is not None else WTConfig()
        self._transport = transport
        self._owns_transport = owns_transport
        self._read_only = read_only
        self._allow_changes = allow_changes
        self._closed = False

        self._session = WTSession(transport, self._config, read_only=read_only)

        # Fernsteuerung nur einschalten, wenn ueberhaupt geschrieben werden
        # darf: ':COMMunicate:REMote ON' ist selbst ein Set-Kommando und
        # scheitert in einer Nur-Lesen-Sitzung an der eigenen Sperre.
        if self._config.use_remote and not read_only:
            self._session.enable_remote()
        elif self._config.use_remote:
            _log.info("Nur-Lesen-Sitzung: ':COMMunicate:REMote ON' wird nicht gesendet")

        # UEBERARBEITET (P-1, siehe PLAN_BEFUNDE_2026-08-19.md): ab hier laeuft
        # der Rest des Konstruktors unter Aufraeumschutz.
        #
        # Vorher stand DeviceInfo.read() ungeschuetzt hinter enable_remote().
        # Scheiterte eine der dortigen Pflichtabfragen - ':INPut:WIRing?' oder
        # ':INPut:MODUle?' -, verliess die Ausnahme den Konstruktor, ohne dass
        # ':COMMunicate:REMote OFF' je gesendet wurde: das Bedienfeld blieb
        # gesperrt zurueck. close() konnte das nicht auffangen, weil bei einem
        # gescheiterten Konstruktor gar kein Objekt entsteht, an dem close()
        # aufrufbar waere.
        #
        # Die Reparatur sitzt bewusst HIER und nicht in from_config(): nur so
        # sind alle drei Wege abgedeckt - from_config(), from_transport() und
        # die direkte Konstruktion. from_transport() raeumte bisher gar nicht
        # auf, weil es den Transport nicht besitzt.
        try:
            # ROADMAP M1-1: die bisher manuelle Verdrahtung
            # sigma_members_from_units(cfg.get_wiring_units()) passiert hier -
            # einmalig, beim Verbinden, fuer alle Fachobjekte gemeinsam.
            self._device = DeviceInfo.read(self._session)
            self._device.log_summary()
        except BaseException:
            # Auch bei Strg+C waehrend des Verbindungsaufbaus: das Bedienfeld
            # gehoert freigegeben.
            self._release_remote_after_failure()
            raise

        self._input: InputConfig | None = None
        self._ranges: RangeAccess | None = None
        self._items: ItemAccess | None = None
        self._measure: MeasureControl | None = None

    # -- Erzeugen -----------------------------------------------------------

    @classmethod
    def connect(
        cls,
        ip: str | None = None,
        read_only: bool = True,
        allow_changes: bool = False,
        dll_path: str | None = None,
        timeout_ms: int | None = None,
        use_remote: bool | None = None,
    ) -> "WT3000":
        """Ueber die TMCTL-DLL verbinden. Nicht angegebene Werte aus WTConfig.

        Der haeufigste Aufruf ueberhaupt:

            with WT3000.connect() as wt:
                ...
        """
        overrides: dict[str, object] = {}
        if ip is not None:
            overrides["ip"] = ip
        if dll_path is not None:
            overrides["dll_path"] = dll_path
        if timeout_ms is not None:
            overrides["timeout_ms"] = timeout_ms
        if use_remote is not None:
            overrides["use_remote"] = use_remote

        config = replace(WTConfig(), **overrides) if overrides else WTConfig()
        return cls.from_config(config, read_only=read_only, allow_changes=allow_changes)

    @classmethod
    def from_config(
        cls, config: WTConfig, read_only: bool = True, allow_changes: bool = False
    ) -> "WT3000":
        """Mit einer fertigen WTConfig verbinden. Die Fassade schliesst den Transport."""
        transport = TmctlTransport(config)
        try:
            return cls(
                transport,
                config,
                read_only=read_only,
                allow_changes=allow_changes,
                owns_transport=True,
            )
        except BaseException:
            # Der Transport steht schon, die Sitzung ist aber nicht zustande
            # gekommen (z.B. weil ':INPut:WIRing?' nicht antwortet). Ohne
            # dieses except bliebe die Verbindung offen.
            #
            # UEBERARBEITET (P-1, siehe PLAN_BEFUNDE_2026-08-19.md): Der
            # Kommentar behauptete hier zusaetzlich, dieser Block verhindere
            # auch, dass das Geraet in Fernsteuerung stehen bleibt. Das hat er
            # nie getan - ein 'REMote OFF' kam an dieser Stelle nicht vor, und
            # nach transport.close() waere es ohnehin ins Leere gegangen.
            # Zustaendig ist jetzt der Konstruktor selbst; er schaltet die
            # Fernsteuerung ab, BEVOR die Ausnahme hier ankommt. Dieser Block
            # kuemmert sich nur noch um den Transport, den nur dieser Weg
            # besitzt.
            transport.close()
            raise

    @classmethod
    def from_transport(
        cls,
        transport: Transport,
        config: WTConfig | None = None,
        read_only: bool = True,
        allow_changes: bool = False,
        owns_transport: bool = False,
    ) -> "WT3000":
        """Auf einem bereits bestehenden Transport aufsetzen.

        Damit laeuft die Fassade auch auf 'FakeTransport' (M1-2) und spaeter
        auf einem Socket- oder VISA-Transport. Voreinstellung ist hier
        owns_transport=False: wer den Transport mitbringt, schliesst ihn auch.
        """
        return cls(
            transport,
            config,
            read_only=read_only,
            allow_changes=allow_changes,
            owns_transport=owns_transport,
        )

    # -- Eigenschaften ------------------------------------------------------

    @property
    def session(self) -> WTSession:
        """Die Protokollschicht. Notausgang fuer Kommandos ohne eigene Methode."""
        return self._session

    @property
    def config(self) -> WTConfig:
        """Die benutzten Verbindungsparameter."""
        return self._config

    @property
    def device(self) -> DeviceInfo:
        """Steckbrief, einmalig beim Verbinden erhoben."""
        return self._device

    @property
    def read_only(self) -> bool:
        """True, wenn die Sitzung kein Set-Kommando durchlaesst."""
        return self._read_only

    @property
    def allow_changes(self) -> bool:
        """True, wenn die Fachobjekte schreiben duerfen."""
        return self._allow_changes

    @property
    def input(self) -> InputConfig:
        """Eingangs- und Messkonfiguration (':INPut'), fertig verdrahtet."""
        self._require_open()
        if self._input is None:
            self._input = InputConfig(self._session, allow_changes=self._allow_changes)
        return self._input

    @property
    def ranges(self) -> RangeAccess:
        """Messbereiche und Autorange - mit Elementliste und Wiring-Units.

        Genau die Verdrahtung, die bisher jeder Aufrufer selbst herstellen
        musste und in stage5b schlicht fehlt: ohne 'sigma_members' laeuft dort
        jeder SIGMA-Scope in einen Fehler.
        """
        self._require_open()
        if self._ranges is None:
            self._ranges = RangeAccess(
                self._session,
                allow_changes=self._allow_changes,
                elements=self._device.elements,
                sigma_members=self._device.sigma_members,
            )
        return self._ranges

    @property
    def items(self) -> ItemAccess:
        """Item-Tabelle der NUMeric-Gruppe."""
        self._require_open()
        if self._items is None:
            self._items = ItemAccess(self._session, allow_changes=self._allow_changes)
        return self._items

    @property
    def measure(self) -> MeasureControl:
        """Messwerte lesen und aufzeichnen."""
        self._require_open()
        if self._measure is None:
            self._measure = MeasureControl(self._session, self.items, read_only=self._read_only)
        return self._measure

    # -- Ablaeufe -----------------------------------------------------------

    def check_protocol_state(self) -> None:
        """Voraussetzungen der Binaerauswertung pruefen. Veraendert nichts.

        ':COMMunicate:HEADer 0' und ':NUMeric:FORMat FLOat' sind keine
        Feinheiten: mit Headern scheitert das Parsen der Item-Tabelle, im
        ASCii-Format kommt kein Blockheader, den query_block() zerlegen kann.

        Diese Methode ist der designierte Ort fuer Befund B-14 (dieselbe
        Pruefung liegt heute in stage2/3/4 in drei leicht abweichenden
        Fassungen) und die Grundlage fuer M1-4, das den Sollzustand dann nicht
        nur prueft, sondern herstellt und beim Verlassen zuruecknimmt.
        """
        header = self._session.query(":COMMunicate:HEADer?")
        if header.strip() != "0":
            raise WTError(
                f":COMMunicate:HEADer ist {header!r}, erwartet '0'. "
                "Mit Headern schlaegt das Parsen der Item-Tabelle fehl."
            )

        fmt = self._session.query(":NUMeric:FORMat?")
        if not fmt.upper().startswith("FLO"):
            raise WTError(
                f":NUMeric:FORMat ist {fmt!r}, erwartet 'FLO'. "
                "Messwerte werden ausschliesslich als Binaerblock gelesen."
            )

        self.log_condition()

    def log_condition(self) -> int:
        """':STATus:CONDition?' auswerten und Auffaelligkeiten protokollieren."""
        bits = int(self._session.query(":STATus:CONDition?"))
        if bits & (1 << 4):
            _log.warning("Condition Bit 4 (FOV): Frequenzmessung im Fehler")
        if bits & (1 << 7):
            _log.warning("Condition Bit 7 (PLLE): kein Signal an der PLL-Quelle")
        if bits & 0x0F00:
            _log.warning("Condition: Overrange an mindestens einem Element")
        return bits

    def range_backup(self) -> RangeBackup:
        """Ist-Zustand aller Bereiche sichern."""
        return RangeBackup.capture(self.ranges)

    @contextmanager
    def applied_ranges(
        self,
        plan: RangePlan,
        backup_file: Path | None = None,
        allow_snapping: bool = False,
        force_restore: bool = False,
    ) -> Iterator[RangeReport]:
        """Bereiche nach Plan setzen, Block ausfuehren, Ausgangszustand zurueck.

        Duenne Weiterleitung an 'wt3000_ranging.applied_ranges()' mit dem
        bereits verdrahteten RangeAccess - der Ablauf selbst bleibt dort, wo
        er getestet ist.
        """
        with applied_ranges(
            self.ranges,
            plan,
            backup_file=backup_file,
            allow_snapping=allow_snapping,
            force_restore=force_restore,
        ) as report:
            yield report

    # -- Beenden ------------------------------------------------------------

    def _require_open(self) -> None:
        if self._closed:
            raise WTError("Diese WT3000-Sitzung ist bereits geschlossen")

    # UEBERARBEITET (P-1, siehe PLAN_BEFUNDE_2026-08-19.md): Gegenstueck zu
    # close() fuer den Fall, dass der Konstruktor nicht durchlaeuft.
    def _release_remote_after_failure(self) -> None:
        """Fernsteuerung zuruecknehmen, wenn der Verbindungsaufbau scheitert.

        Raeumt ausschliesslich das ab, was der Konstruktor selbst angerichtet
        hat - also ':COMMunicate:REMote ON'. Der Transport wird hier bewusst
        NICHT geschlossen: wer ihn erzeugt hat, schliesst ihn auch. Fuer
        from_config() ist das die Fassade selbst, fuer from_transport() der
        Aufrufer.

        disable_remote() ist fuer diesen Einsatz bereits richtig gebaut: es
        prueft '_remote_active', sendet also nichts, wenn nie eingeschaltet
        wurde, und faengt WTError selbst ab.
        """
        try:
            self._session.disable_remote()
        except Exception as error:  # bewusst breit
            # Ein Fehler beim Aufraeumen darf die eigentliche Ursache niemals
            # verdecken - deshalb nur protokollieren, nicht ausloesen.
            _log.error(
                "REMote OFF nach fehlgeschlagenem Verbindungsaufbau misslungen: %s - "
                "Bedienfeld ggf. am Geraet ueber die LOCAL-Taste freigeben",
                error,
            )

    def close(self) -> None:
        """Sauber trennen. Mehrfachaufruf ist unschaedlich.

        Reihenfolge und Fehlerbehandlung sind hier das Wesentliche: jeder
        Schritt laeuft in seinem eigenen try, damit ein misslungener Schritt
        die folgenden nicht ueberspringt. Ein haengengebliebenes HOLD ist der
        unangenehmste Rest, den eine abgebrochene Sitzung hinterlassen kann -
        das Geraet liefert dann in der naechsten Sitzung eingefrorene Werte,
        waehrend die Anzeige weiterlaeuft.
        """
        if self._closed:
            return
        self._closed = True

        if not self._read_only:
            try:
                self._session.write(":NUMeric:HOLD OFF")
                _log.info("HOLD abgeschaltet")
            except WTError as error:
                _log.error("HOLD OFF fehlgeschlagen: %s - Geraet manuell pruefen", error)

        try:
            self._session.disable_remote()
        except WTError as error:  # pragma: no cover - disable_remote faengt selbst
            _log.error("REMote OFF fehlgeschlagen: %s", error)

        if self._owns_transport:
            try:
                self._transport.close()
            except Exception as error:  # bewusst breit: der Transport ist austauschbar
                _log.error("Transport konnte nicht geschlossen werden: %s", error)

    def __enter__(self) -> "WT3000":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()
