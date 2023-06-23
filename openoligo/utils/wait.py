"""
Utilities for waiting.
"""
import logging
import time
from typing import Callable


def wait(seconds: float) -> None:
    """Wait for a given number of seconds."""
    logging.debug("Start waiting for %.2f seconds", seconds)
    time.sleep(seconds)
    logging.debug("Done waiting for %.2f seconds", seconds)


def ms(seconds: float) -> float:  # pylint: disable=invalid-name
    """Convert seconds to milliseconds."""
    return seconds / 1000


def with_wait(
    func: Callable, seconds: float, *args, **kwargs
) -> None:  # pylint: disable=unused-argument
    """Call a function, then wait for a given number of seconds."""
    func(*args, **kwargs)
    wait(seconds)
