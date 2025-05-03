import numpy as np
from scipy.optimize import least_squares


"""
for now:
randomly select pixels
make calculate_speed work
run

choose specific sub areas
use roads as mask
split into training and testing

"""


def calculate_speed(coord, params):
    # query database for all overlaps in that pixel
    #multuply each by param value
    #scale and return
    return 1

def get_weiss_value(coord):
    #return value from dictionary
    pass


# set of corrordinates to compare
coordinate_data = np.array([
    (1.0, 2.0),
    (2.5, 3.1),
    (0.5, 4.2)
])

# Input and output data
truth = np.array(list(map(get_weiss_value, coordinate_data)))


def residuals(params):
    sample = np.array([calculate_speed(coord, params) for coord in coordinate_data])
    return sample - truth


# Initial guess: 30 parameters
initial_guess = np.ones(30)
result = least_squares(residuals, initial_guess, loss='linear')  # use 'soft_l1' for robustness
print("Optimized parameters:", result.x)
