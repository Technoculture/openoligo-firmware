"""
GPIO access abstraction: RPi.GPIO on Raspberry Pi, MockGPIO otherwise.
"""
import importlib
import logging
from abc import ABC, abstractmethod

from openoligo.hal.types import Board, GpioMode, is_rpi


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


class GPIOInterface(ABC):
    """GPIO interface."""

    @abstractmethod
    def setup(self) -> None:
        """Setup GPIO."""

    @abstractmethod
    def setup_pin(self, pin: Board, mode: GpioMode) -> None:
        """Set up a GPIO pin."""

    @abstractmethod
    def set(self, pin: Board, value: bool) -> None:
        """Set the output value of a GPIO pin."""
        logging.debug("Setting pin %s to %s", pin, value)

    @abstractmethod
    def value(self, pin: Board) -> bool:
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
        """Import Board.GPIO"""
        self.gpio = gpio
        self.gpio.setmode(self.gpio.BOARD)
        self.gpio.setwarnings(False)

    def setup(self):
        """Set up all pins."""
        for pin in Board:
            self.setup_pin(pin)

    def setup_pin(self, pin: Board, mode: GpioMode = GpioMode.OUT) -> None:
        """Set up a GPIO pin."""
        self.gpio.setup(pin.value, self.gpio.OUT if mode == GpioMode.OUT else self.gpio.IN)

    def set(self, pin: Board, value: bool) -> None:
        """Set the output value of a GPIO pin."""
        super().set(pin, value)
        self.gpio.output(pin.value, self.gpio.HIGH if value else self.gpio.LOW)

    def value(self, pin: Board) -> bool:
        return self.gpio.input(pin.value)

    def cleanup(self):
        """Clean up GPIO."""
        self.gpio.cleanup()

    def __repr__(self) -> str:
        """Return a string representation of the GPIO module."""
        return ", ".join(f"({pin.value}, {1 if self.value(pin) else 0})" for pin in Board)


class MockGPIO(GPIOInterface):
    """Mock GPIO access."""

    def __init__(self):
        """
        Initialize the state. Its keys are the pin numbers,
        and the values are their mock states
        """
        self.state: dict[int, bool] = {}

    def setup(self) -> None:
        """Setup all pins."""
        for pin in Board:
            self.setup_pin(pin)

    def setup_pin(
        self, pin: Board, mode: GpioMode = GpioMode.OUT
    ) -> None:  # pylint: disable=unused-argument
        """Set up a GPIO pin."""
        self.state[pin.value] = False

    def set(self, pin: Board, value: bool):
        """Set the output value of a GPIO pin."""
        super().set(pin, value)
        self.state[pin.value] = value

    def value(self, pin: Board) -> bool:
        """Get the value of a GPIO pin."""
        return self.state[pin.value]

    def cleanup(self):
        """Clean up GPIO."""
        for pin in Board:
            self.set(pin, False)

    def __repr__(self) -> str:
        """Return a string representation of the GPIO module."""
        return ", ".join(f"({pin.value}, {1 if self.value(pin) else 0})" for pin in Board)
