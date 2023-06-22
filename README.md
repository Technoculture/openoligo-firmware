# OpenOligo

[![Lint OpenOligo](https://github.com/TechnocultureResearch/OpenOligo/actions/workflows/lint.yaml/badge.svg)](https://github.com/TechnocultureResearch/OpenOligo/actions/workflows/lint.yaml) 
[![PyPI version](https://badge.fury.io/py/openoligo.svg)](https://badge.fury.io/py/openoligo)
![Coverage](./.github/coverage.svg)

OpenOligo is an open-source platform for programmatically interacting with and managing DNA synthesis processes.

## Getting Started
```sh
pip install openoligo
```

### A simple Example

```py
from openoligo import Manifold, MockValve
from openoligo.utils import wait, ms

m = Manifold(MockValve, 4)

m.activate_flow(3)
wait(ms(300))
m.activate_flow(2)
wait(1)

print(m)
```
