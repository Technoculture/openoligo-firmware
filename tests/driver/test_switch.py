from unittest.mock import ANY, Mock, patch

import pytest

from openoligo.driver.switch import (MockSwitch, MockValve, PneumaticNoValve,
                                     Pump, Switchable, periodic_toggle, toggle)
from openoligo.driver.types import SwitchingError, ValveState, ValveType


def test_nc_no_switch():
    s1 = MockValve(pin=1, name="test_switch", valve_type=ValveType.NORMALLY_CLOSED)
    s2 = MockValve(pin=2, name="test_switch", valve_type=ValveType.NORMALLY_OPEN)

    assert s1._state == ValveState.CLOSED_FLOW, "NC valve _state should be closed by default"
    assert not s1.value, "NC valve value should be closed by default"
    assert s2._state == ValveState.OPEN_FLOW, "NO valve _state should be open by default"
    assert s2.value, "NO valve value should be open by default"

    s1.open()
    s2.open()
    assert s1._state == ValveState.OPEN_FLOW, "NC valve _state should be open, after open() call"
    assert s2._state == ValveState.OPEN_FLOW, "NO valve _state should be open, after open() call"

    s1.close()
    s2.close()
    assert (
        s1._state == ValveState.CLOSED_FLOW
    ), "NC valve _state should be closed, after close() call"
    assert (
        s2._state == ValveState.CLOSED_FLOW
    ), "NO valve _state should be closed, after close() call"


def test_simulated_switch():
    s1 = MockSwitch(name="test_switch")
    assert s1.name == "test_switch"
    assert not s1.value  # = False
    toggle(s1)
    assert s1.value  # = True
    s1.set(False)
    assert not s1.value  # = False


def test_periodic_toggle():
    s1 = MockSwitch(name="test_switch")

    # run the function for 5 toggles
    periodic_toggle(switch=s1, interval=0.01, loop_forever=False, count=5)
    assert s1._switch_count == 5

    with pytest.raises(AssertionError):
        periodic_toggle(switch=s1, interval=0, loop_forever=False, count=1)
    with pytest.raises(AssertionError):
        periodic_toggle(switch=s1, interval=0.01, loop_forever=False, count=0)
    with pytest.raises(AssertionError):
        periodic_toggle(switch=s1, interval=0.01, loop_forever=False, count=-1)
    with pytest.raises(AssertionError):
        periodic_toggle(switch=s1, interval=-1, loop_forever=False, count=1)


def test_pneumatic_no_valve_init():
    p1 = PneumaticNoValve(pin=1, name="test_valve")
    assert isinstance(p1, MockValve), "PneumaticNoValve should be a subclass of MockValve"
    assert isinstance(p1, Switchable), "PneumaticNoValve should be a subclass of Switchable"
    assert p1.name == "test_valve", "Name should be same as passed to constructor"
    assert p1._state == ValveState.OPEN_FLOW, "Valve should be open by default"
    assert p1.value, "Value should be True (open) by default"
    assert repr(p1) == "1[True]", "repr() should return pin and value"
    toggle(p1)
    assert not p1.value, "Value should be False (Closed) after toggle"
    p1.set(True)
    assert p1.value, "Value should be True (open) after set(True)"


def test_pump_init():
    p1 = Pump(name="test_pump")
    assert isinstance(p1, MockSwitch), "Pump should be a subclass of MockSwitch"
    assert isinstance(p1, Switchable), "Pump should be a subclass of Switchable"
    assert p1.name == "test_pump", "Name should be same as passed to constructor"
    assert not p1.value, "Value should be False (off) by default"
    toggle(p1)
    assert p1.value, "Value should be True (on) after toggle"
    p1.set(False)
    assert not p1.value, "Value should be False (off) after set(False)"
    p1.on()
    assert p1.value, "Value should be True (on) after on()"
    p1.off()
    assert not p1.value, "Value should be False (off) after off()"


def test_periodic_toggle_exception_handling():
    s1 = Mock()  # create a mock switch
    s1.set.side_effect = SwitchingError()  # set the side effect
    with patch("logging.error") as mock_log:  # patch logging to check if it logs the exception
        periodic_toggle(switch=s1, interval=0.01, loop_forever=False, count=1)
        mock_log.assert_called_once_with(ANY)


@pytest.mark.parametrize("valve_type", [ValveType.NORMALLY_CLOSED, ValveType.NORMALLY_OPEN])
def test_get_type(valve_type):
    m = MockValve(pin=1, name="test_switch", valve_type=valve_type)
    assert m.get_type == valve_type, "get_type should return the valve type"
