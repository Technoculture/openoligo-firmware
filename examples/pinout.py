#!/usr/bin/env python
from openoligo.hal.board import Pinout, list_configurable_pins
from openoligo.hal.devices import Valve
from openoligo.hal.instrument import Instrument
from openoligo.hal.types import board
from openoligo.utils.logger import OligoLogger
from openoligo.utils.wait import wait

rl = OligoLogger(rotates=True)
root_logger = rl.get_logger()

print(list_configurable_pins())

pinout = Pinout(
    phosphoramidites={
        "A": Valve(gpio_pin=board.P26),
        "C": Valve(gpio_pin=board.P28),
        "G": Valve(gpio_pin=board.P15),
        "T": Valve(gpio_pin=board.P16),
    },
)

ins = Instrument(pinout=pinout)

ins.all_except(["a", "waste_rxn", "rxn_out"])
wait(10)
ins.all_except(["t", "waste"])
wait(10)
