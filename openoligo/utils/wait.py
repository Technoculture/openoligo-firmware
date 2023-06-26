"""
Utilities for waiting.
"""
import asyncio
import logging
import time
from typing import Callable

from openoligo.utils.sim import SIMULATION_SPEEDUP_FACTOR


async def wait_async(seconds: float) -> None:
    """Wait for a given number of seconds."""
    logging.debug("Start waiting for %.2f seconds", seconds)
    await asyncio.sleep(seconds / SIMULATION_SPEEDUP_FACTOR)
    logging.debug("Done waiting for %.2f seconds", seconds)


def wait(seconds: float) -> None:
    """Wait for a given number of seconds."""
    logging.debug("Start waiting for %.2f seconds", seconds)
    time.sleep(seconds / SIMULATION_SPEEDUP_FACTOR)
    logging.debug("Done waiting for %.2f seconds", seconds)


async def with_wait_async(func: Callable, seconds: float, *args, **kwargs) -> None:
    """Call a function, then wait for a given number of seconds."""
    func(*args, **kwargs)
    await wait_async(seconds / SIMULATION_SPEEDUP_FACTOR)


def with_wait(
    func: Callable, seconds: float, *args, **kwargs
) -> None:  # pylint: disable=unused-argument
    """Call a function, then wait for a given number of seconds."""
    func(*args, **kwargs)
    wait(seconds / SIMULATION_SPEEDUP_FACTOR)


def ms(seconds: float) -> float:  # pylint: disable=invalid-name
    """Convert seconds to milliseconds."""
    return seconds / 1000
