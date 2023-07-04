"""
Types for steps
"""
import logging
from enum import Enum
from functools import wraps

FlowWaitPair = tuple[int, float]
FlowWaitPairs = list[FlowWaitPair]


class FlowBranch(Enum):
    """
    Flow branch enumeration.
    """

    REACTION = "reaction"
    REAGENTS = "reagents"


def _step_decorator(coroutine, is_substep: bool = False):
    """
    Decorator for a step function (which carries out a reaction step).
    """

    @wraps(coroutine)
    async def wrapper_coroutine(*args, **kwargs):
        # instrument = Instrument()

        name, doc = coroutine.__name__, coroutine.__doc__.strip().split("\n")[0]
        level = logging.DEBUG if is_substep else logging.INFO
        repr_args = args[1:]  # Remove instrument from args
        logging.log(
            level, "Starting step [bold]%s[/]%s: %s", name, repr_args, doc, extra={"markup": True}
        )

        return await coroutine(*args, **kwargs)

    return wrapper_coroutine


def step(coroutine):
    """
    Decorator for a step function (which carries out a reaction step).
    """
    return _step_decorator(coroutine, is_substep=False)


def substep(coroutine):
    """
    Decorator for a substep function (which carries out a sub-reaction step).
    """
    return _step_decorator(coroutine, is_substep=True)
