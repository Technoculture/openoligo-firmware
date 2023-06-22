"""
Imports all the classes and functions from the openoligo package.
This is for convenience only. It is recommended to import only the
classes and functions that are needed.
"""

# flake8: noqa

from openoligo.driver.gpio import Board, get_gpio, is_rpi
from openoligo.driver.manifold import Manifold
from openoligo.driver.rpi_pins import RPi
from openoligo.driver.switch import (MockValve, PneumaticNoValve, Pump,
                                     periodic_toggle, toggle)
from openoligo.driver.types import (GpioMode, InvalidManifoldSizeError,
                                    Switchable, SwitchingError, Valvable,
                                    ValveState, ValveType)
from openoligo.utils.wait import ms, wait

__all__ = [
    "Board",
    "get_gpio",
    "is_rpi",
    "Manifold",
    "RPi",
    "PneumaticNoValve",
    "Pump",
    "MockValve",
    "periodic_toggle",
    "toggle",
    "GpioMode",
    "InvalidManifoldSizeError",
    "Switchable",
    "SwitchingError",
    "Valvable",
    "ValveState",
    "ValveType",
    "ms",
    "wait",
]
