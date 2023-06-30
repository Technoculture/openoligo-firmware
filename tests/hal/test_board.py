from unittest.mock import MagicMock, patch

import pytest

from openoligo.hal.board import Pinout, fixed_pinout, list_configurable_pins
from openoligo.hal.devices import Valve
from openoligo.hal.platform import Platform
from openoligo.hal.types import Board, NoSuchPinInPinout, board


def test_board():
    assert isinstance(board, Board)

    board1 = Board(Platform.BB)
    board2 = Board(Platform.RPI)

    assert board1 != board2

    assert int(board2.P3) == 3
    assert board1.P3 == "P8_11"

    assert int(board2.P40) == 40
    assert board1.P40 == "P8_38"

    assert isinstance(board1.P3, str)
    board1 = Board(Platform.BB)
