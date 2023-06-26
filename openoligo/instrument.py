"""
Unified access to configuring and using the instrument.
"""
from dataclasses import dataclass, field
from typing import Any, Dict

from openoligo.fixed_keys_dict import FixedKeysDict
from openoligo.hal.devices import Switch, Valve
from openoligo.hal.gpio import get_gpio
from openoligo.hal.pins import Board


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
class Pinout(metaclass=Singleton):
    """
    Pinout for the instrument.
    """
    waste_after_reaction: Valve
    waste_other: Valve
    solvent: Valve
    inert_gas: Valve

    output: Valve
    pump: Switch

    phosphoramidite: FixedKeysDict = FixedKeysDict[Valve](set(['A', 'C', 'G', 'T']))
    reactants: FixedKeysDict = FixedKeysDict[Valve](set(['ACT', 'OXI', 'CAP1', 'CAP2', 'DEB', 'CLDE']))

    __pinout: Dict[str, Board] = field(init=False)


    def __post_init__(self):
        """
        Make sure no pin is used twice.
        """
        self.__pinout = {}
        # print(self.__dict__.items())
        for k, v in self.__dict__.items():
            if k.startswith('_'):
                continue
            if isinstance(v, dict):
                for sub_k, sub_v in v.items():
                    if sub_v in self.__pinout.values():
                        raise ValueError(f'Pin {sub_v} is used twice in {k}.{sub_k}.')
                    self.__pinout[sub_k] = sub_v
            else:
                if v in self.__pinout.values():
                    raise ValueError(f'Pin {v} is used twice in {k}.')
                self.__pinout[k] = v


    def __repr__(self):
        """
        Return a string representation of the pinout.
        """
        return f'Pinout({self.__pinout})'


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
