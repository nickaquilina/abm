import math
import random
#import operator
import matplotlib.pyplot as pyplot

# -----------------------------------------------------------------------------
# Debugging helper. With the global DEBUG set to False, a lot of debug printing
# is avoided.
DEBUG = True

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


def calc_euclidean_dist(x0, x1, y0, y1):
    """ Function accepts 2 sets of coordinates and calculated the Euclidean
        distance.
    """
    sqr_Dx = (x1-x0)**2
    sqr_Dy = (y1-y0)**2

    return math.sqrt(sqr_Dx + sqr_Dy)


# Define the number of agents, and iterations per agent
num_agents = 10
num_iterations = 2

# Generate a number of agents
agents = []
#for x in range(1, num_agents + 1):
for x in range(num_agents):
    agents.append(gen_initial_coords())
print(agents)



pyplot.ylim(0, 99)
pyplot.xlim(0, 99)
    
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

    for a in agents:
        pyplot.scatter(a[0], a[1], marker=".")
    
    pyplot.show()
    








# Print the largest based on the y coordinate
# print(max(agents, key=operator.itemgetter(1)))