"""
GPIO access abstraction: RPi.GPIO on Raspberry Pi, MockGPIO otherwise.
"""
import importlib
from abc import ABC, abstractmethod
from typing import Callable

from openoligo.hal.platform import Platform, __platform__
from openoligo.hal.types import GpioEdge, GpioMode, board


def get_gpio():
    """Get the GPIO module."""
    if __platform__ == Platform.BB:
        gpio = importlib.import_module("Adafruit_BBIO.GPIO")
        return BbGPIO(gpio)
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

    @abstractmethod
    def value(self, pin: str) -> bool:
        """Get the value of a GPIO pin."""

    @abstractmethod
    def on_edge(self, pin: str, *, edge: GpioEdge, callback: Callable) -> None:
        """Set up a callback for a GPIO pin edge."""

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
        self.gpio.output(int(pin), self.gpio.HIGH if value else self.gpio.LOW)

    def value(self, pin: str) -> bool:
        """Get the value of a GPIO pin."""
        return self.gpio.input(pin)

    def on_edge(self, pin: str, *, edge: GpioEdge, callback: Callable) -> None:
        """Set up a callback for a GPIO pin edge."""
        self.gpio.add_event_detect(pin, edge)
        self.gpio.add_event_callback(pin, callback)

    def cleanup(self):
        """Clean up GPIO."""
        self.gpio.cleanup()

    def __repr__(self) -> str:
        """Return a string representation of the GPIO module."""
        return ", ".join(f"({pin}, {1 if self.value(pin) else 0})" for pin, _ in board)


class BbGPIO(GPIOInterface):
    """GPIO access on Beaglebone Black Board."""

    def __init__(self, gpio):
        """Import Adafruit_BBIO.GPIO"""
        self.gpio = gpio

    def setup_pin(self, pin: str, mode: GpioMode = GpioMode.OUT) -> None:
        """Set up a GPIO pin."""
        self.gpio.setup(pin, self.gpio.OUT if mode == GpioMode.OUT else self.gpio.IN)

    def set(self, pin: str, value: bool) -> None:
        """Set the output value of a GPIO pin."""
        self.gpio.output(
            pin, self.gpio.HIGH if value else self.gpio.LOW, pull_up_down=self.gpio.PUD_UP
        )

    def value(self, pin: str) -> bool:
        """Get the value of a GPIO pin."""
        return self.gpio.input(pin)

    def on_edge(self, pin: str, *, edge: GpioEdge, callback: Callable) -> None:
        """Set up a callback for a GPIO pin edge."""
        self.gpio.add_event_detect(pin, edge, callback=callback)

    def cleanup(self):
        """Clean up GPIO."""
        self.gpio.cleanup()

    def __repr__(self) -> str:
        """Return a string representation of the GPIO module."""
        return ", ".join(f"({pin}, {1 if self.value(pin) else 0})" for pin, _ in board)


class MockGPIO(GPIOInterface):
    """Mock GPIO access."""

    def __init__(self):
        """
        Initialize the state. Its keys are the pin numbers,
        and the values are their mock states
        """
        self.state: dict[str, bool] = {}
        for pin, _ in board:
            self.state[pin] = False

    def setup_pin(
        self, pin: str, _: GpioMode = GpioMode.OUT
    ) -> None:  # pylint: disable=unused-argument
        """Set up a GPIO pin."""
        self.state[pin] = False

    def set(self, pin: str, value: bool) -> None:
        """Set the output value of a GPIO pin."""
        if pin.startswith("P"):
            self.state[pin] = value
        else:
            self.state[f"P{pin}"] = value

    def value(self, pin: str) -> bool:
        """Get the value of a GPIO pin."""
        if pin.startswith("P"):
            return self.state[pin]
        return self.state[f"P{pin}"]

    def on_edge(self, pin: str, *, edge: GpioEdge, callback: Callable) -> None:
        """Set up a callback for a GPIO pin edge."""

    def cleanup(self):
        """Clean up GPIO."""
        for pin, _ in board:
            self.set(pin, False)

    def __repr__(self) -> str:
        """Return a string representation of the GPIO module."""
        # return ", ".join(f"({pin}, {self.value(pin)})" for pin, _ in board)
        return self.state.__repr__()
