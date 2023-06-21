from openoligo.driver.gpio import (GPIOInterface, MockGPIO, Mode, get_gpio,
                                   is_rpi)


def test_get_gpio():
    gpio = get_gpio()
    assert isinstance(gpio, GPIOInterface)


def test_is_rpi():
    assert isinstance(is_rpi(), bool)


def test_mode():
    assert Mode.IN.value == 0
    assert Mode.OUT.value == 1


def test_mock_gpio():
    gpio = MockGPIO()
    assert isinstance(gpio, GPIOInterface)
    assert isinstance(gpio, MockGPIO)
    assert gpio.state == {}

    gpio.setup(1, Mode.OUT)
    assert gpio.state == {1: False}

    gpio.output(1, True)
    assert gpio.state == {1: True}

    gpio.cleanup()
    assert gpio.state == {}
