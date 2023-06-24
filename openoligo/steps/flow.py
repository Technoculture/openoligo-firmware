"""
Functions to create various flows from reagents to columns,
and to clean columns.
"""
import logging
from openoligo.container.types import Slot

# from openoligo.steps.types import FlowBranch


def send(src: Slot, dest: Slot) -> None:
    """
    Flow reagents to column.

    :param from: Slot to flow reagents from.
    :param to: Slot to flow reagents to.
    :return: None
    """
    logging.info("Flowing reagents from %s to %s", src, dest)


def solvent_wash(slot: Slot) -> None:
    """
    Wash column with solvent.

    :param slot: Slot to wash.
    :return: None
    """
    logging.info("Washing column in %s with solvent", slot)


def dry() -> None:
    """
    Dry column.

    :return: None
    """
    logging.info("Drying column")


def clean() -> None:
    """
    Clean column.

    :return: None
    """
    # solvent_wash(Slot.SOL)
    dry()
