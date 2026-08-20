# =============================================================================
# Datei: tests/test_device_facade.py
# NEU (ROADMAP M1-1): die Fassade 'WT3000' geraetefrei pruefen.
#
# Diese Datei ist der Beleg fuer das Abnahmekriterium aus M1-1 - "ein Anwender
# baut mit fuenf Zeilen eine Verbindung auf, liest die Konfiguration und
# trennt sauber wieder". Moeglich ist das erst seit M1-2: die Fassade wird
# hier auf 'FakeTransport' gesetzt, nicht auf 'FakeSession'. Damit laufen
# WTSession, Blockparser, Fehlerqueue und Item-Tabelle im Test mit - also
# genau die Schichten, die eine Fassade zusammenbindet.
#
# 'ItemTableTransport' unten ist ein minimales Geraetemodell: es uebernimmt
# geschriebene ITEM<n>- und NUMber-Kommandos und beantwortet die Abfragen
# daraus. Ohne diese Rueckkopplung koennte man das Schreiben pruefen, aber
# nicht das Verifizieren und schon gar nicht die Wiederherstellung.
# =============================================================================

from __future__ import annotations


import pytest
# UEBERARBEITET (Schritt 7): 'base_responses' und 'ItemTableTransport' liegen
# jetzt in conftest.py - die Stufenskripte brauchen dasselbe Geraetemodell.
from conftest import ItemTableTransport, base_responses

from wt3000_scpi import WT3000, WTConfig, WTError
from wt3000_scpi import wt3000_device  # NEU (P-1): fuer monkeypatch auf TmctlTransport
from wt3000_scpi.wt3000_core import ReadOnlyViolation, TmctlError  # TmctlError: NEU (P-2)
from wt3000_scpi.wt3000_input import ConfigLocked
from wt3000_scpi.wt3000_itemspec import ItemSpec
from wt3000_scpi.wt3000_numeric import ValueStatus
from wt3000_scpi.wt3000_transport import FakeTransport

def open_facade(transport: FakeTransport, **kwargs) -> WT3000:
    """Fassade auf einem Fake-Transport, ohne Fernsteuerung."""
    kwargs.setdefault("read_only", True)
    return WT3000.from_transport(transport, WTConfig(use_remote=False), **kwargs)


# ---------------------------------------------------------------------------
# Verbinden und Steckbrief
# ---------------------------------------------------------------------------


def test_steckbrief_wird_beim_verbinden_erhoben():
    with open_facade(FakeTransport(base_responses())) as wt:
        info = wt.device
        assert info.manufacturer == "YOKOGAWA"
        assert info.model == "WT3000"
        assert info.serial == "C1B234567"
        assert info.firmware == "F2.11"
        assert info.wiring == ("V3A3", "P1W2")
        assert info.elements == (1, 2, 3, 4)
        assert info.elements_assumed is False


def test_unbestueckte_elemente_fallen_aus_der_elementliste():
    """Halber Schritt Richtung M1-3: die Elementliste wird gelesen, nicht gesetzt."""
    responses = base_responses(wiring="V3A3,NONE", modules="30,30,30,0")
    with open_facade(FakeTransport(responses)) as wt:
        assert wt.device.elements == (1, 2, 3)
        assert wt.device.has_element(4) is False
        assert wt.ranges.expand_scope("ALL") == (1, 2, 3)


def test_wiring_units_sind_ohne_zutun_verdrahtet():
    """Der eigentliche Gewinn von M1-1.

    Ohne Fassade muss der Aufrufer sigma_members_from_units(...) selbst
    einsetzen - in stage5b fehlt genau das, dort laeuft jeder SIGMA-Scope in
    einen Fehler.
    """
    with open_facade(FakeTransport(base_responses())) as wt:
        assert wt.ranges.expand_scope("SIGMA") == (1, 2, 3)
        assert wt.ranges.expand_scope("SIGMB") == (4,)
        # Und weiterhin kein Praefixmatching: SIGM != SIGMB.
        assert wt.ranges.expand_scope("SIGM") == (1, 2, 3)


def test_steckbrief_ohne_idn_bricht_nicht_ab():
    """'*IDN?' ist informativ - Verdrahtung und Modultypen sind es nicht."""
    responses = base_responses()
    del responses["*IDN"]
    transport = FakeTransport(responses, fail_commands=["*IDN?"])
    with open_facade(transport) as wt:
        assert wt.device.identity == "unbekannt"
        assert wt.device.elements == (1, 2, 3, 4)


