"""
GPIO access abstraction: RPi.GPIO on Raspberry Pi, MockGPIO otherwise.
"""
import importlib
from abc import ABC, abstractmethod

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
    def setup(self, pin: int, mode: GpioMode) -> None:
        """Set up a GPIO pin."""

    @abstractmethod
    def output(self, pin: int, value: bool) -> None:
        """Set the output value of a GPIO pin."""

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up GPIO."""


class RPiGPIO(GPIOInterface):
    """GPIO access on Raspberry Pi."""

    def __init__(self, gpio):
        """Import RPi.GPIO"""
        self.gpio = gpio

    def setup(self, pin: int, mode: GpioMode = GpioMode.OUT) -> None:
        """Set up a GPIO pin."""
        self.gpio.setmode(self.gpio.BOARD)
        self.gpio.setup(pin, self.gpio.OUT if mode == GpioMode.OUT else self.gpio.IN)

    def output(self, pin: int, value: bool) -> None:
        """Set the output value of a GPIO pin."""
        self.gpio.output(pin, self.gpio.HIGH if value else self.gpio.LOW)

    def cleanup(self):
        """Clean up GPIO."""
        self.gpio.cleanup()


class MockGPIO(GPIOInterface):
    """Mock GPIO access."""

    def __init__(self):
        """
        Initialize the state. Its keys are the pin numbers,
        and the values are their mock states
        """
        self.state = {}

    def setup(self, pin: int, mode: GpioMode):
        """Set up a GPIO pin."""
        self.state[pin] = False

    def output(self, pin: int, value: bool):
        """Set the output value of a GPIO pin."""
        self.state[pin] = value

    def cleanup(self):
        """Clean up GPIO."""
        self.state.clear()


class Board:
    """Board abstraction."""

    def __init__(self, gpio: GPIOInterface):
        """Initialize the board."""
        self.gpio = gpio

    def setup(self, mode: GpioMode):
        """Set up a GPIO pin."""
        for pin in RPi:
            self.gpio.setup(pin.value, mode)

    def output(self, pin: int, value: bool):
        """Set the output value of a GPIO pin."""
        self.gpio.output(pin, value)

    def cleanup(self):
        """Clean up GPIO."""
        self.gpio.cleanup()
