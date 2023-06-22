"""
Utilities for waiting.
"""
import time
from typing import Any


def wait(seconds: float) -> None:
    """Wait for a given number of seconds."""
    time.sleep(seconds)


def ms(seconds: float) -> float:  # pylint: disable=invalid-name
    """Convert seconds to milliseconds."""
    return seconds / 1000


def with_wait(func: Any, seconds: float) -> None:  # pylint: disable=unused-argument
    """Call a function, then wait for a given number of seconds."""
    time.sleep(seconds)
