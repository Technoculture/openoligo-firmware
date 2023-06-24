"""
DNA Snthesis Protocol
"""
import logging
from Bio.Seq import Seq  # type: ignore
from tqdm import tqdm
from openoligo.utils import wait

# from openoligo.steps import


def synthesize(seq: Seq) -> None:
    """
    Synthesize a DNA sequence.

    :param seq: DNA sequence to synthesize.
    :return: None
    """
    logging.info("Initiating synthesis of DNA sequence: '%s'", seq)
    with tqdm(total=len(seq)) as pbar:
        for base_index, base in enumerate(seq):
            logging.debug("Adding %sth base '%s' to growing DNA strand", base_index, base)

            # TODO: Add actual synthesis code here  # pylint: disable=fixme

            wait(1)
            pbar.update(1)

    logging.info("Synthesis complete for DNA sequence: '%s'", seq)
