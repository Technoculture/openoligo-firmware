#!/usr/bin/env python
"""
A minimal example of using the DNA synthesis API.
"""
import asyncio

from Bio.Seq import Seq

from openoligo.protocols.dna_synthesis import synthesize


async def main():
    await synthesize(Seq("ATCGAAATTTTT"))


if __name__ == "__main__":
    asyncio.run(main())
