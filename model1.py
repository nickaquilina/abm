### TO DO
### TIMING
### TESTING

import math
import random
#import operator
import itertools
import matplotlib.pyplot as pyplot

# -----------------------------------------------------------------------------
# Debugging helper. With the global DEBUG set to False, a lot of debug printing
# is avoided.
DEBUG = False

def dbgprint(m):
    if DEBUG:
        print(m)
# -----------------------------------------------------------------------------

def gen_initial_coords(min_bound=0, max_bound=99):
    """ Function to generate the random initial co-ordinates within a grid.
        The default values are 0 & 99 for both x & y, however, these can be
        overridden.
    """
    dbgprint("Enter function: gen_initial_coords()")
    dbgprint(f"-- Mininum Bounds: {min_bound}")
    dbgprint(f"-- Maximum Bounds: {max_bound}")

    dbgprint("-- Generate 2 Random Integers")
    
    x_rand = random.randint(min_bound, max_bound)
    dbgprint(f"-- x: {x_rand}")
    
    y_rand = random.randint(min_bound, max_bound)
    dbgprint(f"-- y: {y_rand}")
    
    ret = [x_rand, y_rand]

    dbgprint(f"Return: {ret}\n")
    return [x_rand, y_rand]



def move_agent(xy_coords, overflow=100):
    """ This function accepts a list of x & Y coordinates. It increments or
        decrements each axis randomly by 1, and returns a list of [x, y]. This
        represents an agent moving on the grid.
    """
    dbgprint(f"Enter function: move_agent({xy_coords})")

    # Generate a random value between 0.0 and 1.0 for each value.
    c = []
    for val in xy_coords:
        dbgprint(f"-- Coordinate: {val}")
        rand = random.random()
        dbgprint(f"-- Random #: {rand}")
        #Torus overflow
        if rand < 0.5:
            val = (val + 1) % overflow
        else:
            val = (val - 1) % overflow
        dbgprint(f"-- New Value: {val}")
        c.append(val)

    dbgprint(f"Return: {c}\n")
    return c

# Tutor supplied
def distance_between(agents_row_a, agents_row_b):
    return (((agents_row_a[0] - agents_row_b[0])**2) + ((agents_row_a[1] - agents_row_b[1])**2))**0.5


def calc_distance(a1:[], a2:[]) -> float:
    """ Function accepts 2 sets of coordinates and calculates the Euclidean
        distance. a1 & a2 each represent a list of [x, y] coordinates, and 
        should be provided in the form [x, y]
    """
    """ Note on testing
        For testing, I used the code provided by the tutor, and ran an equality
        operator between the tutor's code and mine. I also saved a number of test
        values and the expected results.
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
    sqr_Dx = (a2[0] - a1[0])**2
    sqr_Dy = (a2[1] - a1[1])**2

    return math.sqrt(sqr_Dx + sqr_Dy)

def calc_distance_all(agents_list: []) -> []:
    """ Calculate the Eclidean distance between all agents. This excludes same
        agent calculations and is order agnostic.
    """
    results = []
    for agent1, agent2 in itertools.combinations(agents_list, 2):
        results.append([agent1, agent2, calc_distance(agent1, agent2)])

    return results    
    


def create_agents(num = 10):
    """ Function to create a number of 'agent' pairs of co-ordinates and return
        them in the form of a list of lists. Default is set to 10 pairs.
    """
    l_agents = []
    for x in range(num):
        l_agents.append(gen_initial_coords())
    
    return l_agents



# Define the number of agents, and iterations per agent
num_agents = 4
num_iterations = 10

# Generate a number of agents
agents = create_agents(num_agents)



    
    
    




"""

    
for agent in agents:
    pyplot.scatter(agent[0], agent[1], marker=".")
pyplot.show()





for x in range(num_iterations):
    print(f"Iteration: {x}")
    tmp = []
    for agent in agents:
        agent = move_agent(agent)
        tmp.append(agent)
    agents = tmp


    pyplot.ylim(0, 100)
    pyplot.xlim(0, 100)
    
    
    for a in agents:
        pyplot.scatter(a[0], a[1], marker=".")
    
    pyplot.show()
    





"""


# Print the largest based on the y coordinate
# print(max(agents, key=operator.itemgetter(1)))