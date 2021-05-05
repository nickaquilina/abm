""" This is the main Agent Framework file (and Class). All operations related to the Agent
    movement and related states are contained.
"""
import math
import random


class Agent():
    def __init__(self, environment, xLim, yLim, allAgents, logger, x=None, y=None):
        """ If the x & y variables are populated, the agent is created using the incoming
            x & y values. Otherwise, coordinates are auto-generated. Since the state are
            retained for each agent, it is quite possible, for example to add logic in the
            main model, where some agents have different speeds (for moving). For example
            in a model with sheep and wolves, the wolves can have 3 * the move capacity of
            the sheep.
        """
        self.logger = logger
        self.environment = environment
        self.allAgents = allAgents
        self.xLim = xLim
        self.yLim = yLim
        if x is not None:
            self._x = int(x)
        else:
            self._x = random.randint(0, (self.xLim - 1))

        if y is not None:
            self._y = int(y)
        else:
            self._y = random.randint(0, (self.yLim - 1))

        self.store = 0
        self.logger.debug(f"Agent inited - {id(self)}")
        self.logger.debug(f"Agents: {len(self.allAgents)}")
        self.logger.debug(f"xLim: {type(self.xLim)} - {self.xLim}")
        self.logger.debug(f"yLim: {type(self.yLim)} - {self.yLim}")
        self.logger.debug(f"x: {self.x}")
        self.logger.debug(f"y: {self.y}")


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


    def eat(self):
        """ This function removes the resources from the environment and transfers them to
            the Agent's account. The agent can never take out resources more than present.
            When agents eat too much, the resources on the agent's account are added to
            the environment again, to a different location on the map due to wandering.
        """
        self.logger.debug(f"Agent {id(self)} ate 10 resources.")
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
        else:
            remainder = self.environment[self.y][self.x]
            self.environment[self.y][self.x] -= remainder
            self.store += remainder
            self.logger.debug(f"Agent {id(self)} ate {remainder} resources.")
            self.logger.debug(f"Co-ordinate ({self.x},{self.y}) depleted")

        if self.store > 100:
            self.logger.debug(f"Agent {id(self)} has more than 100 resources.")
            self.environment[self.y][self.x] += self.store
            self.logger.debug((f"Agent {id(self)} moved {self.store} resources "
                              f"on to ({self.x},{self.y})"))
            self.store = 0


    def calculateDistance(self, otherAgent):
        """ Function accepts 2 sets of coordinates and calculates the Euclidean distance.
            Since this only calculates, it was easy to test using pre-determined values
            and comparing the results.
            test_data = [[[47, 58], [70, 95], 43.56604182158393],
                         [[47, 58], [47, 58], 0.0],
                         [[47, 58], [25, 20], 43.9089968002003],
                         [[25, 20], [70, 95], 87.46427842267951],
                         [[25, 20], [47, 58], 43.9089968002003],
                         [[44, 42], [70, 95], 59.033888572581766],
                         [[44, 42], [47, 58], 16.278820596099706],
                         [[37, 19], [70, 95], 82.85529554590944],
                         [[37, 19], [47, 58], 40.26164427839479],
                         [[37, 19], [25, 20], 12.041594578792296]]
        """
        sqr_Dx = (otherAgent.x - self.x)**2
        sqr_Dy = (otherAgent.y - self.y)**2

        return math.sqrt(sqr_Dx + sqr_Dy)


    def shareWithNeighbours(self, neighbours):
        """ Function calculates distance between "this" and the other agents in order to
            share resources with agents close by. This could easily be used, for example
            for represenging one type of agent consuming another type of agent.
        """
        for otherAgent in self.allAgents:
            # comparing IDs, so that agents do not share with self. In reality, without
            # this logic, values would still remain the same since averaging with self
            # does not change the value in question.
            if id(self) == id(otherAgent):
                self.logger.debug("Agent ids identical. No need to share with self.")
            else:
                dist = self.calculateDistance(otherAgent)
                if dist <= neighbours:
                    avg = (self.store + otherAgent.store) / 2
                    self.store = avg
                    otherAgent.store = avg
                    self.logger.debug(f"Agent {id(self)} shared resorces with {id(otherAgent)}")


    def _move(self, val, limit):
        """ Function to generate new co-ordinates for an agent to move in the 2D space.
            The function is used for both x & y co-ordinates, and receives the current
            location and the limit related to that location.
        """
        rand = random.random()
        # This also caters for the Torus overflow. If the move passes beyond the limit,
        # the agent moves to the start of that axis again.
        if rand < 0.5:
            val = (val + 1) % limit
        else:
            val = (val - 1) % limit

        return val

    def move(self):
        self.x = self._move(self.x, self.xLim)
        self.y = self._move(self.y, self.yLim)


    def getCoordinates(self):
        """ Simply return the x & y coordinates for the self agent instance
        """
        return self.x, self.y
