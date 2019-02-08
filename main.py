#! /usr/bin/env python3

import random
from lib import Meal


def main():
    pf = Meal("Pfannkuchen", 2)
    ks = Meal("Kaiserschmarrn", 3)
    sp = Meal("Spaghetti", 1)
    ca = Meal("Canneloni", 4)
    pi = Meal("Pizza", 2)
    ka = Meal("Kässpatzen", 4)
    bu = Meal("Burger", 5)

    ms = [pf, ks, sp, ca, pi, ka, bu]
    random.shuffle(ms)

    while True:
        grenze = len(ms) // 2
        rint = random.randint(0, grenze)

        zu_kochen = ms.pop(rint)

        print(zu_kochen)
        ms.append(zu_kochen)

        input()


if __name__ == "__main__":
    main()
