"""
Unified access to configuring and using the instrument.
"""
import logging
from typing import Callable

from openoligo.hal.board import Pinout
from openoligo.hal.devices import DigitalSensor, Valve
from openoligo.hal.gpio import get_gpio
from openoligo.hal.types import OneDestinationError, OneSourceError, ValveRole, board
from openoligo.utils.singleton import Singleton

# import anyio


default_pinout = Pinout(
    phosphoramidites={
        "A": Valve(gpio_pin=board.P26),
        "C": Valve(gpio_pin=board.P28),
        "G": Valve(gpio_pin=board.P15),
        "T": Valve(gpio_pin=board.P16),
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
            OneSourceError: If there is not exactly one source valve.
            OneDestinationError: If there is not exactly one destination valve.
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
            raise OneSourceError("There must be exactly one source valve")

        if len(valve_types[ValveRole.OUTLET]) != 1:
            raise OneDestinationError("There must be exactly one destination valve")

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
            OneSourceError: If there is not exactly one source valve.
            OneDestinationError: If there is not exactly one destination valve.
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

    def register_error_handler(self, handler: Callable[[None], None]) -> None:
        """
        Register an error handler.

        Args:
            handler: A function that takes no arguments and returns nothing.
        """
        pressure_error_sensors: dict[str, DigitalSensor] = self.pinout.get_error_sensors()
        for _, sensor in pressure_error_sensors.items():
            sensor.register_callback(handler)

    def pressure_on(self) -> None:
        """
        Switches the gas inlet ON by switching on the pressure regulator.
        """
        self.pinout.fixed["air_pressure"].set(True)
        self.pinout.fixed["liquid_pressure"].set(True)

    def pressure_off(self) -> None:
        """
        Switches the gas inlet ON by switching on the pressure regulator.
        """
        self.pinout.fixed["liquid_pressure"].set(False)
        self.pinout.fixed["air_pressure"].set(False)

    # async def monitor_pressure(self) -> None:
    #    """
    #    Monitor the pressure sensors.
    #    """
    #    pressure_error_sensors: dict[str, DigitalSensor] = self.pinout.get_error_sensors()
    #    while True:
    #        pressure_errors = {k: v.value() for k, v in pressure_error_sensors.items()}
    #        logging.debug("Pressure errors: %s", pressure_errors)
    #        if pressure_errors["liquid_pressure"] and pressure_errors["air_pressure"]:
    #            raise RuntimeError("Both liquid and air pressure are low")
    #        elif pressure_errors["liquid_pressure"]:
    #            raise RuntimeError("Liquid pressure error")
    #        elif pressure_errors["air_pressure"]:
    #            raise RuntimeError("Air pressure error")
    #        await anyio.sleep(1)

    def __repr__(self):
        """
        Return a string representation of the instrument.
        """
        return f"Instrument({self.pinout})"  # pragma: no cover
