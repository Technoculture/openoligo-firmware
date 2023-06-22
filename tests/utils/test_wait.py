from openoligo.utils.wait import ms, wait


def test_wait():
    wait(0.01)


def test_ms():
    assert ms(1) == 0.001
