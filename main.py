#! /usr/bin/env python3

import random
from datetime import datetime

from bson import ObjectId
from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
database = MongoClient()["random_meal_generator"]
MEALS = database["meals"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chose_meal")
def startpage():
    # All meals in mongodb sorted regarding to datetime in last_time_eaten
    list_of_meals = sorted(MEALS.find(), key=lambda x: x['last_time_eaten'])
    grenze = len(list_of_meals) // 2
    ml = list_of_meals[:grenze]
    print([x['name'] for x in ml])
    random.shuffle(ml)
    meals = [(str(meal['_id']), meal['name']) for meal in ml]
    if len(meals) > 3:
        meals = meals[:3]

    return render_template('main.html', meals=meals)


@app.route("/eat_meal", methods=["post"])
def eat_meal():
    meal = request.form['meal_id']
    print(f"This is the meal: {meal}")
    MEALS.update_one({'_id': ObjectId(meal)}, {'$set': {'last_time_eaten': datetime.now().isoformat()}})
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
