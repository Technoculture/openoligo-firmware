"""
Logging configuration for OpenOligo
"""
import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from rich.logging import RichHandler

# Load the environment variables from the .env file
load_dotenv()

# Configure the logger
CONSOLE_FORMAT = "<%(filename)s:%(lineno)d> %(message)s"
FILE_FORMAT = "%(asctime)s <%(filename)s:%(lineno)d> [%(levelname)s] %(message)s"
LOG_LEVEL = os.getenv("OO_LOG_LEVEL", "INFO")


def configure_logger(filename: str = "openoligo.log", *, rotates: bool = True) -> logging.Logger:
    """Configure the logger for OpenOligo"""

    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)

    if rotates:
        handler = RotatingFileHandler(filename, maxBytes=1000000, backupCount=5)
    else:
        handler = logging.FileHandler(filename)  # type: ignore

    file_logger = handler
    file_logger.setFormatter(logging.Formatter(FILE_FORMAT))
    file_logger.setLevel(logging.DEBUG)

    console_logger = RichHandler()
    console_logger.setFormatter(logging.Formatter(CONSOLE_FORMAT))
    console_logger.setLevel(logging.getLevelName(LOG_LEVEL))

    logger.addHandler(file_logger)
    logger.addHandler(console_logger)

    return logger
