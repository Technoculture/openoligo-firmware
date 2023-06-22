from openoligo import Manifold, MockValve, ms, wait


def main():
    m = Manifold(MockValve, 4)

    m.activate_flow(3)
    wait(ms(300))
    m.activate_flow(2)
    wait(1)

    print(m)


if __name__ == "__main__":
    main()
