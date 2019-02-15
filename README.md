# random-meal Generator

This tool should help you decide what you should make next time you eat something.

## Contents of this repo

- data.json contains examples of meals, with which this tool should be able to be executed
- main.py is currently the script you should execute, if you want to start this tool
- the lib folder contains the classes written for this tool

## How it works

You first need to create a database of meals you know.
Then this tool will randomly choose one (or more) of those meals for you,
but only from the ones you did not eat in the recent past.

## Planned features

- each meal has multiple informations (e.g. ingredients, type of meal)
- when randomly generating meals you can filter for those criteria (e.g. "i want a dessert")
- GUI through which it is also possible to edit the database
- Not only be able to randomly "eat" a meal, but to search for a specific one,
  so that it will move to the back in the database
