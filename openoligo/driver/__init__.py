"""
Driver imports for convenience.
"""

from openoligo.driver.gpio import Board, get_gpio, is_rpi
from openoligo.driver.manifold import Manifold
from openoligo.driver.rpi_pins import RPi
from openoligo.driver.switch import MockValve, PneumaticNoValve, Pump, periodic_toggle, toggle
from openoligo.driver.types import (
    GpioMode,
    InvalidManifoldSizeError,
    Switchable,
    SwitchingError,
    Valvable,
    ValveState,
    ValveType,
)

__all__ = [
    "Board",
    "get_gpio",
    "is_rpi",
    "Manifold",
    "MockValve",
    "PneumaticNoValve",
    "periodic_toggle",
    "Pump",
    "RPi",
    "toggle",
    "GpioMode",
    "InvalidManifoldSizeError",
    "Switchable",
    "SwitchingError",
    "Valvable",
    "ValveState",
    "ValveType",
]
