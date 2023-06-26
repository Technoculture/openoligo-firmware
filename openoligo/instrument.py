"""
Unified access to configuring and using the instrument.
"""
from dataclasses import dataclass
from typing import Any, Dict

from openoligo.hal.board import Board
from openoligo.hal.devices import Switch, Valve
from openoligo.hal.types import Switchable

# from openoligo.hal.gpio import get_gpio


class Singleton(type):
    """
    Metaclass for singleton classes.
    """

    _instances: Dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclass
class EssentialPinouts(metaclass=Singleton):
    """
    Essential pinouts for the instrument.
    """

    waste_after_reaction: Valve = Valve(gpio_pin=Board.P5)
    waste_other: Valve = Valve(gpio_pin=Board.P7)
    solvent: Valve = Valve(gpio_pin=Board.P3)
    inert_gas: Valve = Valve(gpio_pin=Board.P10)

    output: Valve = Valve(gpio_pin=Board.P8)
    pump: Switch = Switch(gpio_pin=Board.P11)


class Pinout(metaclass=Singleton):
    """
    Pinout for the instrument.
    """

    def __init__(
        self,
        essentials: EssentialPinouts,
        phosphoramidites: Dict[str, Valve],
        reactants: Dict[str, Valve],
    ):
        """
        Initialize the pinout.
        """
        self.essentials = essentials
        self.phosphoramidite = phosphoramidites
        self.reactants = reactants
        self.__pinout: Dict[str, Switchable] = {}
        self.init_pinout()

    def check_pin_duplicate(self, pin, category, sub_category):
        """
        Check for duplicate pin usage.
        """
        if pin in self.__pinout.values():
            raise ValueError(f"Pin {pin} is used twice in {category}.{sub_category}.")
        self.__pinout[sub_category] = pin
        # print(sub_category, pin)

    def init_pinout(self):
        """
        Make sure no pin is used twice.
        """
        for category, pins in self.__dict__.items():
            if category.startswith("_"):
                continue

            if isinstance(pins, EssentialPinouts):
                for sub_category, pin in pins.__dict__.items():
                    self.check_pin_duplicate(pin, category, sub_category)
            elif isinstance(pins, dict):
                for sub_category, pin in pins.items():
                    self.check_pin_duplicate(pin, category, sub_category)
            else:
                self.check_pin_duplicate(pins, category, "")

    def __repr__(self):
        """
        Return a string representation of the pinout.
        """
        return f"Pinout({self.__pinout})"


# class Instrument(metaclass=Singleton):
#    """
#    Unified access to the instrument. Hide the details of the hardware.
#    """
#
#    def __init__(self, pinout: Pinout) -> None:
#        """
#        Initialize the instrument.
#        """
#        self.pinout = pinout
#        self.__setup()
#
#    def __setup(self):
#        """
#        Setup the instrument.
#        """
#        self.__gpio = get_gpio()
#        self.__gpio.setup()
#
#    def __repr__(self):
#        """
#        Return a string representation of the instrument.
#        """
#        return f"Instrument({self.pinout})"
