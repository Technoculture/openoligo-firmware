#!/usr/bin/env python
# from openoligo.hal.board import Pinout, list_configurable_pins
# from openoligo.hal.devices import Valve
# from openoligo.hal.instrument import Instrument
# from openoligo.hal.types import board
# from openoligo.hil.board import Hil
# from openoligo.utils.logger import OligoLogger
# from openoligo.utils.wait import wait
#
# rl = OligoLogger(rotates=True)
# root_logger = rl.get_logger()
#
# print(len(list_configurable_pins()))

# pinout = Pinout(
#    phosphoramidites={
#        "A": Valve(gpio_pin=board.P26),
#        "C": Valve(gpio_pin=board.P28),
#        "G": Valve(gpio_pin=board.P15),
#        "T": Valve(gpio_pin=board.P16),
#    },
#    reactants={
#        "ACT": Valve(gpio_pin=board.P18),
#        "OXI": Valve(gpio_pin=board.P19),
#        "CAP1": Valve(gpio_pin=board.P21),
#        "CAP2": Valve(gpio_pin=board.P22),
#        "DEB": Valve(gpio_pin=board.P23),
#        "CLDE": Valve(gpio_pin=board.P24),
#    },
# )

# hil = Hil(pinout=pinout)


# def main():
#    ins = Instrument(pinout=pinout)
#
#    pins = pinout.pins()
#    print(f"{pins=}, {len(pins)=}")
#
#    for pin in pins:
#        p = pinout.get(pin)
#        print(f"{type(p)=}, {p=}")
#
#
# if __name__ == "__main__":
#    main()
