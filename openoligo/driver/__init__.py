"""
Driver imports for convenience.
"""

from openoligo.driver.board import Board, is_rpi
from openoligo.driver.manifold import Manifold
from openoligo.driver.rpi_pins import RPi
from openoligo.driver.switch import BaseValve, PneumaticNoValve, Pump, periodic_toggle, toggle
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
    "is_rpi",
    "Manifold",
    "BaseValve",
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
