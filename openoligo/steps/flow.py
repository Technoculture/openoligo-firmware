"""
Functions to create various flows from reagents to columns,
and to clean columns.
"""
import logging
from openoligo.container.types import Slot
from openoligo.steps.types import FlowBranch


def send(src: Slot, dest: Slot) -> None:
    """
    Flow reagents to column.

    args:
        src: Slot to flow reagents from.
        dest: Slot to flow reagents to.

    return: None
    """
    logging.debug("Flowing reagents from %s to %s", src, dest)


def send_to_reactor(src: Slot) -> None:
    """
    Flow a reagent to the reactor.

    args:
        src: Slot to flow reagents from.

    return: None
    """
    logging.debug("Flowing reagents from %s to reactor", src)


def solvent_wash(branch: FlowBranch) -> None:
    """
    Wash column with solvent.

    args:
        branch: FlowBranch to wash.

    return: None
    """
    logging.debug("Washing flow branch %s with solvent", branch)


def solvent_wash_all() -> None:
    """
    Wash all flow branches with solvent.
    """

    for branch in FlowBranch:
        solvent_wash(branch)


def dry(branch: FlowBranch) -> None:
    """
    Dry column.

    args:
        branch: FlowBranch to dry.

    return: None
    """
    logging.debug("Drying flow branch %s", branch)


def dry_all() -> None:
    """
    Dry all flow branches.
    """

    for branch in FlowBranch:
        dry(branch)
