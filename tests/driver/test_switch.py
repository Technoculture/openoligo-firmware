from unittest.mock import ANY, Mock, patch

import pytest

from openoligo.driver.switch import (PneumaticValve, Pump, SimulatedSwitch,
                                     Switchable, periodic_toggle, toggle)
from openoligo.driver.types import SwitchingError


def test_simulated_switch():
    s1 = SimulatedSwitch(pin=1, name="test_switch")

    assert s1.name == "test_switch"
    assert s1.pin == 1
    assert not s1.value  # = False
    toggle(s1)
    assert s1.value  # = True
    s1.set(False)
    assert not s1.value  # = False


def test_periodic_toggle():
    s1 = SimulatedSwitch(pin=1, name="test_switch")

    # run the function for 5 toggles
    periodic_toggle(switch=s1, interval=0.01, loop_forever=False, count=5)
    assert s1.switch_count == 5

    with pytest.raises(AssertionError):
        periodic_toggle(switch=s1, interval=0, loop_forever=False, count=1)
    with pytest.raises(AssertionError):
        periodic_toggle(switch=s1, interval=0.01, loop_forever=False, count=0)
    with pytest.raises(AssertionError):
        periodic_toggle(switch=s1, interval=0.01, loop_forever=False, count=-1)
    with pytest.raises(AssertionError):
        periodic_toggle(switch=s1, interval=-1, loop_forever=False, count=1)


def test_pneumatic_valve_init():
    p1 = PneumaticValve(pin=1, name="test_valve")
    assert isinstance(p1, SimulatedSwitch)
    assert isinstance(p1, Switchable)
    # print(p1)

    assert p1.name == "test_valve"
    assert p1.pin == 1
    assert not p1.value  # = False
    toggle(p1)
    assert p1.value  # = True
    p1.set(False)
    assert not p1.value  # = False


def test_pump_init():
    p1 = Pump(pin=1, name="test_pump")
    assert isinstance(p1, SimulatedSwitch)
    assert isinstance(p1, Switchable)
    # print(p1)

    assert p1.name == "test_pump"
    assert p1.pin == 1
    assert not p1.value  # = False
    toggle(p1)
    assert p1.value  # = True
    p1.set(False)
    assert not p1.value  # = False


def test_periodic_toggle_exception_handling():
    s1 = Mock()  # create a mock switch
    s1.set.side_effect = SwitchingError()  # set the side effect

    with patch("logging.error") as mock_log:  # patch logging to check if it logs the exception
        periodic_toggle(switch=s1, interval=0.01, loop_forever=False, count=1)
        mock_log.assert_called_once_with(ANY)
