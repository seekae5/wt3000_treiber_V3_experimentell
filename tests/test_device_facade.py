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

import re

import pytest
from conftest import range_responses  # UEBERARBEITET: keine zweite Antworttabelle

from wt3000_scpi import WT3000, WTConfig, WTError
from wt3000_scpi.wt3000_core import ReadOnlyViolation
from wt3000_scpi.wt3000_input import ConfigLocked
from wt3000_scpi.wt3000_itemspec import ItemSpec
from wt3000_scpi.wt3000_numeric import ValueStatus
from wt3000_scpi.wt3000_transport import FakeTransport, float_block

IDN = "YOKOGAWA,WT3000,C1B234567,F2.11"

_ITEM_NODE = re.compile(r"^:NUMERIC:NORMAL:ITEM(\d+)$")


def base_responses(
    wiring: str = "V3A3,P1W2",
    modules: str = "30,30,30,30",
    header: str = "0",
    numeric_format: str = "FLOat",
) -> dict:
    """Antworten, die die Fassade beim Verbinden und Pruefen braucht."""
    table = dict(range_responses())
    table.update(
        {
            "*IDN": IDN,
            ":INPUT:WIRING": wiring,
            ":INPUT:MODULE": modules,
            ":COMMUNICATE:HEADER": header,
            ":NUMERIC:FORMAT": numeric_format,
            ":STATUS:CONDITION": "0",
            ":NUMERIC:HOLD": "0",
        }
    )
    return table


class ItemTableTransport(FakeTransport):
    """FakeTransport, der Schreibzugriffe auf die Item-Tabelle uebernimmt.

    Nur so weit ausgebaut, wie die Item-Tabelle es verlangt: ITEM<n> und
    NUMber werden uebernommen, alles andere bleibt Tabellenantwort.
    """

    MAX_INDEX = 64

    def __init__(self, items: dict[int, str], number: int, **kwargs) -> None:
        self.items = dict(items)
        self.number = number

        responses = base_responses()
        responses[":NUMERIC:NORMAL"] = lambda _cmd: self._table_response()
        for index in range(1, self.MAX_INDEX + 1):
            responses[f":NUMERIC:NORMAL:ITEM{index}"] = self._item_responder(index)
        responses[":NUMERIC:NORMAL:VALUE"] = lambda _cmd: self._value_block()
        responses.update(kwargs.pop("responses", {}))
        super().__init__(responses, **kwargs)

    # -- Geraetemodell ------------------------------------------------------

    def _item_responder(self, index: int):
        return lambda _cmd: self.items.get(index, "NONE")

    def _table_response(self) -> str:
        parts = [str(self.number)]
        parts += [self.items.get(i, "NONE") for i in range(1, self.number + 1)]
        return ";".join(parts)

    def _value_block(self) -> bytes:
        """Ein Messwert je Item - aufsteigend, damit die Zuordnung pruefbar ist."""
        return float_block(float(i) for i in range(1, self.number + 1))

    def write(self, command: str) -> None:
        super().write(command)
        node, _, argument = command.strip().partition(" ")
        key = node.upper()
        match = _ITEM_NODE.match(key)
        if match:
            self.items[int(match.group(1))] = argument.strip()
        elif key == ":NUMERIC:NORMAL:NUMBER":
            self.number = int(argument)


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
