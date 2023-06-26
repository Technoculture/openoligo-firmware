"""
Driver imports for convenience.
"""

from openoligo.hal.gpio import is_rpi
from openoligo.hal.pins import Board
from openoligo.hal.devices import Valve, Switch
from openoligo.hal.types import (
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
    "InvalidManifoldSizeError",
    "Switchable",
    "SwitchingError",
    "Valvable",
    "ValveState",
    "ValveType",
]
