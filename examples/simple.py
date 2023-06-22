#!/usr/bin/env python

from openoligo import Manifold, MockValve
from openoligo.utils import ms, with_wait


def main():
    m = Manifold(MockValve, 4)

    with_wait(m.activate_flow(3), 2)
    print("Flow 3: Activated")
    with_wait(m.activate_flow(0), ms(300))
    print("Flow 0: Activated")
    with_wait(m.activate_flow(2), 1)
    print("Flow 2: Activated")


if __name__ == "__main__":
    main()
