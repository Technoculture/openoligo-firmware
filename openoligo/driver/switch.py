import asyncio
import logging
from dataclasses import dataclass

from openoligo.driver.types import Switchable


@dataclass
class SimulatedSwitch(Switchable):
    pin: int
    name: str
    switch_count: int = 0
    _state: bool = False

    def set(self, switch: bool):
        self._state = switch
        self.switch_count += 1

    @property
    def value(self) -> bool:
        return self._state

    def toggle(self):
        self.set(not self.value)


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
            switch.toggle()
            logging.info(switch)
            await asyncio.sleep(interval)
    except Exception as e:
        logging.error(f"Error occurred while toggling switch: {e}")
