#!/usr/bin/env python
from openoligo.hal.board import Pinout, list_configurable_pins
from openoligo.hal.devices import Valve
from openoligo.hal.instrument import Instrument
from openoligo.hal.types import board
from openoligo.utils.logger import configure_logger
from openoligo.utils.wait import wait

logger = configure_logger(rotates=True)

print(list_configurable_pins())

pinout = Pinout(
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

ins = Instrument(pinout=pinout)

ins.all_except(["a", "waste_rxn", "rxn_out"])
wait(10)
ins.all_except(["t", "waste"])
wait(10)
