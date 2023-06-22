from unittest import TestCase
from unittest.mock import Mock, mock_open, patch

from openoligo.driver.gpio import (Board, GPIOInterface, GpioMode, MockGPIO,
                                   RPiGPIO, get_gpio, is_rpi)
from openoligo.driver.rpi_pins import RPi


def test_get_gpio():
    gpio = get_gpio()
    assert isinstance(gpio, GPIOInterface)


def test_is_rpi():
    assert isinstance(is_rpi(), bool)


def test_mode():
    assert GpioMode.IN.value == 0
    assert GpioMode.OUT.value == 1


def test_mock_gpio():
    gpio = MockGPIO()
    assert isinstance(gpio, GPIOInterface)
    assert isinstance(gpio, MockGPIO)
    assert gpio.state == {}

    gpio.setup(1, GpioMode.OUT)
    assert gpio.state == {1: False}

    gpio.output(1, True)
    assert gpio.state == {1: True}

    gpio.cleanup()
    assert gpio.state == {}


class TestGetGpio(TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="Raspberry")
    def test_get_gpio_on_raspberry(self, mock_file):
        gpio = get_gpio()
        assert isinstance(gpio, GPIOInterface)


def test_RPiGPIO():
    gpio_mock = Mock()

    # Instantiate your class with the mock object
    rpi_gpio = RPiGPIO(gpio_mock)

    # Test setup method
    rpi_gpio.setup(5, GpioMode.OUT)
    gpio_mock.setmode.assert_called_once_with(gpio_mock.BOARD)
    gpio_mock.setup.assert_called_once_with(5, gpio_mock.OUT)

    gpio_mock.reset_mock()  # Reset mock call history

    # Test output method
    rpi_gpio.output(5, True)
    gpio_mock.output.assert_called_once_with(5, gpio_mock.HIGH)

    gpio_mock.reset_mock()  # Reset mock call history

    rpi_gpio.output(5, False)
    gpio_mock.output.assert_called_once_with(5, gpio_mock.LOW)

    # Test cleanup method
    rpi_gpio.cleanup()
    gpio_mock.cleanup.assert_called_once()


def test_Board():
    gpio_mock = Mock()

    # Instantiate your class with the mock object
    board = Board(gpio_mock)

    # Test setup method
    board.setup(GpioMode.OUT)
    assert gpio_mock.setup.call_count == len(RPi)  # Ensure setup was called for each pin
    for pin in RPi:
        gpio_mock.setup.assert_any_call(pin.value, GpioMode.OUT)

    gpio_mock.reset_mock()  # Reset mock call history

    # Test output method
    board.output(RPi.PIN3.value, True)
    gpio_mock.output.assert_called_once_with(RPi.PIN3.value, True)

    gpio_mock.reset_mock()  # Reset mock call history

    # Test cleanup method
    board.cleanup()
    gpio_mock.cleanup.assert_called_once()
