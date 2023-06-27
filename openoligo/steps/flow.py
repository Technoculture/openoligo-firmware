"""
Functions to create various flows from reagents to columns,
and to clean columns.
"""
import functools
import logging

from openoligo import Instrument
from openoligo.steps.types import FlowBranch


def step(coroutine):
    """
    Decorator for a step function (which carries out a reaction step).
    """

    @functools.wraps(coroutine)
    async def wrapper(*args, **kwargs):
        doc = coroutine.__doc__.strip()
        name = coroutine.__name__
        if doc:
            logging.info("%s: %s", name, doc)
        return await coroutine(*args, **kwargs)

    return wrapper


def send_to_prod(instrument: Instrument, src: str) -> None:
    """
    Flow a reagent to the final product outlet.

    args:
        src: Slot to flow reagents from.
    """
    instrument.all_except([src, "prod", "branch", "rxn_out"])
    logging.debug("Flowing %s to prod", src)


def send_to_waste_rxn(instrument: Instrument, src: str) -> None:
    """
    Flow a reagent to the final product outlet.

    args:
        src: Slot to flow reagents from.
    """
    instrument.all_except([src, "branch", "rxn_out", "waste_rxn"])
    logging.debug("Flowing %s to reaction waste", src)


def solvent_wash(instrument: Instrument, branch: FlowBranch) -> None:
    """
    Wash column with solvent.

    args:
        branch: FlowBranch to wash.
    """
    logging.debug("Initiating washing flow branch %s with solvent", branch)
    if branch == FlowBranch.REACTION:
        instrument.all_except(["sol", "rxn_out", "branch", "waste_rxn"])
    elif branch == FlowBranch.REAGENTS:
        instrument.all_except(["sol", "reagents", "waste"])
    logging.debug("Washing of branch %s complete", branch)


def solvent_wash_all(instrument: Instrument) -> None:
    """
    Wash all flow branches with solvent.
    """

    for branch in FlowBranch:
        solvent_wash(instrument, branch)


def dry(instrument: Instrument, branch: FlowBranch) -> None:
    """
    Dry column.

    args:
        branch: FlowBranch to dry.
    """
    logging.debug("Initiating drying of branch %s", branch)
    if branch == FlowBranch.REACTION:
        instrument.all_except(["gas", "rxn_out", "branch", "waste_rxn"])
    elif branch == FlowBranch.REAGENTS:
        instrument.all_except(["gas", "reagents", "waste"])
    logging.debug("Drying of branch %s complete", branch)


def dry_all(instrument: Instrument) -> None:
    """
    Dry all flow branches.
    """

    for branch in FlowBranch:
        dry(instrument, branch)
