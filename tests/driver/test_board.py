import unittest

# from unittest import TestCase
from unittest.mock import Mock, mock_open, patch


from openoligo.driver.board import (
    Board,
    GPIOInterface,
    GpioMode,
    MockGPIO,
    RPiGPIO,
    get_gpio,
    is_rpi,
)
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
    assert gpio.state == {(pin.value): False for pin in RPi}

    gpio.set(RPi.PIN21, True)

    _d = {(pin.value): False for pin in RPi if pin != RPi.PIN21}
    _d[RPi.PIN21.value] = True
    assert gpio.state == _d

    gpio.set(RPi.PIN22, True)
    gpio.setup(RPi.PIN21, GpioMode.OUT)

    assert (
        gpio.__repr__()
        == "(3, 0), (5, 0), (7, 0), (8, 0), (10, 0), (11, 0), (12, 0), (13, 0), (15, 0), (16, 0), (18, 0), (19, 0), (21, 0), (22, 1), (23, 0), (24, 0), (26, 0), (27, 0), (28, 0), (29, 0), (31, 0), (32, 0), (33, 0), (35, 0), (36, 0), (37, 0), (38, 0), (40, 0)"  # noqa: E501
    ), "repr should return all pin states in (pin_number, 0 or 1) format"  # noqa: E501

    gpio.cleanup()
    assert gpio.state == {(pin.value): False for pin in RPi}


def test_RPiGPIO():
    gpio_mock = Mock()

    # Instantiate your class with the mock object
    rpi_gpio = RPiGPIO(gpio_mock)

    # Test setup method
    rpi_gpio.setup(RPi.PIN5, GpioMode.OUT)
    gpio_mock.setmode.assert_called_once_with(gpio_mock.BOARD)
    gpio_mock.setup.assert_called_once_with(5, gpio_mock.OUT)

    gpio_mock.reset_mock()  # Reset mock call history

    # Test output method
    rpi_gpio.set(RPi.PIN5, True)
    gpio_mock.output.assert_called_once_with(5, gpio_mock.HIGH)

    gpio_mock.reset_mock()  # Reset mock call history

    rpi_gpio.set(RPi.PIN5, False)
    gpio_mock.output.assert_called_once_with(5, gpio_mock.LOW)

    # Test cleanup method
    rpi_gpio.cleanup()
    gpio_mock.cleanup.assert_called_once()


class TestGetGpio(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="Not a Raspberry Pi")
    def test_not_on_raspberry_pi(self, mock_file):
        """Test that MockGPIO is returned when not running on a Raspberry Pi."""

        result = get_gpio()
        # Check that the right GPIO class was returned
        self.assertIsInstance(result, MockGPIO)


# class TestRPiGpio(unittest.TestCase):
#    def setUp(self):
#        self.gpio = MockGPIO()
#        self.rpi_gpio = RPiGPIO(self.gpio)
#
#    def test_setup(self):
#        self.rpi_gpio.setup(RPi.PIN3, GpioMode.OUT)
#        self.rpi_gpio.setmode.assert_called_with(self.rpi_gpio.BOARD)
#        self.gpio.setup.assert_called_with(RPi.PIN3.value, self.gpio.OUT)
#
#    def test_set(self):
#        self.rpi_gpio.set(RPi.PIN3, True)
#        self.gpio.output.assert_called_with(RPi.PIN3.value, self.gpio.HIGH)
#
#    def test_value(self):
#        self.gpio.input.return_value = True
#        self.assertEqual(self.rpi_gpio.value(RPi.PIN3), True)
#
#    def test_cleanup(self):
#        self.rpi_gpio.cleanup()
#        self.gpio.cleanup.assert_called()
#
#    def test_repr(self):
#        self.rpi_gpio.value = MagicMock()
#        self.rpi_gpio.value.side_effect = [True, False, True]
#        self.assertEqual(self.rpi_gpio.__repr__(), "(1, 1), (2, 0), (3, 1)")


def test_board():
    with Board() as board:
        board.set(RPi.PIN31, True)
        assert board.value(RPi.PIN31)
        board.set(RPi.PIN40, True)
        board.set(RPi.PIN31, False)
        assert not board.value(RPi.PIN31)

        assert (
            board.__repr__()
            == "Board<<class 'openoligo.driver.board.MockGPIO'>>[(3, 0), (5, 0), (7, 0), (8, 0), (10, 0), (11, 0), (12, 0), (13, 0), (15, 0), (16, 0), (18, 0), (19, 0), (21, 0), (22, 0), (23, 0), (24, 0), (26, 0), (27, 0), (28, 0), (29, 0), (31, 0), (32, 0), (33, 0), (35, 0), (36, 0), (37, 0), (38, 0), (40, 1)]"  # noqa: E501
        ), "board repr should return all pin states in (pin_number, 0 or 1) format"  # noqa: E501
