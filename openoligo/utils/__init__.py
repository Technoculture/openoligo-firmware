"""
Various unrelated modules and functions for logging, simulation, busy waiting, etc.
"""
from openoligo.utils.sim import SIMULATION_SPEEDUP_FACTOR
from openoligo.utils.wait import ms, wait, wait_async

__all__ = ["ms", "wait", "wait_async", "SIMULATION_SPEEDUP_FACTOR"]
