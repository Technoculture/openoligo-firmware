"""
Manifolds are a collection of valves.
"""
from dataclasses import dataclass, field
from typing import List, Type

from openoligo.driver.types import InvalidManifoldSizeError, Switchable


@dataclass
class SwitchSet:
    """
    This class represents a set of switches.
    The switches are created at initialization based on the provided size.
    """

    VALID_SIZES = {4, 8, 10, 16, 20}

    switch_type: Type[Switchable]
    size: int
    switches: List[Switchable] = field(init=False)

    def __post_init__(self):
        if self.size not in self.VALID_SIZES:
            raise InvalidManifoldSizeError(
                f"Invalid switch size: {self.size}. Must be one of {self.VALID_SIZES}"
            )
        self.switches = [self.switch_type(i, f"Switch {i}") for i in range(self.size)]

    async def set(self, index: int, state: bool):
        """Set state of the switch at a given index ON or OFF."""
        if index < 0 or index >= self.size:
            raise ValueError(f"Index out of range: {index}")
        await self.switches[index].set(state)

    def value(self, index: int) -> bool:
        """Get the current value of the switch at a given index."""
        if index < 0 or index >= self.size:
            raise ValueError(f"Index out of range: {index}")
        return self.switches[index].value
