from openoligo.driver.switch import SimulatedSwitch, periodic_toggle
import pytest
from unittest.mock import Mock, patch


def test_simulated_switch():
    s1 = SimulatedSwitch(pin=1, name="test_switch")

    assert s1.name == "test_switch"
    assert s1.pin == 1
    assert s1.value == False
    s1.toggle()
    assert s1.value == True
    s1.set(False)
    assert s1.value == False


#@pytest.mark.asyncio
#async def test_periodic_toggle():
#    s1 = SimulatedSwitch(pin=1, name="test_switch")
#
#    # run the function for 5 toggles
#    await periodic_toggle(switch=s1, interval=0.01, loop_forever=False, count=5)
#    assert s1.switch_count == 5
#
#    # await periodic_toggle(switch=s1, interval=0.01, loop_forever=False, count=0)
#    pytest.raises(AssertionError, periodic_toggle, s1, 0, False, 1)
#    pytest.raises(AssertionError, periodic_toggle, s1, 0.01, False, 0)
#    pytest.raises(AssertionError, periodic_toggle, s1, 0.01, False, -1)
#    pytest.raises(AssertionError, periodic_toggle, s1, -1, False, 1)

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
async def test_periodic_toggle_exception_handling():
    s1 = Mock()  # create a mock switch
    s1.toggle.side_effect = Exception("test")  # raise exception when toggle is called

    with patch('logging.error') as mock_log:  # patch logging to check if it logs the exception
        await periodic_toggle(switch=s1, interval=0.01, loop_forever=False, count=1)
        mock_log.assert_called()  # assert that the error was logged


