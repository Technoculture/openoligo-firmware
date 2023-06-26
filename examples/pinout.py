#!/usr/bin/env python
from openoligo.instrument import Pinout
from openoligo.hal.pins import Board


p = Pinout(
    waste_after_reaction=Board.P3,
    waste_other=Board.P5,
    solvent=Board.P7,
    inert_gas=Board.P8,

    output=Board.P10,
    pump=Board.P11,

    phosphoramidite= 
    { 
     "A": Board.P12, 
     "C": Board.P13, 
     "G": Board.P15, 
     "T": Board.P16
    },

    reactants= 
    { 
     "ACT": Board.P18, 
     "OXI": Board.P19, 
     "CAP1": Board.P21, 
     "CAP2": Board.P22, 
     "DEB": Board.P23,
     "CLDE": Board.P24,
     "ABC": Board.P26
    }
)


print(p)
