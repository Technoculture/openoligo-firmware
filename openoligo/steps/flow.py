"""
Functions to create various flows from reagents to columns,
and to clean columns.
"""
import logging
from openoligo.container.types import Slot
from openoligo.steps.types import FlowBranch, Output

import functools
import logging
from typing import Optional


def step(coroutine):
    @functools.wraps(coroutine)
    async def wrapper(*args, **kwargs):
        doc = coroutine.__doc__.strip()
        name= coroutine.__name__
        if doc:
            logging.info("%s: %s", name, doc)
        return await coroutine(*args, **kwargs)
    return wrapper


def which_branch(dst: Output) -> FlowBranch:
    """
    Determine which flow branch to use.

    args:
        dst: Output to flow reagents to.

    return: FlowBranch
    """
    if dst is Output.OUTPUT:
        return FlowBranch.REACTION
    elif dst is Output.WASTE1:
        return FlowBranch.REACTION
    elif dst is Output.WASTE2:
        return FlowBranch.REAGENTS


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
