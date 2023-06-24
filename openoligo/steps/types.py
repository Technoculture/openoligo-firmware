"""
Types for steps
"""
from enum import Enum


FlowWaitPair = tuple[int, float]
FlowWaitPairs = list[FlowWaitPair]


class FlowBranch(Enum):
    """
    Flow branch enumeration.
    """

    REACTION = "reaction"
    REAGENTS = "reagents"
