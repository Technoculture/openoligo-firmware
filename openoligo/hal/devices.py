"""
Switches can be used to control devices that can be turned on and off.
"""
import logging
from dataclasses import dataclass, field

from openoligo.hal.types import Board, Switchable, Valvable, ValveState, ValveType


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
    _state: bool = field(default=False, init=False)
    __switch_count: int = field(default=0, init=False, repr=False)

    def set(self, state: bool):
        """Set state of the switch ON or OFF."""
        __old_state = self._state
        self._state = state
        self.__switch_count += 1
        # self.board.set(self.gpio_pin, state)
        logging.info(
            "Switch (%s) set from %s to [bold]%s[/]",
            self.gpio_pin,
            __old_state,
            self._state,
            extra={"markup": True},
        )

    def toggle(self):
        """Toggle the state of the switch."""
        self.set(not self._state)

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
    __switch_count: int = field(init=False, default=0)
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
        __old_state: ValveState = self._state
        __new_state: ValveState = ValveState.OPEN_FLOW if state else ValveState.CLOSED_FLOW

        if __old_state == __new_state:
            logging.warn("Valve (%s) is already %s", self.gpio_pin, __old_state)
            return

        self._state = __new_state

        self.__switch_count += 1
        logging.info(
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
