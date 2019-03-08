#! /usr/bin/env python3

from lib.meal import Meal


class Mealhandler:
    _meals = []

    def __init__(self, data_dict):
        if isinstance(data_dict, dict):
            if "meals" not in data_dict:
                raise KeyError("data_dict needs key 'meals'")

            # TODO check for correct type of keys "meals" and "last_time_eaten" or not?
            self._meals = [Meal.decode(m) for m in data_dict["meals"]]

            if "last_time_eaten" in data_dict:
                self._sort_meals(data_dict["last_time_eaten"])
            else:
                self._sort_meals([])

        else:
            raise TypeError("data_dict has to be a dictionary")

    @property
    def meals(self):
        return self._meals

    def filter(self, **kwargs):
        filtered_meals = self.meals[:]
        for key in kwargs:
            print(f"{hasattr(Meal, key)}")
            if hasattr(Meal, key):
                # TODO: Add searching for one keyword in attribute that is list
                if isinstance(kwargs[key], list):
                    multi_filters = [m for m in filtered_meals if getattr(m, key) in kwargs[key]]
                else:
                    multi_filters = None

                filtered_meals = [m for m in filtered_meals if getattr(m, key) == kwargs[key]]

                if multi_filters is not None:
                    filtered_meals.extend(multi_filters)

        return filtered_meals

    def _sort_meals(self, last_time_eaten):
        # TODO: remove type checking?
        if not isinstance(last_time_eaten, list):
            raise TypeError("last_time_eaten must be list")

        for n in last_time_eaten[:]:
            if n not in [m.name for m in self._meals]:
                last_time_eaten.remove(n)

        if len(last_time_eaten) < len(self._meals):
            for n in [m.name for m in self._meals]:
                if n not in last_time_eaten:
                    last_time_eaten.insert(0, n)

        if len(last_time_eaten) != len(self._meals):
            raise ValueError("Configuration borked")

        print(last_time_eaten)
        print(self._meals)

        tmp = self._meals[:]
        for m in tmp:
            self._meals[last_time_eaten.index(m.name)] = m

        print(self._meals)

    def export(self):
        data_dict = {
            "meals":
                sorted([m.encode() for m in self._meals], key=lambda x: x["name"]),
            "last_time_eaten": [m.name for m in self._meals]
        }

        return data_dict
