from time import time

from openoligo.utils.wait import ms, wait, with_wait


def test_wait():
    wait(0.01)


def test_ms():
    assert ms(1) == 0.001


def test_with_wait():
    def p():
        print("Hello World!")

    start = time()
    with_wait(p, 0.01)
    end = time()

    assert end - start >= 0.01
    assert end - start < 0.02
