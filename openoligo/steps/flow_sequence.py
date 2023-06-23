"""
Utilities for flow sequence steps.
"""
import logging

from openoligo.driver.manifold import Manifold

# from openoligo.driver.types import SwitchingError
from openoligo.steps.types import FlowWaitPairs
from openoligo.utils.wait import with_wait


def perform_flow_sequence(manifold: Manifold, flow_wait_pairs: FlowWaitPairs):
    """Perform a sequence of flow activations and waits on a manifold.

    Arguments:
    manifold -- the manifold object to perform operations on
    flow_wait_pairs -- a list of tuples, where each tuple is (valve number, wait time)
    """
    for valve, wait_time in flow_wait_pairs:
        # try:
        logging.debug("Activating valve %d, and starting wait for %.2fs", valve, wait_time)
        with_wait(manifold.activate_flow, wait_time, valve)
        # except SwitchingError as exc:
        #    print(f"An error occurred while activating flow {valve}: {str(exc)}")
