from openoligo import Manifold, MockValve, ms, wait


def main():
    m = Manifold(MockValve, 4)

    m.one_hot(3)
    wait(ms(300))
    m.one_hot(2)
    wait(1)

    print(m)


if __name__ == "__main__":
    main()
