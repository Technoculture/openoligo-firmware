import pytest

from openoligo.hal.platform import Platform
from openoligo.hal.types import Board, board


def test_board():
    assert isinstance(board, Board)

    bb = Board(Platform.BB)
    rpi = Board(Platform.RPI)

    assert bb != rpi

    assert int(rpi.P3) == 3
    assert bb.P3 == "P8_3"

    assert int(rpi.P40) == 40
    assert bb.P40 == "P8_30"

    assert isinstance(bb.P3, str)

    assert len(bb) == 45
    assert len(rpi) == 28

    with pytest.raises(AttributeError):
        bb.foo

    with pytest.raises(AttributeError):
        bb.P10000


def test_board_loop():
    for pin, _ in board:
        assert isinstance(pin, str)
