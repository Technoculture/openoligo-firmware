"""
Switches can be used to control devices that can be turned on and off.
"""
import logging
import time
from dataclasses import dataclass
from typing import Callable

from openoligo.driver.types import Switchable, SwitchingError


@dataclass
class SimulatedSwitch(Switchable):
    """
    This class represents a simulated switch. It is useful for testing purposes.
    It can also be used as a base class for other switchable devices.
    """

    pin: int
    name: str
    on_set: Callable[[bool], None] = lambda _: None
    switch_count: int = 0
    _state: bool = False

    def set(self, state: bool):
        """Set state of the switch ON or OFF."""
        self._state = state
        self.on_set(state)
        self.switch_count += 1

    @property
    def value(self) -> bool:
        """Get the current value of the switch."""
        return self._state


class PneumaticValve(SimulatedSwitch):
    """
    This class represents a pneumatic valve. It is useful for testing purposes.
    It can also be used as a base class for other switchable devices.
    """

    def __init__(self, pin: int, name: str):
        super().__init__(pin, name, on_set=lambda _: None)


class Pump(SimulatedSwitch):
    """
    This class represents a pump. It is useful for testing purposes.
    It can also be used as a base class for other switchable devices.
    """

    def __init__(self, pin: int, name: str):
        super().__init__(pin, name, on_set=lambda _: None)

    def set(self, state: bool):
        super().set(state)
        if state:
            logging.info("Starting pump %s on pin %s", self.name, self.pin)
        else:
            logging.info("Stopping pump %s on pin %s", self.name, self.pin)


def toggle(switch: Switchable):
    """
    Toggle the state of a switchable device.

    :param switch: The device to be toggled
    """
    switch.set(not switch.value)
    logging.debug("Toggled the switch: %s", switch)


def periodic_toggle(switch: Switchable, interval: float, loop_forever: bool = True, count: int = 0):
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
            toggle(switch)
            logging.debug(switch)
            time.sleep(interval)
    except SwitchingError as error:
        logging.error(error)
