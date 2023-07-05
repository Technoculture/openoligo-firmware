import logging
from logging.handlers import RotatingFileHandler
from unittest.mock import MagicMock, call, create_autospec, patch

import pytest

from openoligo.utils.logger import OligoLogger, log_path

# from rich.logging import RichHandler


def test_log_path(tmpdir):
    name = "test"
    path = tmpdir.join("logs")
    expected_path = f"{path}/{name}.log"
    with patch("os.getenv", return_value=str(tmpdir)):
        assert log_path(name) == expected_path
        assert log_path(None) == f"{path}/openoligo.log"


def test_oligo_logger_initialization():
    with patch("logging.getLogger", return_value=logging.Logger("test")) as mock_get_logger:
        logger = OligoLogger("test")
        assert logger.name == "test"
        assert logger.log_level == "INFO"
        assert isinstance(logger.logger, logging.Logger)


def test_get_logger():
    logger = OligoLogger("test")
    with patch.object(
        logger, "_OligoLogger__get_file_handler", return_value=logging.StreamHandler()
    ), patch.object(
        logger, "_OligoLogger__get_console_handler", return_value=logging.StreamHandler()
    ):
        logger_obj = logger.get_logger()
        assert isinstance(logger_obj, logging.Logger)


def test_get_file_handler():
    logger = OligoLogger("test", rotates=False)

    with patch(
        "logging.FileHandler", return_value=logging.FileHandler("dummy.log")
    ) as mock_file_handler:
        _ = logger._OligoLogger__get_file_handler()
        mock_file_handler.assert_called_with(log_path(logger.name))


def test_get_console_handler():
    logger = OligoLogger("test", log_level="WARNING")
    with patch("rich.logging.RichHandler", return_value=logging.StreamHandler()):
        console_handler = logger._OligoLogger__get_console_handler()
        assert console_handler.level == logging.getLevelName("WARNING")


def test_change_log_file():
    logger = OligoLogger("test", rotates=False)
    old_mock_file_handler = create_autospec(logging.FileHandler)

    # Replace handlers with mock handler
    for handler in logger.logger.handlers[:]:
        logger.logger.removeHandler(handler)
    logger.logger.addHandler(old_mock_file_handler)

    # Test exception when trying to change log file name when rotates is True
    logger.rotates = True
    with pytest.raises(ValueError):
        logger.change_log_file("new_test")

    # TODO: Add tests
