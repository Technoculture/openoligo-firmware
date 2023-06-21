import pytest

from openoligo.driver.manifold import (Manifold, set_manifold, set_one_hot,
                                       toggle_manifold)
from openoligo.driver.switch import SimulatedSwitch
from openoligo.driver.types import InvalidManifoldSizeError


@pytest.mark.asyncio
@pytest.mark.parametrize("size", [4, 8, 10, 16, 20])
async def test_manifold(size):
    manifold = Manifold(SimulatedSwitch, size)
    assert len(manifold.switches) == size
    assert all(not manifold.value(i) for i in range(size))

    for i in range(size):
        await manifold.set(i, True)
        assert manifold.value(i)  # == True
        await manifold.set(i, False)
        assert not manifold.value(i)  # == False

    with pytest.raises(ValueError):
        await manifold.set(-1, True)
    with pytest.raises(ValueError):
        await manifold.set(size, True)
    with pytest.raises(ValueError):
        manifold.value(-1)
    with pytest.raises(ValueError):
        manifold.value(size)


def test_manifold_invalid_size():
    with pytest.raises(InvalidManifoldSizeError):
        Manifold(SimulatedSwitch, 5)


def test_manifold_invalid_switch_type():
    with pytest.raises(TypeError):
        Manifold(int, 4)  # type: ignore


@pytest.mark.asyncio
async def test_set_manifold():
    manifold = Manifold(SimulatedSwitch, 4)
    await set_manifold(manifold, True)
    assert all(manifold.value(i) for i in range(4))
    await set_one_hot(manifold, 2)
    assert (
        manifold.value(2)
        and not manifold.value(0)
        and not manifold.value(1)
        and not manifold.value(3)
    )
    await toggle_manifold(manifold)
    assert not manifold.value(2) and manifold.value(0) and manifold.value(1) and manifold.value(3)
