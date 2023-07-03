"""
Functions to create various flows from reagents to columns,
and to clean columns.
"""
from openoligo.hal.instrument import Instrument
from openoligo.steps.types import FlowBranch, substep
from openoligo.utils.logger import configure_logger
from openoligo.utils.wait import wait_async

logger = configure_logger()


@substep
async def send_to_prod(instrument: Instrument, src: str) -> None:
    """
    Flow a reagent to the final product outlet.

    args:
        src: Slot to flow reagents from.
    """
    instrument.all_except([src, "prod", "branch", "rxn_out"])
    logger.debug("Flowing %s to prod", src)


@substep
async def send_to_waste_rxn(instrument: Instrument, src: str) -> None:
    """
    Flow a reagent to the final product outlet.

    args:
        src: Slot to flow reagents from.
    """
    instrument.all_except([src, "branch", "rxn_out", "waste_rxn"])
    logger.debug("Flowing %s to reaction waste", src)


@substep
async def solvent_wash(instrument: Instrument, branch: FlowBranch, duration: float = 10) -> None:
    """
    Wash column with solvent.

    args:
        branch: FlowBranch to wash.
    """
    logger.debug("Initiating washing flow branch %s with solvent", branch)

    if branch == FlowBranch.REACTION:
        instrument.all_except(["sol", "rxn_out", "branch", "waste_rxn"])
    elif branch == FlowBranch.REAGENTS:
        instrument.all_except(["sol", "waste"])

    await wait_async(duration)

    logger.debug("Washing of branch %s complete", branch)


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
    logger.debug("Initiating drying of branch %s", branch)
    if branch == FlowBranch.REACTION:
        instrument.all_except(["gas", "rxn_out", "branch", "waste_rxn"])
    elif branch == FlowBranch.REAGENTS:
        instrument.all_except(["gas", "waste"])
    logger.debug("Drying of branch %s complete", branch)


@substep
async def dry_all(instrument: Instrument) -> None:
    """
    Dry all flow branches.
    """

    await dry(instrument, FlowBranch.REACTION)
    await dry(instrument, FlowBranch.REAGENTS)
