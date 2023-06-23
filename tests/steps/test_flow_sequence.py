from time import time

from openoligo.driver.manifold import Manifold
from openoligo.driver.switch import MockValve
from openoligo.steps.flow_sequence import perform_flow_sequence
from openoligo.steps.types import FlowWaitPair
from openoligo.utils.wait import ms


def test_perform_flow_sequence():
    """Test the perform_flow_sequence function."""
    m = Manifold(MockValve, 4)
    # Test that the function returns the expected results
    # when the flow sequence is empty
    assert all(m.value(i) for i in range(m.size)), "Valves should be open by default"
    perform_flow_sequence(m, [])
    assert all(m.value(i) for i in range(m.size)), "Valves should be open after empty sequence"

    # Test that the function returns the expected results
    # when the flow sequence is not empty
    flow_sequence = [
        FlowWaitPair((1, ms(50))),
        FlowWaitPair((2, ms(100))),
        FlowWaitPair((3, ms(80))),
    ]
    t0 = time()
    perform_flow_sequence(m, flow_sequence)
    t1 = time()
    assert not all(m.value(i) for i in range(m.size) if i != 3), "Valves 0, 1, 2 should be closed"
    assert m.value(3), "Valve 3 should be open"
    # The function should have taken at least 550ms to run
    assert t1 - t0 >= 0.23, "Function should have taken at least 230ms to run"
    # The function should have taken at most 600ms to run
    assert t1 - t0 <= 0.3, "Function should have taken at most 300ms to run"
