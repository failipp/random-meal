#! /usr/bin/env python3


class Meal:
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        if not isinstance(n, str):
            raise TypeError("name expected a string")
        if n == "":
            raise ValueError("name is not allowed to be an empty string")
        self._name = n

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, d):
        if not isinstance(d, int):
            raise TypeError("difficulty expected a string")
        if not 0 < d <= 5:
            # 1: for everybody; 2: easy; 3: medium; 4: hard; 5: impossible
            raise ValueError("difficulty should be from 1 to 5")
        self._difficulty = d

    def __repr__(self):
        return self.name
