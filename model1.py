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

y1 = 40
x1 = 40


def generate_movement(val: int) -> int:
    """ This function accepts a value (one of the coordinates) and returns
        either an increment, or decrement by 1
    """
    # Generate a random value between 0.0 and 1.0
    r = random.random()

    if r < 0.5:
        val += 1
    else:
        val -= 1    

    return val 


for x in range(10):
    y0 = generate_movement(y0)
    x0 = generate_movement(x0)
    y1 = generate_movement(y1)
    x1 = generate_movement(x1)
    print("(y0, x0): ({},{})".format(y0, x0))
    print("(y1, x1): ({},{})".format(y1, x1))
    
