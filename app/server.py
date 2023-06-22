"""
Script to start the REST API server for OpenOligo.
"""
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')


def main():
    """
    This function is the main entry point of the program.
    """
    try:
        main_loop()
    except KeyboardInterrupt:
        logging.info("Program interrupted, exiting gracefully.")


def main_loop():
    """
    This function is the main loop of the program.
    """
    logging.info("Starting main loop.")


if __name__ == "__main__":
    main()
