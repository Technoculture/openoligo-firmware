# OpenOligo

[![PyPI version](https://badge.fury.io/py/openoligo.svg)](https://badge.fury.io/py/openoligo)
![Coverage](https://raw.githubusercontent.com/TechnocultureResearch/OpenOligo/dev/.github/coverage.svg)
[![Lint OpenOligo](https://github.com/TechnocultureResearch/OpenOligo/actions/workflows/lint.yaml/badge.svg)](https://github.com/TechnocultureResearch/OpenOligo/actions/workflows/lint.yaml)
[![Test OpenOligo](https://github.com/TechnocultureResearch/OpenOligo/actions/workflows/test.yaml/badge.svg)](https://github.com/TechnocultureResearch/OpenOligo/actions/workflows/test.yaml)

OpenOligo is an open-source platform for programmatically interacting with and managing DNA synthesis processes.

## Getting Started
```sh
pip install openoligo
```

### A simple Example

```py
import asyncio

from openoligo.instrument import Instrument
from openoligo.protocols.oligosynthesize import synthesize_ssdna
from openoligo.seq import Seq


inst = Instrument()

try:
    asyncio.run(synthesize_ssdna(inst, Seq("ATCGAAATTTTT")))
except KeyboardInterrupt:
    print("Keyboard interrupt received, exiting...")
```

## Firmware
The firmware for OpenOligo is composed of 
- OpenOligo Library
- API server (part of OpenOligo Library)
- In a minimal linux image ([OligoOS](https://github.com/Technoculture/OligoOs/tree/dev))
