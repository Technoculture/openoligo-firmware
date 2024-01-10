from unittest.mock import mock_open, patch

from openoligo.hal.platform import Platform, get_platform, is_bb, is_rpi


def test_rpi():
    with patch("builtins.open", mock_open(read_data="Raspberry")):
        assert is_rpi() is True


def test_not_rpi():
    with patch("builtins.open", mock_open(read_data="Arm")):
        assert is_rpi() is False
    with patch("builtins.open", mock_open(read_data="Intel")):
        assert is_bb() is False


def test_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        assert is_rpi() is False
        assert is_bb() is False


def test_bb():
    with patch("builtins.open", mock_open(read_data="AM33XX")):
        assert is_bb() is True


def test_not_bb():
    with patch("builtins.open", mock_open(read_data="Arm")):
        assert is_bb() is False
    with patch("builtins.open", mock_open(read_data="Intel")):
        assert is_bb() is False


def test_get_platform():
    with patch("builtins.open", mock_open(read_data="Raspberry")):
        assert is_rpi() is True
        assert is_bb() is False
        assert get_platform() == Platform.RPI

    with patch("builtins.open", mock_open(read_data="AM33XX")):
        assert is_rpi() is False
        assert is_bb() is True
        assert get_platform() == Platform.BB

    with patch("builtins.open", mock_open(read_data="Arm")):
        assert is_rpi() is False
        assert is_bb() is False
        assert get_platform() == Platform.SIM

    with patch("builtins.open", mock_open(read_data="Intel")):
        assert is_rpi() is False
        assert is_bb() is False
        assert get_platform() == Platform.SIM
