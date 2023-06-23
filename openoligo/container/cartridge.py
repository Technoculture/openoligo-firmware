"""
Reagents and cartridges for the OpenOligo project.
"""
from types import SimpleNamespace

from openoligo.container.types import Bottle, Reagent, ReagentCategory, ReagentType

reagents = SimpleNamespace(
    acetonitrile=Reagent(
        name="acetonitrile", type=ReagentType.LIQUID, category=ReagentCategory.SOLVENT
    ),
    acetone=Reagent(name="acetone", type=ReagentType.LIQUID, category=ReagentCategory.SOLVENT),
)


dna_cartridge = SimpleNamespace(
    atgc=SimpleNamespace(
        a1=Bottle(
            reagent=reagents.acetonitrile, manufacturing_date="2020-01-01", expiry_date="2020-01-01"
        )
    ),
    methylated=SimpleNamespace(
        a1=Bottle(
            reagent=reagents.acetonitrile, manufacturing_date="2020-01-01", expiry_date="2020-01-01"
        )
    ),
    azide=SimpleNamespace(
        a1=Bottle(
            reagent=reagents.acetonitrile, manufacturing_date="2020-01-01", expiry_date="2020-01-01"
        )
    ),
)


rna_cartridge = SimpleNamespace(
    augc=SimpleNamespace(
        a1=Bottle(
            reagent=reagents.acetonitrile, manufacturing_date="2020-01-01", expiry_date="2020-01-01"
        ),
    ),
    methylated=SimpleNamespace(
        a1=Bottle(
            reagent=reagents.acetonitrile, manufacturing_date="2020-01-01", expiry_date="2020-01-01"
        ),
    ),
)
