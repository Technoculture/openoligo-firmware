"""
Sets some parameters for the simulation.
"""
import os

from openoligo.hal.types import Platform, __platform__
from openoligo.utils.logger import configure_logger

logger = configure_logger()

# Simulation parameters
# Can be set using env variable OO_SIM_SPEED=1000
if os.environ.get("OO_SIM_SPEED") or __platform__ == Platform.SIM:
    SIMULATION_SPEEDUP_FACTOR = int(os.environ.get("OO_SIM_SPEED", 1000))
else:
    SIMULATION_SPEEDUP_FACTOR = 1

logger.info(
    "Using simulation speedup factor of %d (60min to %.2fs)",
    SIMULATION_SPEEDUP_FACTOR,
    60 * 60 / SIMULATION_SPEEDUP_FACTOR,
)
