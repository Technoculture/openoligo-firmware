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
from openoligo.protocols.dna_synthesis import synthesize
from openoligo.seq import Seq


inst = Instrument()

try:
    asyncio.run(synthesize(inst, Seq("ATCGAAATTTTT")))
except KeyboardInterrupt:
    print("Keyboard interrupt received, exiting...")
```
