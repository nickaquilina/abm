""" This file contains the main Agent Class.
"""
import random


class Agent():
    def __init__(self, environment):
        self._x = random.randint(0, 99)
        self._y = random.randint(0, 99)
        self.environment = environment
        self.store = 0
        self.overflow = 100

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = val

    def eat(self): # can you make it eat what is left?
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10


    def _move(self, val):
        rand = random.random()
        #This caters for the Torus overflow.
        if rand < 0.5:
            val = (val + 1) % self.overflow
        else:
            val = (val - 1) % self.overflow

        return val

    def move(self):
        self.x = self._move(self.x)
        self.y = self._move(self.y)


    def getCoordinates(self):
        return self.x, self.y

