# OpenOligo

[![PyPI version](https://badge.fury.io/py/openoligo.svg)](https://badge.fury.io/py/openoligo)
![Coverage](./.github/coverage.svg)
[![Lint OpenOligo](https://github.com/TechnocultureResearch/OpenOligo/actions/workflows/lint.yaml/badge.svg)](https://github.com/TechnocultureResearch/OpenOligo/actions/workflows/lint.yaml)
[![Test OpenOligo](https://github.com/TechnocultureResearch/OpenOligo/actions/workflows/test.yaml/badge.svg)](https://github.com/TechnocultureResearch/OpenOligo/actions/workflows/test.yaml)

OpenOligo is an open-source platform for programmatically interacting with and managing DNA synthesis processes.

## Getting Started
```sh
pip install openoligo
```

### A simple Example

```py
from openoligo import Manifold, MockValve
from openoligo.steps import perform_flow_sequence
from openoligo.utils import ms

m = Manifold(MockValve, 4)

perform_flow_sequence(
    m,
    [
        (0, ms(100)),
        (2, 1),
        (1, ms(200)),
    ],
)
```
