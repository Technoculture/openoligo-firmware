"""
This module contains the main entry point for the openoligo application.
"""
import logging

from openoligo.driver.switch import SimulatedSwitch, periodic_toggle

logging.basicConfig(level=logging.INFO)


def main():
    """
    This function is the main entry point of the program.
    """
    switch1 = SimulatedSwitch(pin=1, name="Switch 1")

    try:
        main_loop(switch1, interval=1)
    except KeyboardInterrupt:
        logging.info("Program interrupted, exiting gracefully.")


def main_loop(switch1: SimulatedSwitch, interval: float):
    periodic_toggle(switch1, interval, loop_forever=True)


if __name__ == "__main__":
    main()
