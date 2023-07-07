#!/usr/bin/env python
"""
A minimal example of using the DNA synthesis API.
"""
import asyncio

from openoligo.hal.instrument import Instrument
from openoligo.protocols.oligosynthesis import synthesize_ssdna
from openoligo.seq import Seq
from openoligo.utils.logger import OligoLogger

rl = OligoLogger(rotates=False)
logger = rl.get_logger()


def main():
    inst = Instrument()

    try:
        asyncio.run(synthesize_ssdna(inst, Seq("ATCGAAATTTTT")))
        logger.info("Synthesis Complete! Exiting...")
    except KeyboardInterrupt:
        logger.warning("Keyboard interrupt received, exiting...")
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()
