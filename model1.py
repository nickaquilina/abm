import math
import random

""" Model:
    # Make a y variable.
    # Make a x variable.
    # Change y and x based on random numbers.
    # Make a second set of y and xs, and make these change randomly as well.
    # Work out the distance between the two sets of y and xs.
"""


def gen_coordinates(x, y):
    """ This function accepts two integers representing y,x coordinates, and returns new
        coordinates, incremented, or decremented by 1.
    """
    # Generate a random value between 0.0 and 1.0
    x_rand = random.random()
    y_rand = random.random()

    print("x_rand: {}".format(x_rand))
    print("y_rand: {}".format(y_rand))

    if x_rand < 0.5:
        x += 1
    else:
        x -= 1

    if y_rand < 0.5:
        y += 1
    else:
        y -= 1

    return (x, y)


def calc_euclidean_dist(x0, x1, y0, y1):
    """ Function accepts 2 sets of coordinates and calculated the Euclidean
        distance.
    """
    sqr_Dx = (x1-x0)**2
    sqr_Dy = (y1-y0)**2

    return math.sqrt(sqr_Dx + sqr_Dy)


def gen_initial_coords(min_bound=0, max_bound=99):
    """ Function to generate the random initial co-ordinates within a grid. The default
        values are 0 & 99 for both x & y, however, these can be overridden.
    """
    x_rand = random.randint(min_bound, max_bound)
    y_rand = random.randint(min_bound, max_bound)

    return(x_rand, y_rand)


# Generate the initial coordinates
x0, y0 = gen_initial_coords()
x1, y1 = gen_initial_coords()


print(f"({x0}, {y0})")
print(f"({x1}, {y1})")

# Move the agents 2 times
x0, y0 = gen_coordinates(x0, y0)
x0, y0 = gen_coordinates(x0, y0)

x1, y1 = gen_coordinates(x1, y1)
x1, y1 = gen_coordinates(x1, y1)

print(f"(x0, y0): ({x0},{y0})")
print(f"(x1, y1): ({x1},{y1})")


distance = calc_euclidean_dist(x0, x1, y0, y1)

print(f"Distance: {distance}")
