"""
Unified access to configuring and using the instrument.
"""
from dataclasses import dataclass
from openoligo.hal.devices import Valve, Switch
from openoligo.fixed_keys_dict import FixedKeysDict
from openoligo.hal.gpio import get_gpio
from openoligo.hal.pins import Board


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclass
class Instrument(metaclass=Singleton):
    def __init__(self):
        self.gpio = get_gpio()

        self.gpio.setup()

        #self.valves = FixedKeysDict[str](valid_keys=set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']))
        self.pump_switch = Switch('PUMP')
