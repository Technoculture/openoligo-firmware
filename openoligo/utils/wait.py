"""
Utilities for waiting.
"""
from time import sleep


def wait(seconds: float) -> None:
    """Wait for a given number of seconds."""
    sleep(seconds)


def ms(seconds: float) -> float:  # pylint: disable=invalid-name
    """Convert seconds to milliseconds."""
    return seconds / 1000
