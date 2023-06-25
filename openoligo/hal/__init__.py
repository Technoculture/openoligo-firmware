"""
Driver imports for convenience.
"""

from openoligo.hal.gpio import is_rpi
from openoligo.hal.pins import RPi
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
    "RPi",
    "GpioMode",
    "InvalidManifoldSizeError",
    "Switchable",
    "SwitchingError",
    "Valvable",
    "ValveState",
    "ValveType",
]
