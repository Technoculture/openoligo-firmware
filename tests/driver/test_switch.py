from unittest.mock import ANY, AsyncMock, patch

import pytest

from openoligo.driver.switch import (PneumaticValve, SimulatedSwitch,
                                     Switchable, periodic_toggle, toggle)
from openoligo.driver.types import SwitchingError


@pytest.mark.asyncio
async def test_simulated_switch():
    s1 = SimulatedSwitch(pin=1, name="test_switch")

    assert s1.name == "test_switch"
    assert s1.pin == 1
    assert not s1.value  # = False
    await toggle(s1)
    assert s1.value  # = True
    await s1.set(False)
    assert not s1.value  # = False


@pytest.mark.asyncio
async def test_periodic_toggle():
    s1 = SimulatedSwitch(pin=1, name="test_switch")

    # run the function for 5 toggles
    await periodic_toggle(switch=s1, interval=0.01, loop_forever=False, count=5)
    assert s1.switch_count == 5

    with pytest.raises(AssertionError):
        await periodic_toggle(switch=s1, interval=0, loop_forever=False, count=1)
    with pytest.raises(AssertionError):
        await periodic_toggle(switch=s1, interval=0.01, loop_forever=False, count=0)
    with pytest.raises(AssertionError):
        await periodic_toggle(switch=s1, interval=0.01, loop_forever=False, count=-1)
    with pytest.raises(AssertionError):
        await periodic_toggle(switch=s1, interval=-1, loop_forever=False, count=1)


@pytest.mark.asyncio
async def test_pneumatic_valve_init():
    p1 = PneumaticValve(pin=1, name="test_valve")
    assert isinstance(p1, SimulatedSwitch)
    assert isinstance(p1, Switchable)
    # print(p1)

    assert p1.name == "test_valve"
    assert p1.pin == 1
    assert not p1.value  # = False
    await toggle(p1)
    assert p1.value  # = True
    await p1.set(False)
    assert not p1.value  # = False


@pytest.mark.asyncio
async def test_periodic_toggle_exception_handling():
    s1 = AsyncMock()  # create a mock switch
    s1.set.side_effect = SwitchingError()  # set the side effect

    with patch("logging.error") as mock_log:  # patch logging to check if it logs the exception
        await periodic_toggle(switch=s1, interval=0.01, loop_forever=False, count=1)
        mock_log.assert_called_once_with(ANY)


# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(test_pneumatic_valve_init())
