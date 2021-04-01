import random

""" Model:
    # Make a y variable.
    # Make a x variable.
    # Change y and x based on random numbers.
    # Make a second set of y and xs, and make these change randomly as well.
    # Work out the distance between the two sets of y and xs.
"""


y0 = 50
x0 = 50

y1 = 50
x1 = 50


def gen_coordinates(y: int, x: int) -> ():
    """ This function accepts two integers representing y,x coordinates, and
        returns new coordinates, incremented or decremented by 1.
    """
    # Generate a random value between 0.0 and 1.0
    y_rand = random.random()
    x_rand = random.random()
    
    print("y_rand: {}".format(y_rand))
    print("x_rand: {}".format(x_rand))

    if y_rand < 0.5:
        y += 1
    else:
        y -= 1    

    if x_rand < 0.5:
        x += 1
    else:
        x -= 1    

    return (x, y)


print("(y0, x0): ({},{})".format(y0, x0))
print("(y1, x1): ({},{})".format(y1, x1))

# Move the agents 2 times

y0, x0 = gen_coordinates(y0, x0)
y0, x0 = gen_coordinates(y0, x0)

y1, x1 = gen_coordinates(y1, x1)
y1, x1 = gen_coordinates(y1, x1)
   
print("(y0, x0): ({},{})".format(y0, x0))
print("(y1, x1): ({},{})".format(y1, x1))
    
