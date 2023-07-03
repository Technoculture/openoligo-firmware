"""
Utilities for waiting.
"""
import asyncio
import time

from openoligo.utils.logger import configure_logger
from openoligo.utils.sim import SIMULATION_SPEEDUP_FACTOR

logger = configure_logger()


async def wait_async(seconds: float) -> None:
    """Wait for a given number of seconds."""
    logger.debug("Start waiting for %.2f seconds", seconds)  # pragma: no cover
    await asyncio.sleep(seconds / SIMULATION_SPEEDUP_FACTOR)
    logger.debug("Done waiting for %.2f seconds", seconds)  # pragma: no cover


def wait(seconds: float) -> None:
    """Wait for a given number of seconds."""
    logger.debug("Start waiting for %.2f seconds", seconds)
    time.sleep(seconds / SIMULATION_SPEEDUP_FACTOR)
    logger.debug("Done waiting for %.2f seconds", seconds)


def ms(seconds: float) -> float:  # pylint: disable=invalid-name
    """Convert seconds to milliseconds."""
    return seconds / 1000
