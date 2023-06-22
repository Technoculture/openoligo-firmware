"""
This module contains definitions of protocols and exceptions related to switchable devices.
"""
from enum import Enum
from typing import Protocol


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
