#!/usr/bin/env python
from openoligo.hal.board import Board
from openoligo.hal.devices import Switch, Valve
from openoligo.instrument import EssentialPinouts, Pinout

e = EssentialPinouts(
    waste_after_reaction=Valve(gpio_pin=Board.P3),
    waste_other=Valve(gpio_pin=Board.P5),
    solvent=Valve(gpio_pin=Board.P7),
    inert_gas=Valve(gpio_pin=Board.P8),
    output=Valve(gpio_pin=Board.P10),
    pump=Switch(gpio_pin=Board.P12),
)

p = Pinout(
    essentials=e,
    phosphoramidites={
        "A": Valve(gpio_pin=Board.P26),
        "C": Valve(gpio_pin=Board.P13),
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


print(p)
