import asyncio
import time
from unittest.mock import AsyncMock, patch

import pytest

from openoligo.utils.wait import ms, wait, wait_async


def test_wait():
    wait(0.01)


def test_ms():
    assert ms(1) == 0.001


@pytest.mark.parametrize("factor", [10, 100, 1000])
def test_wait_async(factor):
    with patch.dict("openoligo.utils.sim.__dict__", {"SIMULATION_SPEEDUP_FACTOR": factor}):
        from openoligo.utils.sim import SIMULATION_SPEEDUP_FACTOR

        start_time = time.time()
        DURATION = 1
        asyncio.run(wait_async(DURATION))
        elapsed_time = time.time() - start_time
        assert elapsed_time == pytest.approx(
            (DURATION / SIMULATION_SPEEDUP_FACTOR) / 1000, abs=0.01
        )


@pytest.mark.asyncio
async def test_wait_async_calls_sleep():
    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        await wait_async(1)
        mock_sleep.assert_awaited_once_with(1 / 2)
