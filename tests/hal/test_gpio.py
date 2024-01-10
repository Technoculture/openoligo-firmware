# from unittest import TestCase
from unittest.mock import Mock, mock_open, patch

import pytest

from openoligo.hal.gpio import GPIOInterface, GpioMode, MockGPIO, RPiGPIO, get_gpio
from openoligo.hal.platform import is_rpi
from openoligo.hal.types import board


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
    assert isinstance(gpio, GPIOInterface), "MockGPIO should be a GPIOInterface"
    # assert gpio.state == {(pin): False for pin in board}

    gpio.set(board.P21, True)
    _d = {pin: False for pin, _ in board if pin != board.P21}
    _d["P21"] = True
    assert gpio.state == _d

    gpio.set(board.P22, True)
    gpio.set(board.P40, True)

    assert (
        gpio.__repr__()
        == "{'P3': False, 'P5': False, 'P7': False, 'P8': False, 'P10': False, 'P11': False, 'P12': False, 'P13': False, 'P15': False, 'P16': False, 'P18': False, 'P19': False, 'P21': True, 'P22': True, 'P23': False, 'P24': False, 'P26': False, 'P27': False, 'P28': False, 'P29': False, 'P31': False, 'P32': False, 'P33': False, 'P35': False, 'P36': False, 'P37': False, 'P38': False, 'P40': True}"  # noqa: E501
    ), "repr should return all pin states in (pin_number, 0 or 1) format"  # noqa: E501

    gpio.cleanup()
    assert gpio.state == {(pin): False for pin, _ in board}


def test_RPiGPIO():
    gpio_mock = Mock()

    # Instantiate your class with the mock object
    rpi_gpio = RPiGPIO(gpio_mock)

    # Test setup method
    gpio_mock.setmode.assert_called_once_with(gpio_mock.BCM)

    gpio_mock.reset_mock()  # Reset mock call history

    # Test output method
    rpi_gpio.set(board.P5, True)
    gpio_mock.output.assert_called_once_with(5, gpio_mock.HIGH)

    gpio_mock.reset_mock()  # Reset mock call history

    rpi_gpio.set(board.P5, False)
    gpio_mock.output.assert_called_once_with(5, gpio_mock.LOW)

    # Test cleanup method
    rpi_gpio.cleanup()
    gpio_mock.cleanup.assert_called_once()


@pytest.fixture
def mock_file():
    with patch(
        "builtins.open", new_callable=mock_open, read_data="Not a Raspberry Pi"
    ) as mock_file:
        yield mock_file


def test_not_on_raspberry_pi(mock_file):
    """Test that MockGPIO is returned when not running on a Raspberry Pi."""
    result = get_gpio()
    # Check that the right GPIO class was returned
    assert isinstance(result, MockGPIO)
