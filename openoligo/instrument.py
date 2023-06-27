"""
Unified access to configuring and using the instrument.
"""
import logging

from openoligo.hal.board import Pinout
from openoligo.hal.devices import Valve
from openoligo.hal.gpio import get_gpio
from openoligo.hal.types import Board, Switchable
from openoligo.utils.singleton import Singleton

default_pinout = Pinout(
    phosphoramidites={
        "A": Valve(gpio_pin=Board.P26),
        "C": Valve(gpio_pin=Board.P28),
        "G": Valve(gpio_pin=Board.P15),
        "T": Valve(gpio_pin=Board.P16),
    },
    reactants={
        "ACT": Valve(gpio_pin=Board.P18),
        "OXI": Valve(gpio_pin=Board.P19),
        "CAP1": Valve(gpio_pin=Board.P21),
        "CAP2": Valve(gpio_pin=Board.P22),
        "DEB": Valve(gpio_pin=Board.P23),
        "CLDE": Valve(gpio_pin=Board.P24),
    },
)


class Instrument(metaclass=Singleton):
    """
    Unified access to the instrument. Hide the details of the hardware.
    """

    def __init__(self, pinout: Pinout = default_pinout) -> None:
        """
        Initialize the instrument.
        """
        self.pinout = pinout
        self.__setup()

    def __setup(self):
        """
        Setup the instrument.
        """
        self.controller = get_gpio()
        self.controller.setup()

    def all_except(self, name: list[str]) -> None:
        """
        Set the state of a pin on the instrument.

        Args:
            name: A list of valve/switch names
            state: The state of the pin.
        """
        all_valves_in_pinout = self.pinout.valves()
        for n in all_valves_in_pinout:
            if n in name:
                all_valves_in_pinout[n].open()
            else:
                all_valves_in_pinout[n].close()
        logging.info(f"Set {name} to [bold]open[/] and all others to close.", extra={"markup": True})

    def __repr__(self):
        """
        Return a string representation of the instrument.
        """
        return f"Instrument({self.pinout})"
