#! /usr/bin/env python3

import json
import random

from lib import Meal

if __name__ == "__main__":
    with open("data.json", "r") as f:
        me = f.read()

    data = json.loads(me)
    ms = [Meal.decode(x) for x in data]

    random.shuffle(ms)
    print(ms)

    try:
        while True:
            grenze = len(ms) // 2
            rint = random.randint(0, grenze)

            zu_kochen = ms.pop(rint)

            print(zu_kochen)
            ms.append(zu_kochen)
            print(ms, end="")

            input()
    except KeyboardInterrupt:
        print("Loop End")
