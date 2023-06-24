"""
DNA Snthesis Protocol
"""
import logging
from Bio.Seq import Seq  # type: ignore
from tqdm import tqdm
from openoligo.utils import wait
from openoligo.steps.flow import solvent_wash_all, dry_all


def detritylate() -> None:
    """
    Remove the trityl group from the 5'-end of the DNA sequence.
    Involves the reagent to be sent to the reactor, and then the reactor to be washed and dried.
    """
    logging.debug("Add 3% trichloroacetic acid in dichloromethane to the reactor")
    # send_to_reactor("3% trichloroacetic acid in dichloromethane")
    wait(1)


def activate() -> None:
    """
    0.1 M phosphoramidite monomer and 0.5 M tetrazole in acetonitrile
    """
    logging.debug("Add 0.1 M phosphoramidite monomer and 0.5 M tetrazole to the reactor")
    # send_to_reactor("0.1 M phosphoramidite monomer and 0.5 M tetrazole in acetonitrile")
    wait(1)


def cap() -> None:
    """
    acetic anhydride/pyridine/THF 1/1/8 and 17.6% w/v N-methyl imidazole in acetonitrile
    """
    logging.debug("Add acetic anhydride/pyridine/THF and N-methyl imidazole to the reactor")
    # send_to_reactor("acetic anhydride/pyridine/THF and N-methyl imidazole")
    wait(1)


def oxidize() -> None:
    """
    Oxidize the DNA sequence.
    0.015 M iodine in water/pyridine/THF 2/20/78
    """
    logging.debug("Add 0.015 M iodine in water/pyridine/THF to the reactor")
    # send_to_reactor("Oxidizing the DNA sequence")
    wait(1)


def cleave() -> None:
    """
    Cleave the DNA sequence from the solid support.
    """
    logging.debug("Cleaving the DNA sequence from the solid support")
    # send_to_reactor("Cleaving the DNA sequence from the solid support")
    wait(1)


def deprotect() -> None:
    """
    Remove the protecting groups from the DNA sequence.
    """
    logging.debug("Removing protecting groups from the DNA sequence")
    # send_to_reactor("Removing protecting groups from the DNA sequence")
    wait(1)


def synthesize(seq: Seq) -> None:
    """
    Synthesize a DNA sequence.

    args:
        seq: DNA sequence to synthesize.
    """
    logging.debug("Initiating synthesis of DNA sequence: '%s'", seq)
    with tqdm(total=len(seq) + 2) as pbar:
        solvent_wash_all()
        dry_all()

        pbar.update(1)

        for base_index, base in enumerate(seq):
            logging.debug("Adding %sth base '%s' to growing DNA strand", base_index, base)

            detritylate()

            solvent_wash_all()
            dry_all()

            activate()

            solvent_wash_all()
            dry_all()

            cap()

            solvent_wash_all()
            dry_all()

            oxidize()

            solvent_wash_all()
            dry_all()

            wait(1)
            pbar.update(1)

        cleave()
        deprotect()

        pbar.update(1)

    logging.debug("Synthesis complete for DNA sequence: '%s'", seq)
