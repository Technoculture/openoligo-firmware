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

from openoligo import Manifold, MockValve
from openoligo.steps import perform_flow_sequence
from openoligo.utils import ms

logging.basicConfig(level=logging.DEBUG)


def main():
    m = Manifold(MockValve, 4)

    perform_flow_sequence(
        m,
        [
            (0, ms(100)),
            (2, 1),
            (1, ms(200)),
        ],
    )


if __name__ == "__main__":
    main()
