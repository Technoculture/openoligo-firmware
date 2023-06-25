from openoligo.driver.pins import RPi
from openoligo.driver.types import GpioMode

from openoligo.driver.gpio import get_gpio


class Board:
    """
    Board abstraction: Collection of GPIO pins found in a Raspberry Pi.
    All pins are set to output mode by default.
    """

    __version__ = "0.1.0"

    def __init__(self):
        """Initialize the board."""
        self.gpio = get_gpio()
        self.gpio_type = type(self.gpio)

    def setup(self, mode: GpioMode = GpioMode.OUT):
        """Set up the board."""
        for pin in RPi:
            self.gpio.setup(pin, mode)

    def __enter__(self):
        """Enter the runtime context related to this object."""
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit the runtime context related to this object."""
        self.gpio.cleanup()

    def set(self, pin: RPi, value: bool = True) -> None:
        """Set the output value of a GPIO pin."""
        self.gpio.set(pin, value)

    def value(self, pin: RPi) -> bool:
        """Get the value of a pin."""
        return self.gpio.value(pin)

    def __repr__(self) -> str:
        """String representation for the board type"""
        return f"Board<{self.gpio_type}>[{self.gpio}]"
