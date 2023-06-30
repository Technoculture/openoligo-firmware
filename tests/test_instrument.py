from unittest.mock import Mock, patch

import pytest

from openoligo.hal.board import Pinout
from openoligo.hal.devices import Valve
from openoligo.hal.gpio import get_gpio
from openoligo.hal.types import OneDestinationException, OneSourceException, ValveRole, board
from openoligo.instrument import Instrument


@pytest.fixture
def mock_pinout():
    # create a dictionary of mock valves
    valves = {
        "I1": Mock(spec=Valve),
        "I2": Mock(spec=Valve),
        "I3": Mock(spec=Valve),
        "T1": Mock(spec=Valve),
        "T2": Mock(spec=Valve),
        "O1": Mock(spec=Valve),
        "O2": Mock(spec=Valve),
        "B1": Mock(spec=Valve),
        "B2": Mock(spec=Valve),
        "N1": Mock(spec=Valve),
    }

    # set the role of each mock valve
    valves["I1"].role = ValveRole.INLET
    valves["I2"].role = ValveRole.INLET
    valves["I3"].role = ValveRole.INLET
    valves["T1"].role = ValveRole.TRANSIT
    valves["T2"].role = ValveRole.TRANSIT
    valves["O1"].role = ValveRole.OUTLET
    valves["O2"].role = ValveRole.OUTLET
    valves["B1"].role = ValveRole.BRANCH
    valves["B2"].role = ValveRole.BRANCH

    # mock the Pinout object
    pinout = Mock(spec=Pinout)
    pinout.get.side_effect = valves.get
    pinout.valves.return_value = valves

    return pinout


def test_instrument_init(mock_pinout):
    instrument = Instrument(mock_pinout)
    assert instrument.pinout == mock_pinout


def test_get_valve(mock_pinout):
    # with the valve present
    instrument = Instrument(mock_pinout)
    valve = instrument._Instrument__get_valve("I2")
    assert valve.role == ValveRole.INLET  # assuming all valves have INLET role in this test

    # with the valve not present
    with pytest.raises(ValueError):
        instrument._Instrument__get_valve("Non-existent Valve")


def test_validate_valve_set(mock_pinout):
    instrument = Instrument(mock_pinout)
    # with one inlet and one outlet valve
    instrument.pinout.get("I1").role = ValveRole.INLET
    instrument.pinout.get("O1").role = ValveRole.OUTLET

    instrument.validate_valve_set(["I1", "O1"])

    # with multiple inlet valves
    instrument.pinout.get("I1").role = ValveRole.INLET

    with pytest.raises(OneSourceException):
        instrument.validate_valve_set(["I1", "I2"])
        instrument.validate_valve_set(["I1", "I2", "I3"])
        instrument.validate_valve_set(["I1", "I2", "O1"])

    # with multiple outlet valves
    instrument.pinout.get("O2").role = ValveRole.OUTLET

    with pytest.raises(OneDestinationException):
        instrument.validate_valve_set(["I1", "O1", "O2"])


def test_all_except(mock_pinout):
    instrument = Instrument(mock_pinout)
    instrument.all_except(["I1", "O1"])

    assert instrument.pinout.get("I1").open.called
    assert not instrument.pinout.get("O1").close.called

    for name in ["I2", "I3", "T1", "T2", "O2", "B1", "B2"]:
        assert not instrument.pinout.get(name).open.called
        assert instrument.pinout.get(name).close.called