def test_fehlende_verdrahtung_ist_ein_fehler():
    responses = base_responses()
    del responses[":INPUT:WIRING"]
    with pytest.raises(KeyError):
        open_facade(FakeTransport(responses))


# ---------------------------------------------------------------------------
# Die beiden Schloesser
# ---------------------------------------------------------------------------


def test_voreinstellung_ist_nur_lesen():
    with open_facade(ItemTableTransport(three_items(), number=3)) as wt:
        assert wt.read_only is True
        assert wt.allow_changes is False

        with pytest.raises(ConfigLocked):
            wt.input.set_crest_factor(6)
        with pytest.raises(WTError):
            wt.items.apply(wt.items.read())
        with pytest.raises(ReadOnlyViolation):
            wt.session.write(":INPut:CFACtor 6")


def test_allow_changes_ohne_schreibsitzung_wird_abgelehnt():
    """Ein Widerspruch, der sonst erst beim ersten Set-Kommando auffiele."""
    with pytest.raises(WTError, match="widerspruechlich"):
        open_facade(FakeTransport(base_responses()), read_only=True, allow_changes=True)


def test_nur_lesen_sendet_kein_remote():
    transport = FakeTransport(base_responses())
    with WT3000.from_transport(transport, WTConfig(use_remote=True)) as wt:
        assert wt.read_only is True
    assert ":COMMunicate:REMote ON" not in transport.written


def test_schreibsitzung_schaltet_remote_ein_und_beim_schliessen_ab():
    transport = FakeTransport(base_responses())
    with WT3000.from_transport(
        transport, WTConfig(use_remote=True), read_only=False, allow_changes=True
    ) as wt:
        assert wt.allow_changes is True
        assert ":COMMunicate:REMote ON" in transport.written

    assert ":NUMeric:HOLD OFF" in transport.written
    assert ":COMMunicate:REMote OFF" in transport.written
    assert transport.written.index(":NUMeric:HOLD OFF") < transport.written.index(
        ":COMMunicate:REMote OFF"
    )


# ---------------------------------------------------------------------------
# NEU (P-1, siehe PLAN_BEFUNDE_2026-08-19.md): Fernsteuerung beim GESCHEITERTEN
# Verbindungsaufbau.
#
# Der Fall, den close() strukturell nicht abdecken kann: scheitert der
# Konstruktor, entsteht kein WT3000-Objekt, an dem sich close() aufrufen liesse.
# ':COMMunicate:REMote ON' ist da aber laengst gesendet - das Bedienfeld bliebe
# gesperrt zurueck. Geprueft wird deshalb fuer JEDEN Erzeugungsweg einzeln.
#
# 'fail_commands' laesst ':INPut:WIRing?' scheitern. Das ist eine der beiden
# Pflichtabfragen aus DeviceInfo.read() - genau der Fall, den der Kommentar in
# from_config() beschreibt.
# ---------------------------------------------------------------------------

WIRING_QUERY = ":INPut:WIRing?"


def test_gescheiterter_verbindungsaufbau_gibt_das_bedienfeld_frei():
    """P-1: REMote ON ohne passendes OFF waere ein gesperrtes Bedienfeld."""
    transport = FakeTransport(base_responses(), fail_commands={WIRING_QUERY})

    with pytest.raises(WTError):
        WT3000.from_transport(
            transport, WTConfig(use_remote=True), read_only=False, allow_changes=True
        )

    assert ":COMMunicate:REMote ON" in transport.written
    assert ":COMMunicate:REMote OFF" in transport.written
    assert transport.written.index(":COMMunicate:REMote ON") < transport.written.index(
        ":COMMunicate:REMote OFF"
    )


def test_gescheiterter_verbindungsaufbau_meldet_weiter_die_urspruengliche_ursache():
    """Das Aufraeumen darf die Ursache nicht verdecken."""
    transport = FakeTransport(base_responses(), fail_commands={WIRING_QUERY})

    with pytest.raises(WTError) as fehler:
        WT3000.from_transport(
            transport, WTConfig(use_remote=True), read_only=False, allow_changes=True
        )

    assert "WIRing" in str(fehler.value)


