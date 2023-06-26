import pytest

from openoligo.hal.board import Board
from openoligo.hal.devices import Switch, Valve
from openoligo.hal.types import ValveState, ValveType


def test_nc_no_valve():
    s1 = Valve(pin=1, name="test_switch", valve_type=ValveType.NORMALLY_CLOSED)
    s2 = Valve(pin=2, name="test_switch", valve_type=ValveType.NORMALLY_OPEN)

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
    s1 = Switch(name="test_switch", gpio_pin=Board.P3)
    assert s1.name == "test_switch"
    assert not s1.value  # = False


@pytest.mark.parametrize("valve_type", [ValveType.NORMALLY_CLOSED, ValveType.NORMALLY_OPEN])
def test_get_type(valve_type):
    m = Valve(pin=1, name="test_switch", valve_type=valve_type)
    assert m.get_type == valve_type, "get_type should return the valve type"
