"""
Reagents and cartridges for the OpenOligo project.
"""
from types import SimpleNamespace

from openoligo.container.types import (Reagent, ReagentCategory, ReagentType,
                                       Slot, SlotID)

reagents = SimpleNamespace(
    acetonitrile=Reagent(
        name="acetonitrile", type=ReagentType.LIQUID, category=ReagentCategory.SOLVENT
    ),
)


dna_cartridge = SimpleNamespace(
    a1=Slot(slot_id=SlotID.A1, reagent=reagents.acetonitrile, associated_valve=1),
    a2=Slot(slot_id=SlotID.A2, reagent=reagents.acetonitrile, associated_valve=2),
)
