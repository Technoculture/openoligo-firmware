"""
Driver imports for convenience.
"""

from openoligo.hal.board import Pinout
from openoligo.hal.devices import Switch, Valve
from openoligo.hal.gpio import Platform, __platform__
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
    "__platform__",
    "Platform",
    "Valve",
    "Switch",
    "board",
    "GpioMode",
    "Pinout",
    "InvalidManifoldSizeError",
    "Switchable",
    "SwitchingError",
    "Valvable",
    "ValveState",
    "ValveType",
]
