# OpenOligo

[![Lint OpenOligo](https://github.com/TechnocultureResearch/OpenOligo/actions/workflows/lint.yaml/badge.svg)](https://github.com/TechnocultureResearch/OpenOligo/actions/workflows/lint.yaml) 
[![PyPI version](https://badge.fury.io/py/openoligo.svg)](https://badge.fury.io/py/openoligo)

OpenOligo is an open-source platform for programmatically interacting with and managing DNA synthesis processes.

## Getting Started
```sh
pip install openoligo
```

### A simple Example

```py
from time import sleep
from openoligo import Manifold, MockValve

m = Manifold(MockValve, 4)

m.one_hot(3)
wait(ms(300))
m.one_hot(2)
wait(1)

print(m)
```
