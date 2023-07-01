"""
Driver imports for convenience.
"""

from openoligo.hal.board import Pinout, list_configurable_pins
from openoligo.hal.devices import Switch, Valve
from openoligo.hal.gpio import MockGPIO, Platform, __platform__
from openoligo.hal.types import (
    GpioMode,
    InvalidManifoldSizeError,
    Switchable,
    SwitchingError,
    Valvable,
    ValveState,
    ValveType,
    board,
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
    "list_configurable_pins",
    "MockGPIO",
]
