#!/usr/bin/env python
"""
A custom example synthesis protocol
"""
from Bio.Seq import Seq  # type: ignore
from tqdm import tqdm
from openoligo.utils import wait
from openoligo.steps.flow import solvent_wash_all, dry_all


def detritylate() -> None:
    print("Add 3% trichloroacetic acid in dichloromethane to the reactor")
    # send_to_reactor("3% trichloroacetic acid in dichloromethane")
    wait(1)


def activate() -> None:
    print("Add 0.1 M phosphoramidite monomer and 0.5 M tetrazole to the reactor")
    # send_to_reactor("0.1 M phosphoramidite monomer and 0.5 M tetrazole in acetonitrile")
    wait(1)


def cap() -> None:
    print("Add acetic anhydride/pyridine/THF and N-methyl imidazole to the reactor")
    # send_to_reactor("acetic anhydride/pyridine/THF and N-methyl imidazole")
    wait(1)


def oxidize() -> None:
    print("Add 0.015 M iodine in water/pyridine/THF to the reactor")
    # send_to_reactor("Oxidizing the DNA sequence")
    wait(1)


def cleave() -> None:
    print("Cleaving the DNA sequence from the solid support")
    # send_to_reactor("Cleaving the DNA sequence from the solid support")
    wait(1)


def deprotect() -> None:
    print("Removing protecting groups from the DNA sequence")
    # send_to_reactor("Removing protecting groups from the DNA sequence")
    wait(1)


def synthesize(seq: Seq) -> None:
    print("Initiating synthesis of DNA sequence: '%s'", seq)
    with tqdm(total=len(seq) + 2) as pbar:
        solvent_wash_all()
        dry_all()

        pbar.update(1)

        for base_index, base in enumerate(seq):
            print("Adding {}th base '{}' to growing DNA strand".format(base_index, base))

            detritylate()

            solvent_wash_all()
            dry_all()
            pbar.update(0.25)

            activate()

            solvent_wash_all()
            dry_all()
            pbar.update(0.25)

            cap()

            solvent_wash_all()
            dry_all()
            pbar.update(0.25)

            oxidize()

            solvent_wash_all()
            dry_all()
            pbar.update(0.25)

            wait(1)

        cleave()
        deprotect()

        pbar.update(1)

    print("Synthesis complete for DNA sequence: '{}'".format(seq))


if __name__ == "__main__":
    synthesize(Seq("ATCGAAATTTTT"))
    print("Done!")
