import pytest

from openoligo.driver.manifold import Manifold
from openoligo.driver.switch import MockValve
from openoligo.driver.types import InvalidManifoldSizeError


@pytest.mark.parametrize("size", [4, 8, 10, 16, 20])
def test_manifold(size):
    manifold = Manifold(valve_class=MockValve, size=size)
    assert len(manifold.valves) == size
    # assert all(not manifold.value(i) for i in range(size))

    for i in range(size):
        manifold.set(i, True)
        assert manifold.value(i), "Failed to set {}th valve to True".format(i)
        manifold.set(i, False)
        assert not manifold.value(i), "Failed to set {}th valve to False".format(i)

    with pytest.raises(ValueError):
        manifold.set(-1, True)  # bad index
    with pytest.raises(ValueError):
        manifold.set(size, True)  # bad index
    assert not manifold.value(-1)  # not bad index !!!
    with pytest.raises(ValueError):
        manifold.value(size)  # bad index


def test_manifold_invalid_size():
    with pytest.raises(InvalidManifoldSizeError):
        Manifold(MockValve, 5)


def test_manifold_invalid_switch_type():
    with pytest.raises(TypeError):
        Manifold(int, 4)  # type: ignore


def test_set_manifold():
    manifold = Manifold(MockValve, 4)
    manifold.all(True)
    assert all(
        manifold.value(i) for i in range(4)
    ), "Failed to set all valves to True (Close all flows)"

    manifold.one_hot(2)
    assert (
        manifold.value(2)
        and not manifold.value(0)
        and not manifold.value(1)
        and not manifold.value(3)
    ), "Failed to set one_hot to 2"

    manifold.toggle()
    assert not manifold.value(2) and manifold.value(0) and manifold.value(1) and manifold.value(3)


@pytest.mark.parametrize("indices", [[0, 3], [0, 1, 3], [2]])
def test_n_hot(indices):
    manifold = Manifold(MockValve, 4)
    manifold.n_hot(indices)
    assert all(manifold.value(i) for i in indices), "Failed to set n_hot to {}".format(indices)
    assert not any(
        manifold.value(i) for i in range(4) if i not in indices
    ), "Failed to set n_hot to {}".format(indices)


@pytest.mark.parametrize("indices", [[5, 4], [-1], [4], [10, 20]])
def test_n_hot_invalid_indices(indices):
    manifold = Manifold(MockValve, 4)
    with pytest.raises(ValueError):
        manifold.n_hot(indices)
