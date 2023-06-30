"""
GPIO access abstraction: RPi.GPIO on Raspberry Pi, MockGPIO otherwise.
"""
import importlib
import logging
from abc import ABC, abstractmethod

from openoligo.hal.platform import Platform, __platform__
from openoligo.hal.types import GpioMode, board


def get_gpio():
    """Get the GPIO module."""
    if __platform__ == Platform.BB:
        return MockGPIO()
    if __platform__ == Platform.RPI:
        gpio = importlib.import_module("RPi.GPIO")
        return RPiGPIO(gpio)
    return MockGPIO()


class GPIOInterface(ABC):
    """GPIO interface."""

    @abstractmethod
    def setup_pin(self, pin: str, mode: GpioMode) -> None:
        """Set up a GPIO pin."""

    @abstractmethod
    def set(self, pin: str, value: bool) -> None:
        """Set the output value of a GPIO pin."""
        logging.debug("Setting pin %s to %s", pin, value)

    @abstractmethod
    def value(self, pin: str) -> bool:
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
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setwarnings(False)

    def setup_pin(self, pin: str, mode: GpioMode = GpioMode.OUT) -> None:
        """Set up a GPIO pin."""
        self.gpio.setup(pin, self.gpio.OUT if mode == GpioMode.OUT else self.gpio.IN)

    def set(self, pin: str, value: bool) -> None:
        """Set the output value of a GPIO pin."""
        super().set(pin, value)
        self.gpio.output(pin, self.gpio.HIGH if value else self.gpio.LOW)

    def value(self, pin: str) -> bool:
        return self.gpio.input(pin)

    def cleanup(self):
        """Clean up GPIO."""
        self.gpio.cleanup()

    def __repr__(self) -> str:
        """Return a string representation of the GPIO module."""
        return ", ".join(f"({pin}, {1 if self.value(pin) else 0})" for pin in board)


class MockGPIO(GPIOInterface):
    """Mock GPIO access."""

    def __init__(self):
        """
        Initialize the state. Its keys are the pin numbers,
        and the values are their mock states
        """
        self.state: dict[str, bool] = {}

    def setup_pin(
        self, pin: str, mode: GpioMode = GpioMode.OUT
    ) -> None:  # pylint: disable=unused-argument
        """Set up a GPIO pin."""
        self.state[pin] = False

    def set(self, pin: str, value: bool):
        """Set the output value of a GPIO pin."""
        super().set(pin, value)
        self.state[pin] = value

    def value(self, pin: str) -> bool:
        """Get the value of a GPIO pin."""
        return self.state[pin]

    def cleanup(self):
        """Clean up GPIO."""
        for pin in board:
            self.set(pin, False)

    def __repr__(self) -> str:
        """Return a string representation of the GPIO module."""
        return ", ".join(f"({pin}, {1 if self.value(pin) else 0})" for pin in board)
