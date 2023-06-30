"""
This module contains definitions of protocols and exceptions related to switchable devices.
"""
from enum import Enum
from typing import Iterator, Protocol

from openoligo.hal.platform import (
    PLATFORM_TO_BOARD,
    MinimumCommonPinout,
    Platform,
    __platform__,
    rpi_board_pins,
)


class Board:
    """
    Represents a board with a minimum common pinout.
    """

    board_dict: MinimumCommonPinout

    def __init__(self, platform: Platform) -> None:
        """Creates a board given a particular platform."""
        self.board_dict = PLATFORM_TO_BOARD.get(platform, rpi_board_pins)

    def __getattr__(self, name: str) -> str:
        """Return the pin number (as a string) for a given pin name."""
        if name.startswith("P"):
            try:
                return self.board_dict[name]
            except KeyError as exc:
                raise AttributeError(f"{self.__class__.__name__} has no pin {name}") from exc
        raise AttributeError(f"{self.__class__.__name__} has no attribute {name}")

    def __len__(self) -> int:
        """Return the number of pins on the board."""
        return len(self.board_dict)

    def __repr__(self) -> str:
        """Return a string representation of the board."""
        return f"{self.__class__.__name__}({self.board_dict})"

    def __iter__(self) -> Iterator[tuple[str, str]]:
        """Return an iterator over the pin names."""
        return iter(self.board_dict.items())


board = Board(__platform__)


class GpioMode(Enum):
    """GPIO mode."""

    IN = 0
    OUT = 1


class ValveState(Enum):
    """This class represents the state of a valve."""

    OPEN_FLOW = 0
    CLOSED_FLOW = 1


class ValveType(Enum):
    """Valve Type: NC/NO"""

    NORMALLY_CLOSED = 0
    NORMALLY_OPEN = 1


class ValveRole(Enum):
    """Valve Role: Inlet/Outlet/Transit/Branch"""

    INLET = 0
    OUTLET = 1
    TRANSIT = 2
    BRANCH = 3


class Switchable(Protocol):
    """
    This protocol represents a switchable device. Any class implementing this protocol should
    be able to set, get the current value and toggle the state of the switch.
    """

    def __init__(self, pin: int, name: str):
        """Initialize the switchable device."""
        raise NotImplementedError

    def set(self, state: bool):
        """Set the state of the switch."""
        raise NotImplementedError

    #    @property
    #    def gpio(self) -> Board:
    #        """Get the GPIO pin number."""
    #        raise NotImplementedError

    @property
    def value(self) -> bool:
        """Get the current value of the switch."""
        raise NotImplementedError


class Valvable(Switchable, Protocol):
    """
    A semantic wrapper around a switchable device. This class is used to represent a valve.
    """

    def __init__(self, pin: int, name: str, valve_type: ValveType = ValveType.NORMALLY_OPEN):
        """Initialize the valve."""
        raise NotImplementedError

    def open(self):
        """Open the valve."""
        raise NotImplementedError

    def close(self):
        """Close the valve."""
        raise NotImplementedError

    @property
    def get_type(self) -> ValveType:
        """Get the type of the valve."""
        raise NotImplementedError


class SwitchingError(Exception):
    """
    An exception that represents a failure in switching operation.
    """


class InvalidManifoldSizeError(Exception):
    """
    An exception that represents an invalid manifold size.
    """


class NoSuchPinInPinout(Exception):
    """
    Thrown when a pin for a given name is not found in the pinout.
    """


class OneSourceException(SwitchingError):
    """
    When more than one source valve is being attempted to be used.
    """


class OneDestinationException(SwitchingError):
    """
    When more than one destination valve is being attempted to be used.
    """
