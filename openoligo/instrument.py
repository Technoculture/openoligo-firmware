"""
Unified access to configuring and using the instrument.
"""
from openoligo.hal.board import Pinout
from openoligo.hal.gpio import get_gpio
from openoligo.utils.singleton import Singleton


class Instrument(metaclass=Singleton):
    """
    Unified access to the instrument. Hide the details of the hardware.
    """

    def __init__(self, pinout: Pinout) -> None:
        """
        Initialize the instrument.
        """
        self.pinout = pinout
        self.__setup()

    def __setup(self):
        """
        Setup the instrument.
        """
        self.__gpio = get_gpio()
        self.__gpio.setup()

    def start_reaction(self):
        print("Starting reaction")

    def stop_reaction(self):
        print("Stopping reaction")

    def __repr__(self):
        """
        Return a string representation of the instrument.
        """
        return f"Instrument({self.pinout})"
