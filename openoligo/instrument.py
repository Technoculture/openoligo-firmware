"""
Unified access to configuring and using the instrument.
"""
import logging

from openoligo.hal.board import Pinout
from openoligo.hal.devices import Valve
from openoligo.hal.gpio import get_gpio
from openoligo.hal.types import Board, OneDestinationException, OneSourceException
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

    def __get_valve(self, name: str) -> Valve:
        """
        Get a valve by name.
        """
        valve = self.pinout.get(name)
        if not isinstance(valve, Valve):
            raise ValueError(f"{name} is not a valve")
        return valve

    def validate_valve_set(self, name: list[str]) -> None:
        """
        Validate that the list of valves conform to a set of rules.

        1. Each valve must be a valve.
        1. The list must contain one and only one reagent (inlet) valve.
        2. The list must contain one and only one product (outlet) valve.
        3. The list may contain zero or more transit valves
        4. The list may contain a branch valve, but only one.

        args:
            name: list of valve names

        raises:
            OneSourceException: If there is not exactly one source valve.
            OneDestinationException: If there is not exactly one destination valve.
        """
        source_valves = []
        destination_valves = []

        for _name in name:
            if not isinstance(self.pinout.get(_name), Valve):
                raise ValueError(f"{_name} is not a valve")

        for _name in name:
            valve: Valve = self.__get_valve(_name)
            if valve.role == "source":
                source_valves.append(valve)
            elif valve.role == "destination":
                destination_valves.append(valve)

        if len(source_valves) != 1:
            raise OneSourceException("There must be exactly one source valve")
        if len(destination_valves) != 1:
            raise OneDestinationException("There must be exactly one destination valve")

    def all_except(self, name: list[str]) -> None:
        """
        Set the state of a pin on the instrument.

        Args:
            name: A list of valve names
            state: The state of the pin.

        raises:
            OneSourceException: If there is not exactly one source valve.
            OneDestinationException: If there is not exactly one destination valve.
        """
        self.validate_valve_set(name)

        all_valves_in_pinout = self.pinout.valves()
        for _name in all_valves_in_pinout:
            if _name in name:
                all_valves_in_pinout[_name].open()
            else:
                all_valves_in_pinout[_name].close()
        logging.info(
            "Set %s to [bold]open[/] and all others to close.", name, extra={"markup": True}
        )

    def __repr__(self):
        """
        Return a string representation of the instrument.
        """
        return f"Instrument({self.pinout})"
