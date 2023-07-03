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
# DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
# DATE_FORMAT = "%H:%M:%S"
LOG_LEVEL = os.getenv("OO_LOG_LEVEL", "INFO")

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

rot = RotatingFileHandler("openoligo.log", maxBytes=1000000, backupCount=5)
rot.setFormatter(logging.Formatter(FILE_FORMAT))
rot.setLevel(logging.DEBUG)

rich = RichHandler()
rich.setFormatter(logging.Formatter(CONSOLE_FORMAT))
rich.setLevel(logging.getLevelName(LOG_LEVEL))

logger.addHandler(rot)
logger.addHandler(rich)
