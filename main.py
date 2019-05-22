#! /usr/bin/env python3

import random
from datetime import datetime

from bson.objectid import ObjectId
from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient

app = Flask(__name__)
database = MongoClient()["random_meal_generator"]
MEALS = database["meals"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chose_meal")
def startpage():
    # Sorted meals in mongodb (key: datetime in last_time_eaten)
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
    allmeals = [(str(x['_id']), x) for x in sorted(MEALS.find(), key=lambda x: x['name'])]
    return render_template("all-meals.html", allmeals=allmeals)


@app.route("/edit_meal", methods=['post'])
def edit_meal():
    meal_id = request.form['meal_id']
    if meal_id == "0":
        meal_id = str(ObjectId())
    meal = MEALS.find_one({'_id': ObjectId(meal_id)})
    if meal is None:
        return render_template("edit-meal.html", meal_id=meal_id, meal={})
    ingredients = ", ".join(meal['ingredients'])
    return render_template("edit-meal.html", meal_id=meal_id, meal=meal, ingredients=ingredients)


@app.route("/update_meal", methods=["post"])
def update_meal():
    # TODO: Properties to add to a meal:
    #  - Additional information (textbox) DONE
    #  - Rating
    #  - Category / Tags (e.g. vegetarian, dessert, warm/cold, italian, ...)
    # TODO: Further properties?
    #  - Ingredients: Include in tags? Amount of ingredient? Manage in seperate collection?
    meal_id = request.form['meal_id']
    meal_name = request.form['meal_name']
    meal_difficulty = int(request.form['meal_difficulty'])
    meal_ingredients = request.form['meal_ingredients'].split(", ")
    meal_info = request.form['meal_info']
    MEALS.update_one({'_id': ObjectId(meal_id)},
                     {'$set': {'name': meal_name, 'difficulty': meal_difficulty, 'ingredients': meal_ingredients,
                               'additional_info': meal_info},
                      "$setOnInsert": {"last_time_eaten": datetime.now().isoformat()}},
                     upsert=True)
    if meal_info == "":
        MEALS.update_one({'_id': ObjectId(meal_id)}, {'$unset': {'additional_info': 1}})

    return redirect(url_for('all_meals'))


if __name__ == '__main__':
    app.run(debug=True)