def test_gescheiterter_verbindungsaufbau_ohne_remote_sendet_kein_off():
    """Ohne vorheriges ON gibt es nichts zurueckzunehmen.

    Haengt an der Pruefung von '_remote_active' in disable_remote() - ein
    blindes OFF waere in einer Nur-Lesen-Sitzung ausserdem ein Set-Kommando
    und wuerde an der eigenen Sperre scheitern.
    """
    transport = FakeTransport(base_responses(), fail_commands={WIRING_QUERY})

    with pytest.raises(WTError):
        WT3000.from_transport(transport, WTConfig(use_remote=True), read_only=True)

    assert ":COMMunicate:REMote ON" not in transport.written
    assert ":COMMunicate:REMote OFF" not in transport.written


def test_from_config_gibt_bedienfeld_frei_und_schliesst_den_transport(monkeypatch):
    """Zweiter Erzeugungsweg: hier gehoert der Transport der Fassade.

    Reihenfolge ist entscheidend - nach transport.close() ginge ein
    'REMote OFF' ins Leere.
    """
    transport = FakeTransport(base_responses(), fail_commands={WIRING_QUERY})
    monkeypatch.setattr(wt3000_device, "TmctlTransport", lambda _config: transport)

    with pytest.raises(WTError):
        WT3000.from_config(
            WTConfig(use_remote=True), read_only=False, allow_changes=True
        )

    assert ":COMMunicate:REMote OFF" in transport.written
    assert transport.closed is True


def test_strg_c_waehrend_des_verbindungsaufbaus_gibt_das_bedienfeld_frei():
    """KeyboardInterrupt ist kein WTError - deshalb faengt der Konstruktor
    BaseException. Ein abgebrochener Verbindungsaufbau darf das Geraet nicht
    gesperrt zuruecklassen."""

    def abbruch(_command: str) -> str:
        raise KeyboardInterrupt

    responses = base_responses()
    responses[":INPUT:WIRING"] = abbruch
    transport = FakeTransport(responses)

    with pytest.raises(KeyboardInterrupt):
        WT3000.from_transport(
            transport, WTConfig(use_remote=True), read_only=False, allow_changes=True
        )

    assert ":COMMunicate:REMote OFF" in transport.written


def test_erfolgreicher_aufbau_sendet_kein_vorzeitiges_off():
    """Gegenprobe: der Aufraeumpfad darf im Regelfall nicht anspringen."""
    transport = FakeTransport(base_responses())
    wt = WT3000.from_transport(
        transport, WTConfig(use_remote=True), read_only=False, allow_changes=True
    )
    try:
        assert ":COMMunicate:REMote OFF" not in transport.written
    finally:
        wt.close()
    assert ":COMMunicate:REMote OFF" in transport.written


# ---------------------------------------------------------------------------
# Beenden
# ---------------------------------------------------------------------------


def test_context_manager_schliesst_auch_bei_einem_fehler_im_block():
    transport = FakeTransport(base_responses())
    with pytest.raises(ZeroDivisionError):
        with WT3000.from_transport(
            transport, WTConfig(use_remote=True), read_only=False, allow_changes=True
        ):
            raise ZeroDivisionError("Fehler im Nutzblock")
    assert ":NUMeric:HOLD OFF" in transport.written
    assert ":COMMunicate:REMote OFF" in transport.written


def test_close_ist_mehrfach_aufrufbar_und_sperrt_danach():
    wt = open_facade(FakeTransport(base_responses()))
    wt.close()
    wt.close()
    with pytest.raises(WTError, match="geschlossen"):
        _ = wt.input


def test_mitgebrachter_transport_wird_nicht_geschlossen():
    """Wer den Transport mitbringt, schliesst ihn auch - Voreinstellung von from_transport."""
    transport = FakeTransport(base_responses())
    with open_facade(transport):
        pass
    assert transport.closed is False


def test_eigener_transport_wird_geschlossen():
    transport = FakeTransport(base_responses())
    with WT3000.from_transport(transport, WTConfig(use_remote=False), owns_transport=True):
        pass
    assert transport.closed is True


# ---------------------------------------------------------------------------
# Sollzustand der Kommunikation
# ---------------------------------------------------------------------------


def test_protokollzustand_in_ordnung():
    with open_facade(FakeTransport(base_responses())) as wt:
        wt.check_protocol_state()


@pytest.mark.parametrize(
    ("kwargs", "fragment"),
    [
        ({"header": "1"}, "HEADer"),
        ({"numeric_format": "ASCii"}, "FORMat"),
    ],
)
def test_protokollzustand_faellt_auf(kwargs, fragment):
    with open_facade(FakeTransport(base_responses(**kwargs))) as wt:
        with pytest.raises(WTError, match=fragment):
            wt.check_protocol_state()


