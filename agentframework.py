""" This file contains the main Agent Class.
"""
import random


class Agent():
    def __init__(self, environment, xLim, yLim):
        self.environment = environment
        self.xLim = xLim
        self.yLim = yLim

        self._x = random.randint(0, (self.xLim - 1))
        self._y = random.randint(0, (self.yLim - 1))
        self.store = 0


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
        else:
            remainder = self.environment[self.y][self.x]
            self.environment[self.y][self.x] -= remainder
            self.store += remainder

        # Sick Up
        if self.store > 100:
            ##print(f"Sicking Up: {self.store}")
            self.environment[self.y][self.x] += self.store
            self.store = 0
            ##print(f"Store: {self.store}")


    def _move(self, val, overflow):
        rand = random.random()
        #This caters for the Torus overflow.
        if rand < 0.5:
            val = (val + 1) % overflow
        else:
            val = (val - 1) % overflow

        return val

    def move(self):
        self.x = self._move(self.x, self.xLim)
        self.y = self._move(self.y, self.yLim)


    def getCoordinates(self):
        return self.x, self.y

