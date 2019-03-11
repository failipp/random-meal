#! /usr/bin/env python3

import json
import random
from flask import Flask, redirect, render_template, url_for
from pymongo import MongoClient

from lib import Meal, Mealhandler

app = Flask(__name__)
database = MongoClient()["random_meal_generator"]
MEALS = database["meals"]
MEAL_SEQUENCE = database["meal_sequence"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chose_meal")
def startpage():
    ms = MEAL_SEQUENCE.find_one({"_id": 0})["meal_sequence"]
    grenze = len(ms) // 2
    ml = ms[:grenze]
    print(ml)
    random.shuffle(ml)
    res = ml[:3]
    meals = [
        (ml[0], MEALS.find_one({"_id": ml[0]})["name"]),
        (ml[1], MEALS.find_one({"_id": ml[1]})["name"]),
        (ml[2], MEALS.find_one({"_id": ml[2]})["name"]),
    ]
    return render_template('main.html', meals=meals)


@app.route("/eat_meal/<meal>/", methods=["post"])
def eat_meal(meal):
    ms = MEAL_SEQUENCE.find_one({"_id": 0})["meal_sequence"]
    eaten = ms.pop(ms.index(meal))
    ms.append(eaten)
    MEAL_SEQUENCE.update_one({"_id": 0}, {"$set": {"meal_sequence": ms}})
    return redirect(url_for('startpage'))


if __name__ == '__main__':
    # global ms
    # with open("data.json", "r") as f:
    #     me = f.read()
    #
    # print(me)
    # data = json.loads(me)
    # mH = Mealhandler(data)
    # # ms = [Meal.decode(x) for x in data]
    # ms = mH._meals

    app.run(debug=True)
