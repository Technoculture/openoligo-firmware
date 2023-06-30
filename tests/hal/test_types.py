from openoligo.hal.platform import Platform
from openoligo.hal.types import Board, board


def test_board():
    assert isinstance(board, Board)

    bb = Board(Platform.BB)
    rpi = Board(Platform.RPI)

    assert bb != rpi

    assert int(rpi.P3) == 3
    assert bb.P3 == "P8_11"

    assert int(rpi.P40) == 40
    assert bb.P40 == "P8_38"

    assert isinstance(bb.P3, str)

    assert len(bb) == 28
    assert len(rpi) == 28
