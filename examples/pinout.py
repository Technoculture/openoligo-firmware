#!/usr/bin/env python
from openoligo.hal.board import Pinout, list_configurable_pins
from openoligo.instrument import Instrument

# from openoligo.hal.devices import Valve
# from openoligo.hal.types import Board


# print(list_configurable_pins())

# pinout = Pinout(
#    phosphoramidites={
#        "A": Valve(gpio_pin=Board.P26),
#        "C": Valve(gpio_pin=Board.P28),
#        "G": Valve(gpio_pin=Board.P15),
#        "T": Valve(gpio_pin=Board.P16),
#    },
#    reactants={
#        "ACT": Valve(gpio_pin=Board.P18),
#        "OXI": Valve(gpio_pin=Board.P19),
#        "CAP1": Valve(gpio_pin=Board.P21),
#        "CAP2": Valve(gpio_pin=Board.P22),
#        "DEB": Valve(gpio_pin=Board.P23),
#        "CLDE": Valve(gpio_pin=Board.P24),
#    },
# )

pinout = Pinout()

# print(pinout)

# a = pinout.get("a")
# a.close()
#
# pump = pinout.get("pump")
# pump.toggle()

ins = Instrument(pinout=pinout)
ins.all_except(["a", "waste"])