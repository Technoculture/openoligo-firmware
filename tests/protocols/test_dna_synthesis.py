import asyncio
from unittest.mock import AsyncMock, patch  # , call

from openoligo.hal.instrument import Instrument
from openoligo.protocols.oligosynthesis import synthesize_ssdna
from openoligo.seq import Seq
from openoligo.steps.flow import send_to_waste_rxn
from openoligo.utils import wait_async


def test_synthesize():
    with patch("openoligo.utils.wait_async", new_callable=AsyncMock) as mock_wait_async, patch(
        "openoligo.steps.flow.send_to_waste_rxn", new_callable=AsyncMock
    ) as mock_send_to_waste_rxn:
        # Creating mock Instrument and Seq objects
        mock_instrument = AsyncMock(spec=Instrument)
        mock_seq = Seq("ATGC")  # or use a mock, depending on Seq class complexity

        # Running the function
        asyncio.run(synthesize_ssdna(mock_instrument, mock_seq))

        ## Checking that the function calls the correct functions in the correct order
        # mock_wait_async.assert_has_calls(
        #    [
        #        call(mock_instrument, "send_to_waste_rxn", "act")
        #    ]
        # )
