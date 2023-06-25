"""
DNA Snthesis Protocol
"""
from time import time
import logging
from Bio.Seq import Seq  # type: ignore
from tqdm import tqdm
from openoligo.utils import wait_async
from openoligo.steps.flow import solvent_wash_all, dry_all

import openoligo.utils as utils


async def detritylate() -> None:
    """
    Remove the trityl group from the 5'-end of the DNA sequence.
    Involves the reagent to be sent to the reactor, and then the reactor to be washed and dried.
    """
    logging.debug("Add 3% trichloroacetic acid in dichloromethane to the reactor")
    # send_to_reactor("CAP")
    await wait_async(50)


async def activate() -> None:
    """
    0.1 M phosphoramidite monomer and 0.5 M tetrazole in acetonitrile
    """
    logging.debug("Add 0.1 M phosphoramidite monomer and 0.5 M tetrazole to the reactor")
    # 1. Trigger transports
    #    send_to_reactor("0.1 M phosphoramidite monomer and 0.5 M tetrazole in acetonitrile")
    # 2. Wait for residence time
    await wait_async(50)


async def cap() -> None:
    """
    acetic anhydride/pyridine/THF 1/1/8 and 17.6% w/v N-methyl imidazole in acetonitrile
    """
    logging.debug("Add acetic anhydride/pyridine/THF and N-methyl imidazole to the reactor")
    # send_to_reactor("acetic anhydride/pyridine/THF and N-methyl imidazole")
    await wait_async(30)


async def oxidize() -> None:
    """
    Oxidize the DNA sequence.
    0.015 M iodine in water/pyridine/THF 2/20/78
    """
    logging.debug("Add 0.015 M iodine in water/pyridine/THF to the reactor")
    # send_to_reactor("Oxidizing the DNA sequence")
    await wait_async(45)


async def cleave() -> None:
    """
    Cleave the DNA sequence from the solid support.
    """
    logging.debug("Cleaving the DNA sequence from the solid support")
    # send_to_reactor("Cleaving the DNA sequence from the solid support")
    await wait_async(180)


async def deprotect() -> None:
    """
    Remove the protecting groups from the DNA sequence.
    """
    logging.debug("Removing protecting groups from the DNA sequence")
    # send_to_reactor("Removing protecting groups from the DNA sequence")
    await wait_async(45)


async def synthesize(seq: Seq) -> None:
    """
    Synthesize a DNA sequence.

    args:
        seq: DNA sequence to synthesize.
    """
    logging.info("Initiating synthesis of DNA sequence: '%s'", seq)
    start_time = time()  # start timer
    with tqdm(total=len(seq) + 2) as pbar:
        solvent_wash_all()
        dry_all()

        pbar.update(1)

        for base_index, base in enumerate(seq):
            logging.info("Adding %sth base '%s' to growing DNA strand", base_index, base)

            await detritylate()

            solvent_wash_all()
            dry_all()

            await activate()

            solvent_wash_all()
            dry_all()

            await cap()

            solvent_wash_all()
            dry_all()

            await oxidize()

            solvent_wash_all()
            dry_all()

            await wait_async(1)
            pbar.update(1)

        await cleave()
        await deprotect()

        pbar.update(1)
    end_time = time()  # end timer
    elapsed_time_in_minutes = ((end_time - start_time) / 60) * utils.SIMULATION_SPEEDUP_FACTOR
    logging.info("Synthesis complete for DNA sequence: '%s' in %s minutes", 
                 seq, elapsed_time_in_minutes)
