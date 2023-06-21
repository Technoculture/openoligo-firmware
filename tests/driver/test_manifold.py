import pytest

from openoligo.driver.manifold import SwitchSet
from openoligo.driver.switch import SimulatedSwitch
from openoligo.driver.types import InvalidManifoldSizeError


@pytest.mark.asyncio
@pytest.mark.parametrize("size", [4, 8, 10, 16, 20])
async def test_switch_set(size):
    switch_set = SwitchSet(SimulatedSwitch, size)
    assert len(switch_set.switches) == size
    assert all(not switch_set.value(i) for i in range(size))

    for i in range(size):
        await switch_set.set(i, True)
        assert switch_set.value(i)  # == True
        await switch_set.set(i, False)
        assert not switch_set.value(i)  # == False

    with pytest.raises(ValueError):
        await switch_set.set(-1, True)
    with pytest.raises(ValueError):
        await switch_set.set(size, True)
    with pytest.raises(ValueError):
        switch_set.value(-1)
    with pytest.raises(ValueError):
        switch_set.value(size)


def test_switch_set_invalid_size():
    with pytest.raises(InvalidManifoldSizeError):
        SwitchSet(SimulatedSwitch, 5)