def test_condition_bits_werden_gemeldet(caplog):
    responses = base_responses()
    responses[":STATUS:CONDITION"] = str((1 << 4) | (1 << 7))
    with open_facade(FakeTransport(responses)) as wt:
        with caplog.at_level("WARNING"):
            assert wt.log_condition() == 0x90
    assert "FOV" in caplog.text
    assert "PLLE" in caplog.text


# ---------------------------------------------------------------------------
# Item-Tabelle und Messwerte
# ---------------------------------------------------------------------------


def three_items() -> dict[int, str]:
    return {1: "U,1", 2: "I,1", 3: "P,1"}


def test_items_lesen_und_werte_zuordnen():
    transport = ItemTableTransport(three_items(), number=3)
    with open_facade(transport) as wt:
        table = wt.items.read()
        assert [item.key for item in table.items] == ["U1", "I1", "P1"]

        mapped = wt.measure.read_mapped(table)
        assert list(mapped) == ["U1", "I1", "P1"]
        assert mapped["U1"].value == pytest.approx(1.0)
        assert mapped["P1"].value == pytest.approx(3.0)
        assert all(v.status is ValueStatus.OK for v in mapped.values())


def test_hold_wird_in_der_nur_lesen_sitzung_stillgelegt():
    transport = ItemTableTransport(three_items(), number=3)
    with open_facade(transport) as wt:
        with wt.measure.hold() as hold:
            hold.refresh()
    assert not [c for c in transport.written if c.startswith(":NUMeric:HOLD")]


def test_applied_schreibt_verifiziert_und_stellt_zurueck():
    """Der Ablauf, den Stufe 3 und Stufe 4 heute jeweils von Hand nachbauen."""
    transport = ItemTableTransport(three_items(), number=3)
    specs = [ItemSpec("U", "1"), ItemSpec("I", "1"), ItemSpec("P", "1"), ItemSpec("U", "SIGMA")]

    with WT3000.from_transport(
        transport, WTConfig(use_remote=False), read_only=False, allow_changes=True
    ) as wt:
        with wt.items.applied(specs) as target:
            assert target.number == 4
            # Zustand am 'Geraet' waehrend des Blocks.
            assert transport.number == 4
            assert transport.items[4] == "U,SIGMA"
            assert wt.items.verify(target) == []

        # Nach dem Block ist der Ausgangszustand wiederhergestellt.
        assert transport.number == 3
        assert wt.items.read().items[0].argument == "U,1"


def test_applied_stellt_auch_nach_einem_fehler_zurueck():
    transport = ItemTableTransport(three_items(), number=3)
    specs = [ItemSpec("U", "1"), ItemSpec("I", "1"), ItemSpec("P", "1"), ItemSpec("U", "SIGMA")]

    with WT3000.from_transport(
        transport, WTConfig(use_remote=False), read_only=False, allow_changes=True
    ) as wt:
        with pytest.raises(ZeroDivisionError):
            with wt.items.applied(specs):
                raise ZeroDivisionError("Fehler im Nutzblock")
        assert transport.number == 3
        assert 4 not in [item.index for item in wt.items.read().items]


# ---------------------------------------------------------------------------
# NEU (P-2, siehe PLAN_BEFUNDE_2026-08-19.md): misslungene Wiederherstellung.
#
# 'applied()' verspricht "Ausgangszustand garantiert zurueck". Bisher wurde ein
# Fehler im Restore nur protokolliert und dann verschluckt - der Aufrufer
# verliess den Block ohne Ausnahme und ohne jeden Hinweis darauf, dass die
# Item-Tabelle noch verstellt war.
#
# Die beiden Transporte unten stellen die zwei Arten des Misslingens nach:
# das Kommando kommt gar nicht durch, oder es kommt durch und wirkt nicht.
# ---------------------------------------------------------------------------


class BreakableItemTransport(ItemTableTransport):
    """Ab 'break_writes = True' scheitert jeder Schreibzugriff auf die Tabelle.

    Der abgerissene Verbindungsweg: das Kommando erreicht das Geraet nicht.
    """

    break_writes = False

    def write(self, command: str) -> None:
        if self.break_writes and command.upper().startswith(":NUMERIC:NORMAL"):
            raise TmctlError("TmcSend", 0xDEAD, command)
        super().write(command)


