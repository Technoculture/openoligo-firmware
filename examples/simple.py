#!/usr/bin/env python

"""
 Run the following command in order to run this example:
      poetry run python examples/simple.py
 Or,
      poetry shell # to enter the virtual environment
      python examples/simple.py
 Or,
      cd examples
      ./simple.py
"""

import logging

from openoligo import Manifold, Valve
from openoligo.utils import ms

logging.basicConfig(level=logging.DEBUG)


def main():
    m = Manifold(Valve, 4)


if __name__ == "__main__":
    main()
