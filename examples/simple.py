from time import sleep

from openoligo import Manifold, MockValve


def main():
    m = Manifold(MockValve, 4)

    m.one_hot(3)
    sleep(1)
    m.one_hot(2)
    sleep(2)

    print(m)


if __name__ == "__main__":
    main()
