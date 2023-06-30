"""
Utilities for waiting.
"""
import asyncio
import logging
import time

from openoligo.utils.sim import SIMULATION_SPEEDUP_FACTOR


async def wait_async(seconds: float) -> None:
    """Wait for a given number of seconds."""
    logging.debug("Start waiting for %.2f seconds", seconds)  # pragma: no cover
    await asyncio.sleep(seconds / SIMULATION_SPEEDUP_FACTOR)
    logging.debug("Done waiting for %.2f seconds", seconds)  # pragma: no cover


def wait(seconds: float) -> None:
    """Wait for a given number of seconds."""
    logging.debug("Start waiting for %.2f seconds", seconds)
    time.sleep(seconds / SIMULATION_SPEEDUP_FACTOR)
    logging.debug("Done waiting for %.2f seconds", seconds)


def ms(seconds: float) -> float:  # pylint: disable=invalid-name
    """Convert seconds to milliseconds."""
    return seconds / 1000
