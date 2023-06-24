#!/usr/bin/env python
"""
A minimal example of using the DNA synthesis API.
"""
from openoligo.protocols.dna_synthesis import synthesize


def main():
    synthesize("ATCGAAATTTTT")


if __name__ == "__main__":
    main()
