#!/usr/bin/env python

from openoligo import Board, RPi


def main():
    with Board() as b:
        print(b)
        b.setup()
        print(b)
        b.set(RPi.PIN3, True)
        b.set(RPi.PIN5, True)
        b.set(RPi.PIN7, True)
        print(b)


if __name__ == "__main__":
    main()
