"""
Logging configuration for OpenOligo
"""
import os
import logging
from dotenv import load_dotenv
from rich.logging import RichHandler

# Load the environment variables from the .env file
load_dotenv()

# Configure the logger
FORMAT = "<%(filename)s:%(lineno)d> %(message)s"
LOG_LEVEL = os.getenv("OO_LOG_LEVEL", "NOTSET")

logging.basicConfig(
    level=logging.getLevelName(LOG_LEVEL), format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger("rich")
