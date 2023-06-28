"""
Functions to create various flows from reagents to columns,
and to clean columns.
"""
import logging

from openoligo import Instrument
from openoligo.steps.types import FlowBranch, substep
from openoligo.utils.wait import wait_async


@substep
async def send_to_prod(instrument: Instrument, src: str) -> None:
    """
    Flow a reagent to the final product outlet.

    args:
        src: Slot to flow reagents from.
    """
    instrument.all_except([src, "prod", "branch", "rxn_out"])
    logging.debug("Flowing %s to prod", src)


@substep
async def send_to_waste_rxn(instrument: Instrument, src: str) -> None:
    """
    Flow a reagent to the final product outlet.

    args:
        src: Slot to flow reagents from.
    """
    instrument.all_except([src, "branch", "rxn_out", "waste_rxn"])
    logging.debug("Flowing %s to reaction waste", src)


@substep
async def solvent_wash(instrument: Instrument, branch: FlowBranch, duration: float = 10) -> None:
    """
    Wash column with solvent.

    args:
        branch: FlowBranch to wash.
    """
    logging.debug("Initiating washing flow branch %s with solvent", branch)

    if branch == FlowBranch.REACTION:
        instrument.all_except(["sol", "rxn_out", "branch", "waste_rxn"])
    elif branch == FlowBranch.REAGENTS:
        instrument.all_except(["sol", "waste"])

    await wait_async(duration)

    logging.debug("Washing of branch %s complete", branch)


@substep
async def solvent_wash_all(instrument: Instrument) -> None:
    """
    Wash all flow branches with solvent.
    """

    await solvent_wash(instrument, FlowBranch.REACTION)
    await solvent_wash(instrument, FlowBranch.REAGENTS)


@substep
async def dry(instrument: Instrument, branch: FlowBranch) -> None:
    """
    Dry column.

    args:
        branch: FlowBranch to dry.
    """
    logging.debug("Initiating drying of branch %s", branch)
    if branch == FlowBranch.REACTION:
        instrument.all_except(["gas", "rxn_out", "branch", "waste_rxn"])
    elif branch == FlowBranch.REAGENTS:
        instrument.all_except(["gas", "waste"])
    logging.debug("Drying of branch %s complete", branch)


@substep
async def dry_all(instrument: Instrument) -> None:
    """
    Dry all flow branches.
    """

    await dry(instrument, FlowBranch.REACTION)
    await dry(instrument, FlowBranch.REAGENTS)
