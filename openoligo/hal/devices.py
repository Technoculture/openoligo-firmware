"""
Switches can be used to control devices that can be turned on and off.
"""
import logging
from dataclasses import dataclass, field

from openoligo.hal.board import Board
from openoligo.hal.types import Switchable, Valvable, ValveState, ValveType


@dataclass
class Switch(Switchable):
    """
    A switch that actually controls a GPIO pin on the Raspberry Pi.

    Attributes:
        name: Name of the switch.
        gpio_pin: GPIO pin number.
        board: Board object to access the GPIO pins.
    """

    gpio_pin: Board
    _switch_count: int = field(default=0, init=False)
    _state: bool = field(default=False, init=False)

    def set(self, state: bool):
        """Set state of the switch ON or OFF."""
        self._state = state
        self._switch_count += 1
        # self.board.set(self.gpio_pin, state)
        logging.info("Switch (%s) set to [bold]%s[/]", self.gpio_pin, state, extra={"markup": True})

    @property
    def value(self) -> bool:
        """
        Get the current value of the switch.

        raises:
            SwitchingError: If the switch is not set.
        """
        # if self._state is not self.board.value(self.gpio_pin):
        #    raise SwitchingError(f"Switch ({self.name}) is not set")
        return self._state


@dataclass
class Valve(Valvable):
    """
    A valve that actually controls a GPIO pin on the Raspberry Pi.
    """

    gpio_pin: Board
    valve_type: ValveType = field(default=ValveType.NORMALLY_OPEN)
    _switch_count: int = field(init=False, default=0)
    _state: ValveState = field(init=False)

    def __post_init__(self):
        """Initialize the valve."""
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
        self._state = ValveState.OPEN_FLOW if state else ValveState.CLOSED_FLOW
        self._switch_count += 1
        logging.debug(
            "Valve (%s) set to [bold]%s[/]", self.gpio_pin, self._state, extra={"markup": True}
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
