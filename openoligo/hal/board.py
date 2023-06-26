"""
Pins in the Raspberry Pi GPIO header.
"""
from enum import Enum


class Board(Enum):
    """
    Enumerates the GPIO pins on the Raspberry Pi 3 Model B.
    """

    P3 = 3
    P5 = 5
    P7 = 7
    P8 = 8
    P10 = 10
    P11 = 11
    P12 = 12
    P13 = 13
    P15 = 15
    P16 = 16
    P18 = 18
    P19 = 19
    P21 = 21
    P22 = 22
    P23 = 23
    P24 = 24
    P26 = 26
    P27 = 27
    P28 = 28
    P29 = 29
    P31 = 31
    P32 = 32
    P33 = 33
    P35 = 35
    P36 = 36
    P37 = 37
    P38 = 38
    P40 = 40
