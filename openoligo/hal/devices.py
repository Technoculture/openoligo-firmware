"""
Switches can be used to control devices that can be turned on and off.
"""
import logging
from dataclasses import dataclass, field

from openoligo.hal.gpio import get_gpio
from openoligo.hal.types import Switchable, Valvable, ValveRole, ValveState, ValveType


@dataclass
class Switch(Switchable):
    """
    A switch that actually controls a GPIO pin on the Raspberry Pi.

    Attributes:
        name: Name of the switch.
        gpio_pin: GPIO pin number.
        board: Board object to access the GPIO pins.
    """

    gpio_pin: str
    _state: bool = field(default=False, init=False)
    _switch_count: int = field(default=0, init=False, repr=False)

    def __post_init__(self):
        """Initialize the switch."""
        self.controller = get_gpio()
        self.controller.setup_pin(self.gpio_pin)

    def set(self, state: bool):
        """Set state of the switch ON or OFF."""
        __old_state = self._state
        __new_state = state

        if __old_state == __new_state:
            logging.warning("Switch %s is already %s", self.gpio_pin, __old_state)
            return

        self._state = __new_state
        self.controller.set(self.gpio_pin, state)
        self._switch_count += 1

        logging.debug(
            "Switch (%s) set from %s to [bold]%s[/]",
            self.gpio_pin,
            __old_state,
            __new_state,
            extra={"markup": True},
        )

    def toggle(self):
        """Toggle the state of the switch."""
        self.set(not self._state)

    @property
    def value(self) -> bool:
        """
        Get the current value of the switch.
        """
        return self._state


@dataclass
class Valve(Valvable):
    """
    A valve that actually controls a GPIO pin on the Raspberry Pi.
    """

    gpio_pin: str
    role: ValveRole = field(default=ValveRole.INLET)
    valve_type: ValveType = field(default=ValveType.NORMALLY_OPEN)
    _switch_count: int = field(init=False, default=0)
    _state: ValveState = field(init=False)

    def __post_init__(self):
        """Initialize the valve."""
        self.controller = get_gpio()
        self.controller.setup_pin(self.gpio_pin)

        self._state = (
            ValveState.CLOSED_FLOW
            if self.valve_type == ValveType.NORMALLY_CLOSED
            else ValveState.OPEN_FLOW
        )

    def open(self):
        """Open the valve."""
        self.set(True)

    def close(self):
        """Close the valve."""
        self.set(False)

    def set(self, state: bool):
        """Set the state of the valve."""
        __old_state: ValveState = self._state
        __new_state: ValveState = ValveState.OPEN_FLOW if state else ValveState.CLOSED_FLOW

        if __old_state == __new_state:
            if __old_state == ValveState.OPEN_FLOW:
                logging.debug("Valve (%s) is already %s", self.gpio_pin, __old_state)
            return

        self.controller.set(self.gpio_pin, state)
        self._state = __new_state

        self._switch_count += 1
        logging.debug(
            "Valve (%s) set from %s to [bold]%s[/]",
            self.gpio_pin,
            __old_state,
            self._state,
            extra={"markup": True},
        )

    @property
    def value(self) -> bool:
        """Get the current value of the valve."""
        return self._state == ValveState.OPEN_FLOW

    @property
    def get_type(self) -> ValveType:
        """Get the type of the valve."""
        return self.valve_type

    def __repr__(self) -> str:
        return f"{self.gpio_pin}[{self.value}]"
