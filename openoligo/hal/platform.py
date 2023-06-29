"""
Provides the platform on which the program is running.
"""
from enum import Enum


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


__platform__ = get_platform()
