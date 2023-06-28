#!/usr/bin/env python
"""
A minimal example of using the DNA synthesis API.
"""
import asyncio
import logging

from Bio.Seq import Seq

from openoligo.instrument import Instrument
from openoligo.protocols.dna_synthesis import synthesize


async def main():
    inst = Instrument()
    await synthesize(inst, Seq("ATCGAAATTTTT"))


if __name__ == "__main__":
    try:
        asyncio.run(main())
        logging.info("Synthesis Complete! Exiting...")
    except KeyboardInterrupt:
        logging.warning("Keyboard interrupt received, exiting...")
    except Exception as e:
        logging.error(e)
