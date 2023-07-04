"""
Logging configuration for OpenOligo
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional

from dotenv import load_dotenv
from rich.logging import RichHandler

load_dotenv()
LOG_LEVEL = os.getenv("OO_LOG_LEVEL", "INFO")


def log_path(name: Optional[str]) -> str:
    """
    Get the path to the log file
    """
    log_dir = os.getenv("OO_LOG_DIR", os.path.expanduser("~/.openoligo/logs"))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Created log directory: {log_dir}")
    if name is None:
        return os.path.join(log_dir, "openoligo.log")
    return os.path.join(log_dir, f"{name}.log")


class OligoLogger:
    """
    Logger for OpenOligo
    """

    CONSOLE_FORMAT = "<%(name)s:%(lineno)d> %(message)s"
    FILE_FORMAT = "%(asctime)s <%(name)s:%(lineno)d> [%(levelname)s] %(message)s"
    DEFAULT_LOG_NAME = "openoligo"

    def __init__(
        self, name: Optional[str] = None, *, log_level: str = LOG_LEVEL, rotates: bool = True
    ):
        """Initialize the logger"""
        self.log_level = log_level
        self.name = name
        self.rotates = rotates

        if self.name is None:
            self.logger = logging.getLogger()
        else:
            self.logger = logging.getLogger(self.name)
            self.logger.propagate = False

        self.logger.setLevel(logging.NOTSET)

    def get_logger(self) -> logging.Logger:
        """Return a logger with the given name."""
        print(self.logger.handlers)

        if not self.logger.handlers:
            # If no handlers are set, add them
            self.logger.addHandler(self.__get_file_handler())
            self.logger.addHandler(self.__get_console_handler())
            print(self.logger.handlers)
            return self.logger

        # print(logging.StreamHandler in [(type(h)) for h in self.logger.handlers])
        if logging.StreamHandler in [type(h) for h in self.logger.handlers]:
            # If a console handler is set, remove it
            self.logger.handlers.clear()
            self.logger.addHandler(self.__get_console_handler())
            return self.logger

        return self.logger

    def __get_file_handler(self) -> logging.Handler:
        """Get file handler for logging"""
        if self.rotates:
            handler = RotatingFileHandler(log_path(self.name), maxBytes=1000000, backupCount=5)
        else:
            handler = logging.FileHandler(log_path(self.name))  # type: ignore

        handler.setFormatter(logging.Formatter(self.FILE_FORMAT))
        handler.setLevel(logging.DEBUG)
        return handler

    def __get_console_handler(self) -> logging.Handler:
        """Get console handler for logging"""
        console_handler = RichHandler()
        console_handler.setFormatter(logging.Formatter(self.CONSOLE_FORMAT))
        console_handler.setLevel(logging.getLevelName(self.log_level))
        return console_handler

    def change_log_file(self, new_name: str) -> None:
        """Allows change of the file being logged to

        rasises:
            ValueError: if attempting to change filename of a rotating log
        """
        if self.rotates:
            raise ValueError("Cannot change log file when rotating is enabled")

        if self.name == new_name:
            logging.warning("Log file name is already set to %s. No change needed.", new_name)
            return

        log_level = self.logger.level

        for handler in self.logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                self.logger.removeHandler(handler)

        new_file_handler = logging.FileHandler(log_path(new_name))
        new_file_handler.setFormatter(logging.Formatter(OligoLogger.FILE_FORMAT))
        new_file_handler.setLevel(log_level)

        self.logger.addHandler(new_file_handler)
