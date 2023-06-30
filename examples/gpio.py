from openoligo.hal.gpio import MockGPIO
from openoligo.hal.types import board

gpio = MockGPIO()

gpio.set(board.P21, True)
print(gpio.value(board.P21))

gpio.set(board.P22, True)
print(gpio.value(board.P22))

gpio.set(board.P40, True)
# print(gpio.value("P40"))

print(board.P21)

print(gpio)
