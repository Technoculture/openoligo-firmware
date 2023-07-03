"""
DNA Snthesis Protocol
"""
from time import time

from tqdm import tqdm

from openoligo import utils
from openoligo.hal.instrument import Instrument
from openoligo.seq import Seq
from openoligo.steps.flow import dry_all, send_to_waste_rxn, solvent_wash_all
from openoligo.steps.types import step
from openoligo.utils import wait_async
from openoligo.utils.logger import configure_logger

logger = configure_logger()


@step
async def detritylate(instrument: Instrument) -> None:
    """
    Add 3% trichloroacetic acid in dichloromethane to the reactor
    """
    await send_to_waste_rxn(instrument, "act")
    await wait_async(50)


@step
async def activate(instrument: Instrument) -> None:
    """
    Add 0.1 M phosphoramidite monomer and 0.5 M tetrazole to the reactor
    """
    await send_to_waste_rxn(instrument, "act")
    await wait_async(50)


@step
async def cap(instrument: Instrument) -> None:
    """
    Add acetic anhydride/pyridine/THF and N-methyl imidazole to the reactor
    """
    await send_to_waste_rxn(instrument, "cap1")
    await send_to_waste_rxn(instrument, "cap2")
    await wait_async(30)


@step
async def oxidize(instrument: Instrument) -> None:
    """
    Add 0.015 M iodine in water/pyridine/THF to the reactor
    """
    await send_to_waste_rxn(instrument, "oxi")
    await wait_async(45)


@step
async def cleave(instrument: Instrument) -> None:
    """
    Cleave the DNA sequence from the solid support.
    """
    await send_to_waste_rxn(instrument, "clde")
    await wait_async(180)


@step
async def deprotect(instrument: Instrument) -> None:
    """
    Remove the protecting groups from the DNA sequence.
    """
    await send_to_waste_rxn(instrument, "deb")
    await wait_async(45)


async def synthesize(instrument: Instrument, seq: Seq) -> None:
    """
    Synthesize a DNA sequence.

    args:
        seq: DNA sequence to synthesize.
    """
    logger.info("Initiating synthesis of DNA sequence: '%s'", seq)
    start_time = time()  # start timer
    with tqdm(total=len(seq) + 2) as pbar:
        await solvent_wash_all(instrument)
        await dry_all(instrument)

        pbar.update(1)

        for base_index, base in enumerate(seq):
            logger.info("Adding %sth base '%s' to growing DNA strand", base_index, base)

            await detritylate(instrument)

            await solvent_wash_all(instrument)
            await dry_all(instrument)

            await activate(instrument)

            await solvent_wash_all(instrument)
            await dry_all(instrument)

            await cap(instrument)

            await solvent_wash_all(instrument)
            await dry_all(instrument)

            await oxidize(instrument)

            await solvent_wash_all(instrument)
            await dry_all(instrument)

            await wait_async(1)
            pbar.update(1)

        await cleave(instrument)
        await deprotect(instrument)

        pbar.update(1)
    end_time = time()  # end timer
    elapsed_time_in_minutes = ((end_time - start_time) / 60) * utils.SIMULATION_SPEEDUP_FACTOR
    logger.info(
        "Synthesis complete for DNA sequence: '%s' in %s minutes", seq, elapsed_time_in_minutes
    )
