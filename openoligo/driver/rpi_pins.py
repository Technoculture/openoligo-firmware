"""
Pins in the Raspberry Pi GPIO header.
"""
from enum import Enum

# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BOARD)


class RPi(Enum):
    """
    Enumerates the GPIO pins on the Raspberry Pi 3 Model B.
    """

    PIN3 = 3
    PIN5 = 5
    PIN7 = 7
    PIN8 = 8
    PIN10 = 10
    PIN11 = 11
    PIN12 = 12
    PIN13 = 13
    PIN15 = 15
    PIN16 = 16
    PIN18 = 18
    PIN19 = 19
    PIN21 = 21
    PIN22 = 22
    PIN23 = 23
    PIN24 = 24
    PIN26 = 26
    PIN27 = 27
    PIN28 = 28
    PIN29 = 29
    PIN31 = 31
    PIN32 = 32
    PIN33 = 33
    PIN35 = 35
    PIN36 = 36
    PIN37 = 37
    PIN38 = 38
    PIN40 = 40


# Then, to use a pin you can refer to it as follows:
# GPIO.setup(RPiBoardPins.PIN3.value, GPIO.OUT)
