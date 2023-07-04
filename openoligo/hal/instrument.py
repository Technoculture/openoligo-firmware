"""
Unified access to configuring and using the instrument.
"""
import logging

from openoligo.hal.board import Pinout
from openoligo.hal.devices import Valve
from openoligo.hal.gpio import get_gpio
from openoligo.hal.types import OneDestinationException, OneSourceException, ValveRole, board
from openoligo.utils.singleton import Singleton

default_pinout = Pinout(
    phosphoramidites={
        "A": Valve(gpio_pin=board.P26),
        "C": Valve(gpio_pin=board.P28),
        "G": Valve(gpio_pin=board.P15),
        "T": Valve(gpio_pin=board.P16),
    },
    reactants={
        "ACT": Valve(gpio_pin=board.P18),
        "OXI": Valve(gpio_pin=board.P19),
        "CAP1": Valve(gpio_pin=board.P21),
        "CAP2": Valve(gpio_pin=board.P22),
        "DEB": Valve(gpio_pin=board.P23),
        "CLDE": Valve(gpio_pin=board.P24),
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
        logging.info("Initializing instrument with pinout: %s", self.pinout)
        self.controller = get_gpio()

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
        2. The list must contain one and only one reagent (inlet) valve.
        3. The list must contain one and only one product (outlet) valve.
        4. The list may contain zero or more transit valves
        5. The list may contain a branch valve, but only one.

        args:
            name: list of valve names

        raises:
            OneSourceException: If there is not exactly one source valve.
            OneDestinationException: If there is not exactly one destination valve.
        """
        valve_types: dict[ValveRole, list[Valve]] = {
            ValveRole.INLET: [],
            ValveRole.OUTLET: [],
            ValveRole.BRANCH: [],
            ValveRole.TRANSIT: [],
        }

        for _name in name:
            if not isinstance(self.pinout.get(_name), Valve):
                raise ValueError(f"{_name} is not a valve")
            valve: Valve = self.__get_valve(_name)

            if valve.role not in valve_types:
                raise ValueError(f"Unknown valve role: {valve.role}")

            valve_types[valve.role].append(valve)

        if len(valve_types[ValveRole.INLET]) != 1:
            raise OneSourceException("There must be exactly one source valve")

        if len(valve_types[ValveRole.OUTLET]) != 1:
            raise OneDestinationException("There must be exactly one destination valve")

        if len(valve_types[ValveRole.TRANSIT]) > 0:
            logging.debug(
                "Make sure that the transit valve(s) are in the route you expect"
            )  # pragma: no cover

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
        logging.debug(
            "Set %s to [bold]open[/] and all others to close.", name, extra={"markup": True}
        )

    def __repr__(self):
        """
        Return a string representation of the instrument.
        """
        return f"Instrument({self.pinout})"  # pragma: no cover
