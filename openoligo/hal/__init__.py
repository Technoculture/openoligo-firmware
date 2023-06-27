"""
Driver imports for convenience.
"""

from openoligo.hal.board import Pinout
from openoligo.hal.devices import Switch, Valve
from openoligo.hal.gpio import is_rpi
from openoligo.hal.types import (
    Board,
    GpioMode,
    InvalidManifoldSizeError,
    Switchable,
    SwitchingError,
    Valvable,
    ValveState,
    ValveType,
)

__all__ = [
    "is_rpi",
    "Valve",
    "Switch",
    "Board",
    "GpioMode",
    "Pinout",
    "InvalidManifoldSizeError",
    "Switchable",
    "SwitchingError",
    "Valvable",
    "ValveState",
    "ValveType",
]
