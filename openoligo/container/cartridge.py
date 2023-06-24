"""
Reagents and cartridges for the OpenOligo project.
"""
from types import SimpleNamespace

# from openoligo.fixed_keys_dict import FixedKeysDict
from openoligo.container.types import Reagent, ReagentCategory

reagents = SimpleNamespace(
    acetonitrile=Reagent(name="acetonitrile", accronym="ACN", category=ReagentCategory.SOLVENT),
    acetone=Reagent(name="acetone", accronym="ACET", category=ReagentCategory.SOLVENT),
)
