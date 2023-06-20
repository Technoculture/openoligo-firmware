"""
This module contains the main entry point for the openoligo application.
"""
import asyncio
import logging

from openoligo.driver.switch import SimulatedSwitch, periodic_toggle

logging.basicConfig(level=logging.INFO)


def main():
    """
    This function is the main entry point of the program.
    """
    switch1 = SimulatedSwitch(pin=1, name="Switch 1")
    switch2 = SimulatedSwitch(pin=2, name="Switch 2")

    try:
        asyncio.run(main_loop(switch1, switch2, interval=1))
    except KeyboardInterrupt:
        logging.info("Program interrupted, exiting gracefully.")


async def main_loop(switch1: SimulatedSwitch, switch2: SimulatedSwitch, interval: float):
    await asyncio.gather(
        periodic_toggle(switch1, interval, loop_forever=True),
        periodic_toggle(switch2, interval + 1, loop_forever=True),
    )


if __name__ == "__main__":
    main()
