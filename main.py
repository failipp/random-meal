#! /usr/bin/env python3

import json
import random
from flask import Flask, redirect, render_template, url_for, request

from lib import Meal, Mealhandler

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chose_meal")
def startpage():
    global ms
    grenze = len(ms) // 2
    ml = list(enumerate(ms[:grenze]))
    print(ml)
    random.shuffle(ml)
    res = ml[:3]
    return render_template('main.html', meals=res)


@app.route("/eat_meal", methods=["post"])
def eat_meal():
    global ms
    meal = int(request.form['meal_id'])
    eaten = ms.pop(meal)
    ms.append(eaten)
    return redirect(url_for('startpage'))


if __name__ == '__main__':
    global ms
    with open("data.json", "r") as f:
        me = f.read()

    print(me)
    data = json.loads(me)
    mH = Mealhandler(data)
    # ms = [Meal.decode(x) for x in data]
    ms = mH._meals

    app.run(debug=True)
