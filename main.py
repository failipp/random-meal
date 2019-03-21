#! /usr/bin/env python3

import random

from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

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
    meals = [
        (ml[0], MEALS.find_one({"_id": ml[0]})["name"]),
        (ml[1], MEALS.find_one({"_id": ml[1]})["name"]),
        (ml[2], MEALS.find_one({"_id": ml[2]})["name"]),
    ]
    return render_template('main.html', meals=meals)


@app.route("/eat_meal", methods=["post"])
def eat_meal():
    meal = request.form['meal_id']
    print(f"This is the meal: {meal}")
    ms = MEAL_SEQUENCE.find_one({"_id": 0})["meal_sequence"]
    eaten = ms.pop(ms.index(meal))
    ms.append(eaten)
    MEAL_SEQUENCE.update_one({"_id": 0}, {"$set": {"meal_sequence": ms}})
    return redirect(url_for('startpage'))


@app.route("/all_meals")
def all_meals():
    allmeals = [(x['_id'], x) for x in sorted(MEALS.find(), key=lambda x: x['name'])]
    return render_template("all-meals.html", allmeals=allmeals)


@app.route("/edit_meal", methods=['post'])
def edit_meal():
    pass


if __name__ == '__main__':
    app.run(debug=True)
