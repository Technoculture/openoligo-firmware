from typing import Protocol


class Switchable(Protocol):
    def set(self, switch: bool):
        """Set the state of the switch."""
        ...

    def value(self) -> bool:
        """Get the current value of the switch."""
        ...

    def toggle(self):
        """Toggle the state of the switch."""
        ...
