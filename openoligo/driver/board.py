"""
GPIO access abstraction: RPi.GPIO on Raspberry Pi, MockGPIO otherwise.
"""
import logging
import importlib
from abc import ABC, abstractmethod
from typing import Optional, Type
from types import TracebackType

from openoligo.driver.rpi_pins import RPi
from openoligo.driver.types import GpioMode


def get_gpio():
    """Get the GPIO module."""
    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8") as file:
            if "Raspberry" in file.read():
                gpio = importlib.import_module("RPi.GPIO")
                return RPiGPIO(gpio)
            return MockGPIO()
    except (FileNotFoundError, ModuleNotFoundError):
        return MockGPIO()


def is_rpi() -> bool:
    """Returns True if running on a Raspberry Pi, False otherwise."""
    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8") as file:
            return "Raspberry" in file.read()
    except FileNotFoundError:
        return False


class GPIOInterface(ABC):
    """GPIO interface."""

    @abstractmethod
    def setup(self, pin: RPi, mode: GpioMode) -> None:
        """Set up a GPIO pin."""

    @abstractmethod
    def set(self, pin: RPi, value: bool) -> None:
        """Set the output value of a GPIO pin."""
        logging.debug("Setting pin %s to %s", pin, value)

    @abstractmethod
    def value(self, pin: RPi) -> bool:
        """Get the value of a GPIO pin."""

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up GPIO."""

    @abstractmethod
    def __repr__(self) -> str:
        """Return a string representation of the GPIO module."""


class RPiGPIO(GPIOInterface):
    """GPIO access on Raspberry Pi."""

    def __init__(self, gpio):
        """Import RPi.GPIO"""
        self.gpio = gpio

    def setup(self, pin: RPi, mode: GpioMode = GpioMode.OUT) -> None:
        """Set up a GPIO pin."""
        self.gpio.setmode(self.gpio.BOARD)
        self.gpio.setup(pin.value, self.gpio.OUT if mode == GpioMode.OUT else self.gpio.IN)

    def set(self, pin: RPi, value: bool) -> None:
        """Set the output value of a GPIO pin."""
        super().set(pin, value)
        self.gpio.output(pin.value, self.gpio.HIGH if value else self.gpio.LOW)

    def value(self, pin: RPi) -> bool:
        return self.gpio.input(pin.value)

    def cleanup(self):
        """Clean up GPIO."""
        self.gpio.cleanup()

    def __repr__(self) -> str:
        """Return a string representation of the GPIO module."""
        return ", ".join(f"({pin.value}, {1 if self.value(pin) else 0})" for pin in RPi)


class MockGPIO(GPIOInterface):
    """Mock GPIO access."""

    def __init__(self):
        """
        Initialize the state. Its keys are the pin numbers,
        and the values are their mock states
        """
        self.state: dict[int, bool] = {}
        for pin in RPi:
            self.setup(pin)

    def setup(
        self, pin: RPi, mode: GpioMode = GpioMode.OUT
    ) -> None:  # pylint: disable=unused-argument
        """Set up a GPIO pin."""
        self.state[pin.value] = False

    def set(self, pin: RPi, value: bool):
        """Set the output value of a GPIO pin."""
        super().set(pin, value)
        self.state[pin.value] = value

    def value(self, pin: RPi) -> bool:
        """Get the value of a GPIO pin."""
        return self.state[pin.value]

    def cleanup(self):
        """Clean up GPIO."""
        for pin in RPi:
            self.set(pin, False)

    def __repr__(self) -> str:
        """Return a string representation of the GPIO module."""
        return ", ".join(f"({pin.value}, {1 if self.value(pin) else 0})" for pin in RPi)


class Board:
    """
    Board abstraction: Collection of GPIO pins found in a Raspberry Pi.
    All pins are set to output mode by default.
    """

    __version__ = "0.1.0"

    def __init__(self, mode: GpioMode = GpioMode.OUT):
        """Initialize the board."""
        self.gpio = get_gpio()
        self.gpio_type = type(self.gpio)
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
