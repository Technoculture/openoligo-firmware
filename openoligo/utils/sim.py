"""
Sets some parameters for the simulation.
"""
import logging
import os

from openoligo.hal.gpio import is_rpi

# Simulation parameters
# Can be set using env variable OO_SIM_SPEED=1000
SIMULATION_SPEEDUP_FACTOR = 1 if is_rpi() else int(os.environ.get("OO_SIM_SPEED", 1000))
logging.info(
    "Using simulation speedup factor of %d (60min to %.2fs)",
    SIMULATION_SPEEDUP_FACTOR,
    60 * 60 / SIMULATION_SPEEDUP_FACTOR,
)
