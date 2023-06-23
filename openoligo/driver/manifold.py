"""
Manifolds are a collection of valves.
"""
from dataclasses import dataclass, field
from typing import Generic, List, Type, TypeVar

from openoligo.driver.switch import toggle
from openoligo.driver.types import InvalidManifoldSizeError, Valvable, ValveType

T = TypeVar("T", bound=Valvable)


@dataclass
class Manifold(Generic[T]):
    """
    This class represents a set of switches.
    The switches are created at initialization based on the provided size.
    """

    VALID_SIZES = {4, 8, 10, 16, 20}

    valve_class: Type[T]
    size: int
    manifold_type: ValveType = ValveType.NORMALLY_OPEN
    valves: List[T] = field(init=False)

    def __post_init__(self):
        if self.size not in self.VALID_SIZES:
            raise InvalidManifoldSizeError(
                f"Invalid switch size: {self.size}. Must be one of {self.VALID_SIZES}"
            )
        self.valves = [
            self.valve_class(i, f"Valve {i}", self.manifold_type) for i in range(self.size)
        ]

    def set(self, index: int, state: bool):
        """Set state of the switch at a given index ON or OFF."""
        if index < 0 or index >= self.size:
            raise ValueError(f"Index out of range: {index}")
        self.valves[index].set(state)

    def value(self, index: int) -> bool:
        """Get the current value of the switch at a given index."""
        try:
            return self.valves[index].value
        except IndexError as exc:
            raise ValueError(f"Index out of range: {index}") from exc

    def all(self, state: bool):
        """Set the state of a list of switches."""
        for valve in self.valves:
            valve.set(state)

    def toggle(self):
        """Toggle the state of a list of switches."""
        for valve in self.valves:
            toggle(valve)

    def activate_flow(self, index: int):
        """Set state for the index to ON and all others to OFF"""
        self.activate_n_flows([index])

    def activate_n_flows(self, indices: List[int]):
        """Set state for the indices to ON and all others to OFF"""
        for i in indices:
            if i < 0 or i >= self.size:
                raise ValueError(f"Index out of range: {i}")
        for i in range(self.size):
            self.set(i, i in indices)
