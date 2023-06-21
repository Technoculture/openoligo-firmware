from openoligo.container.cartridge import dna_cartridge, reagents
from openoligo.container.types import (Reagent, ReagentCategory, ReagentType,
                                       Slot)


def test_reagents():
    for reagent_name, reagent in reagents.__dict__.items():
        assert isinstance(reagent_name, str)
        assert isinstance(reagent, Reagent)
        assert reagent.name == reagent_name
        assert isinstance(reagent.type, ReagentType)
        assert isinstance(reagent.category, ReagentCategory)


def test_cartridge_slots():
    for slot_name, slot in dna_cartridge.__dict__.items():
        assert isinstance(slot_name, str)
        assert isinstance(slot, Slot)
        assert slot.slot_id.value == slot_name
        assert isinstance(slot.reagent, Reagent)
        assert isinstance(slot.associated_valve, int)