class IgnoringItemTransport(ItemTableTransport):
    """Ab 'ignore_writes = True' werden Schreibzugriffe angenommen, aber nicht uebernommen.

    Der heimtueckischere Fall: kein Fehler, kein Hinweis - der Zustand stimmt
    trotzdem nicht. Ohne Gegenprobe faellt das nirgends auf, weil das Geraet
    Set-Kommandos nicht quittiert.
    """

    ignore_writes = False

    def write(self, command: str) -> None:
        if self.ignore_writes:
            FakeTransport.write(self, command)  # nur protokollieren
            return
        super().write(command)


def test_misslungener_restore_wird_gemeldet_statt_verschluckt():
    """P-2: der Kern des Befunds BF-H2."""
    transport = BreakableItemTransport(three_items(), number=3)
    specs = [ItemSpec("U", "1"), ItemSpec("I", "1"), ItemSpec("P", "1"), ItemSpec("U", "SIGMA")]

    with WT3000.from_transport(
        transport, WTConfig(use_remote=False), read_only=False, allow_changes=True
    ) as wt:
        with pytest.raises(WTError):
            with wt.items.applied(specs):
                # Der Nutzblock selbst laeuft sauber durch - die Ausnahme kommt
                # ausschliesslich aus der Wiederherstellung.
                transport.break_writes = True
        transport.break_writes = False


def test_stiller_restore_ohne_wirkung_wird_von_der_gegenprobe_gefunden():
    """Restore laeuft ohne Fehler, der Ausgangszustand steht trotzdem nicht."""
    transport = IgnoringItemTransport(three_items(), number=3)
    specs = [ItemSpec("U", "1"), ItemSpec("I", "1"), ItemSpec("P", "1"), ItemSpec("U", "SIGMA")]

    with WT3000.from_transport(
        transport, WTConfig(use_remote=False), read_only=False, allow_changes=True
    ) as wt:
        with pytest.raises(WTError, match="Abweichung"):
            with wt.items.applied(specs):
                transport.ignore_writes = True
        transport.ignore_writes = False

        # Beleg dafuer, dass die Meldung berechtigt war: das 'Geraet' steht
        # noch auf der Zieltabelle, nicht auf dem Ausgangszustand.
        assert transport.number == 4


def test_fehler_im_nutzblock_und_im_restore_bleiben_beide_erhalten():
    """Befund.md verlangt ausdruecklich, dass keiner der beiden verloren geht.

    Python leistet das von selbst: die im finally ausgeloeste Ausnahme traegt
    die urspruengliche als '__context__'.
    """
    transport = BreakableItemTransport(three_items(), number=3)
    specs = [ItemSpec("U", "1"), ItemSpec("I", "1"), ItemSpec("P", "1"), ItemSpec("U", "SIGMA")]

    with WT3000.from_transport(
        transport, WTConfig(use_remote=False), read_only=False, allow_changes=True
    ) as wt:
        with pytest.raises(WTError) as fehler:
            with wt.items.applied(specs):
                transport.break_writes = True
                raise ZeroDivisionError("Fehler im Nutzblock")
        transport.break_writes = False

    assert isinstance(fehler.value.__context__, ZeroDivisionError)
    assert "Nutzblock" in str(fehler.value.__context__)


def test_gelungener_restore_wird_durch_die_gegenprobe_bestaetigt(caplog):
    """Gegenprobe: im Regelfall laeuft die Kontrolle durch und meldet Erfolg."""
    transport = ItemTableTransport(three_items(), number=3)
    specs = [ItemSpec("U", "1"), ItemSpec("I", "1"), ItemSpec("P", "1"), ItemSpec("U", "SIGMA")]

    with WT3000.from_transport(
        transport, WTConfig(use_remote=False), read_only=False, allow_changes=True
    ) as wt:
        with caplog.at_level("INFO"):
            with wt.items.applied(specs):
                pass

    assert any("Restore-Kontrolle" in r.message for r in caplog.records)
    assert transport.number == 3


def test_applied_verlangt_eine_schreibsitzung():
    transport = ItemTableTransport(three_items(), number=3)
    with open_facade(transport) as wt:
        with pytest.raises(WTError, match="allow_changes"):
            with wt.items.applied([ItemSpec("U", "1")]):
                pass
    assert not [c for c in transport.written if c.startswith(":NUMeric:NORMal:ITEM")]


def test_standardprofil_ist_ueber_die_fassade_erreichbar():
    with open_facade(ItemTableTransport(three_items(), number=3)) as wt:
        specs = wt.items.standard_profile()
        table = wt.items.build(specs)
        assert table.number == len(specs) == 31
        assert table.items[0].key == "U1"
