#! /usr/bin/env python3

import json
import random
from flask import Flask

from lib import Meal, Mealhandler

app = Flask(__name__)

if __name__ == "__main__":
    with open("data.json", "r") as f:
        me = f.read()

    print(me)
    data = json.loads(me)
    mH = Mealhandler(data)
    # ms = [Meal.decode(x) for x in data]
    ms = mH._meals

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

    to_write = json.dumps(mH.export(),
                          ensure_ascii=False,
                          indent=4)

    with open("data.json", "w") as f:
        f.write(to_write)
