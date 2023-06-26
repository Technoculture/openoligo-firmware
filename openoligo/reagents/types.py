"""
A cartridge is a container containing a set of different categories of reagents,
in 2 different sizes of bottles (small and large).
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ReagentCategory(str, Enum):
    """The category of reagent."""

    DETRITYLATION = "detritylation"
    ACTIVATION = "activation"
    COUPLING = "coupling"
    CAPPING = "capping"
    OXIDATION = "oxidation"
    DEPROTECTION = "deprotection"

    PHOSPHORAMIDITE = "phosphoramidite"
    SOLVENT = "solvent"
    GAS = "gas"


class BottleSlotID(Enum):
    """The ID of the bottle slot."""

    A1 = 1
    A2 = 2
    A3 = 3
    A4 = 4
    A5 = 5
    A6 = 6
    A7 = 7
    A8 = 8

    B1 = 9
    B2 = 10
    B3 = 11
    B4 = 12
    B5 = 13
    B6 = 14
    B7 = 15
    B8 = 16

    C1 = 17
    C2 = 18
    C3 = 19
    C4 = 20
    C5 = 21
    C6 = 22
    C7 = 23
    C8 = 24

    D1 = 25
    D2 = 26
    D3 = 27
    D4 = 28
    D5 = 29
    D6 = 30
    D7 = 31
    D8 = 32


@dataclass
class Slot:
    """A slot in the cartridge."""

    idn: BottleSlotID
    valve: int


valid_keys = {member.name for member in BottleSlotID}


@dataclass
class Reagent:
    """A reagent."""

    name: str
    accronym: str
    category: ReagentCategory


@dataclass
class Bottle:
    """A bottle containing a particular reagent."""

    reagent: str = ""
    slot: Optional[Slot] = None
