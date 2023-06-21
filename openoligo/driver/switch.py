"""
Switches can be used to control devices that can be turned on and off.
"""
import asyncio
import logging
from dataclasses import dataclass

from openoligo.driver.types import Switchable, SwitchingError


@dataclass
class SimulatedSwitch(Switchable):
    """
    This class represents a simulated switch. It is useful for testing purposes.
    It can also be used as a base class for other switchable devices.
    """

    pin: int
    name: str
    switch_count: int = 0
    _state: bool = False

    async def set(self, switch: bool):
        """Set state of the switch ON or OFF."""
        self._state = switch
        self.switch_count += 1

    @property
    def value(self) -> bool:
        """Get the current value of the switch."""
        return self._state


async def toggle(switch: Switchable):
    """
    Toggle the state of a switchable device.

    :param switch: The device to be toggled
    """
    await switch.set(not switch.value)
    logging.debug("Toggled the switch: %s", switch)


async def periodic_toggle(
    switch: Switchable, interval: float, loop_forever: bool = True, count: int = 0
):
    """
    Periodically toggle the state of a switchable device.

    :param switch: The device to be toggled
    :param interval: The time interval between toggles in seconds
    :param loop_forever: If True, toggles the device indefinitely, else toggles it for 'count' times
    :param count: The number of times to toggle the device (ignored if loop_forever is True)
    """
    assert interval > 0, "Interval must be greater than 0"
    assert count > 0 or loop_forever, "Must toggle at least once"

    try:
        while loop_forever or count > 0:
            count -= 1 if count > 0 else 0
            await toggle(switch)
            logging.debug(switch)
            await asyncio.sleep(interval)
    except SwitchingError as error:
        logging.error(error)
