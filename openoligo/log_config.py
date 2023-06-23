"""
Logging configuration for OpenOligo
"""
import logging

from rich.logging import RichHandler

# Configure the logger
FORMAT = "[%(filename)s:%(lineno)d] %(message)s"

logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

logger = logging.getLogger("rich")
