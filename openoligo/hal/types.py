"""
This module contains definitions of protocols and exceptions related to switchable devices.
"""
from enum import Enum
from typing import Protocol


def is_rpi() -> bool:
    """Returns True if running on a Raspberry Pi, False otherwise."""
    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8") as file:
            return "Raspberry" in file.read()
    except FileNotFoundError:
        return False


def is_bb() -> bool:
    """Returns True if running on a Raspberry Pi, False otherwise."""
    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8") as file:
            return "AM33XX" in file.read()
    except FileNotFoundError:
        return False


class Platform(Enum):
    """Platform type."""

    RPI = "RPI"
    BB = "BB"
    SIM = "SIM"


def get_platform() -> Platform:
    """Get the platform type."""
    if is_rpi():
        return Platform.RPI
    if is_bb():
        return Platform.BB
    return Platform.SIM


class RPiBoard(Enum):
    """
    Enumerates the GPIO pins on the Raspberry Pi 3 Model B.
    """

    P3 = 3
    P5 = 5
    P7 = 7
    P8 = 8
    P10 = 10
    P11 = 11
    P12 = 12
    P13 = 13
    P15 = 15
    P16 = 16
    P18 = 18
    P19 = 19
    P21 = 21
    P22 = 22
    P23 = 23
    P24 = 24
    P26 = 26
    P27 = 27
    P28 = 28
    P29 = 29
    P31 = 31
    P32 = 32
    P33 = 33
    P35 = 35
    P36 = 36
    P37 = 37
    P38 = 38
    P40 = 40


class BbBoard(Enum):
    """
    Enumerates the GPIO pins on the Beaglebone Black.
    """

    P3 = 3
    P5 = 5
    P7 = 7
    P8 = 8
    P10 = 10
    P11 = 11
    P12 = 12
    P13 = 13
    P15 = 15
    P16 = 16
    P18 = 18
    P19 = 19
    P21 = 21
    P22 = 22
    P23 = 23
    P24 = 24
    P26 = 26
    P27 = 27
    P28 = 28
    P29 = 29
    P31 = 31
    P32 = 32
    P33 = 33
    P35 = 35
    P36 = 36
    P37 = 37
    P38 = 38
    P40 = 40


__platform__ = get_platform()


if __platform__ == Platform.BB:
    Board = BbBoard
else:
    Board = RPiBoard  # Also acts as a mock board


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

    @property
    def gpio(self) -> Board:
        """Get the GPIO pin number."""
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
