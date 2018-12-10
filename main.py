import requests
import math
import random
import csv
import json
import os.path
import pandas as pd
import datetime
from matplotlib import pyplot as plt
from sklearn import datasets, linear_model

API_KEY = '2520FD98-BA2D-356A-8A02-9FE608339890'
GET_URL = 'http://quickstats.nass.usda.gov/api/api_GET' # url to request data from
SHORT_DESC = 'TURKEYS, YOUNG, SLAUGHTER, FI - SLAUGHTERED, MEASURED IN HEAD' # description of data wanted
STATE = 'VA'
YEAR_GE = '1989' # greater than / equal to year
YEAR_LE = '2018' # less than / equal to year
FORMAT = 'CSV'
DATA_FILE = 'turkey.csv' # save file
GET_PARAMS = { # params to specifiy request
    'key' : API_KEY,
    'year__GE' : YEAR_GE,
    'year__LE' : YEAR_LE,
    'state_alpha' : STATE,
    'short_desc' : SHORT_DESC,
    'format' : FORMAT
    }

'''
Simple Linear Regression Code from the TextBook.
'''
def mean(x):
    return sum(x) / len(x)

def scalar_multiply(c, v):
    return [c * v_i for v_i in v]

def dot(v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

def sum_of_squared_errors(alpha, beta, x, y):
    return sum(error(alpha, beta, x_i, y_i) ** 2
               for x_i, y_i in zip(x, y))

def vector_subtract(v, w):
    """subtracts two vectors componentwise"""
    return [v_i - w_i for v_i, w_i in zip(v,w)]

def sum_of_squares(v):
    """computes the sum of squared elements in v"""
    return sum(v_i ** 2 for v_i in v)

def de_mean(x):
    """translate x by subtracting its mean (so the result has mean 0)"""
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]

def variance(x):
    """assumes x has at least two elements"""
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n - 1)

def standard_deviation(x):
    return math.sqrt(variance(x))

def covariance(x, y):
    n = len(x)
    return dot(de_mean(x), de_mean(y)) / (n - 1)



def correlation(x, y):
    stdev_x = standard_deviation(x)
    stdev_y = standard_deviation(y)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(x, y) / stdev_x / stdev_y
    else:
        return 0 # if no variation, correlation is zero

def predict(alpha, beta, x_i):
    return beta * x_i + alpha

def error(alpha, beta, x_i, y_i):
    return y_i - predict(alpha, beta, x_i)

def sum_of_squared_errors(alpha, beta, x, y):
    return sum(error(alpha, beta, x_i, y_i) ** 2
               for x_i, y_i in zip(x, y))

def least_squares_fit(x,y):
    """given training values for x and y,
    find the least-squares values of alpha and beta"""
    beta = correlation(x, y) * standard_deviation(y) / standard_deviation(x)
    alpha = mean(y) - beta * mean(x)
    return alpha, beta

def total_sum_of_squares(y):
    """the total squared variation of y_i's from their mean"""
    return sum(v ** 2 for v in de_mean(y))

def r_squared(alpha, beta, x, y):
    """the fraction of variation in y captured by the model, which equals
    1 - the fraction of variation in y not captured by the model"""

    return 1.0 - (sum_of_squared_errors(alpha, beta, x, y) /
                  total_sum_of_squares(y))

def squared_error(x_i, y_i, theta):
    alpha, beta = theta
    return error(alpha, beta, x_i, y_i) ** 2

def squared_error_gradient(x_i, y_i, theta):
    alpha, beta = theta
    return [-2 * error(alpha, beta, x_i, y_i),       # alpha partial derivative
            -2 * error(alpha, beta, x_i, y_i) * x_i] # beta partial derivative

def negate(f):
    """return a function that for any input x returns -f(x)"""
    return lambda *args, **kwargs: -f(*args, **kwargs)

def in_random_order(data):
    """generator that returns the elements of data in random order"""
    indexes = [i for i, _ in enumerate(data)]  # create a list of indexes
    random.shuffle(indexes)                    # shuffle them
    for i in indexes:                          # return the data in that order
        yield data[i]

def minimize_stochastic(target_fn, gradient_fn, x, y, theta_0, alpha_0=0.01):

    data = zip(x, y)
    theta = theta_0                             # initial guess
    alpha = alpha_0                             # initial step size
    min_theta, min_value = None, float("inf")   # the minimum so far
    iterations_with_no_improvement = 0

    # if we ever go 100 iterations with no improvement, stop
    while iterations_with_no_improvement < 100:
        value = sum( target_fn(x_i, y_i, theta) for x_i, y_i in data )

        if value < min_value:
            # if we've found a new minimum, remember it
            # and go back to the original step size
            min_theta, min_value = theta, value
            iterations_with_no_improvement = 0
            alpha = alpha_0
        else:
            # otherwise we're not improving, so try shrinking the step size
            iterations_with_no_improvement += 1
            alpha *= 0.9

        # and take a gradient step for each of the data points
        for x_i, y_i in in_random_order(data):
            gradient_i = gradient_fn(x_i, y_i, theta)
            theta = vector_subtract(theta, scalar_multiply(alpha, gradient_i))

    return min_theta


'''
We'll use data obtained from the National Agricultural Statistics Service API. First,
request an API key via https://quickstats.nass.usda.gov/api
API Documentation is located on the same page under "Usage"
Create an API request to return data for all TURKEYA desctibed as "TURKEYS,
YOUNG, SLAUGHTER, FI - SLAUGHTERED, MEASURED IN HEAD" in Virginia
for each month for each year available 1989 - 2018. Save this data in a format that you
can reuse.
Include the API command you used in your project report.
'''
def do_part_one():
    response = requests.get(GET_URL, params=GET_PARAMS)
    with open(DATA_FILE, "wb") as file:
        file.write(response.content)

'''(a) Create a line plot of the Value for each month of your data set from 1989-2002 and
2009-2018. Include the plot in your report. Note: There is a gap in your data between
2002 and 2009.
(b) Report any Structure you find, and any hypotheses you have about that structure.
(c) Report mean and median of the Value grouped by year
'''
def do_part_two(data_frame):
    data = data_frame[data_frame['year'] < 2003]
    data_2 = data_frame[data_frame['year'] > 2008]
    data = pd.concat([data, data_2])
    data['Value'] = pd.to_numeric(data['Value'])
    fig = data.plot(kind='line', x='reference_period_desc', y='Value').get_figure()
    fig.savefig('turkey_line_plot.pdf')
    print("Mean: " + str(data['Value'].mean()))
    print("Median: " + str(data['Value'].median()))

'''(a) For just the data from 2017, fit a linear regression to your data for the months January
- October
(b) Using your linear fit, predict the value of turkeys as described for November
(c) Compute the absolute error between your predicted value and the actual value of
turkeys slaughtered in Virginia in Nov 2017
(d) Compute the coefficient of determination, or R^2 value, to determine how well your
model fits your data.
(e) Plot a line plot of Values from 2017 along with the linear fit.
Report on (a)-(e).
'''
def do_part_three(data_frame):
    data = data_frame[data_frame['year'] == 2017]
    data = data[data_frame['begin_code'] <= 10]
    data['Value'] = pd.to_numeric(data['Value'])
    linear_regr = linear_model.LinearRegression()
    x = data['begin_code'].tolist()
    y = data['Value'].tolist()
    x = x[1:] # Removing the january values because the spike hurts the linear fit
    y = y[1:]
    print(x)
    print(y)
    alpha, beta = least_squares_fit(x, y)
    print("Alpha: " + str(alpha))
    print("Beta: " + str(beta))
    theta = [random.random(), random.random()]
    alpha, beta = minimize_stochastic(squared_error,
                                      squared_error_gradient,
                                      x,
                                      y,
                                      theta,
                                      0.0001)
    print("Optimized Alpha: " + str(alpha))
    print("Optimized Beta: " + str(beta))
    predited_Y = predict(alpha, beta, 11)
    print("November Turkey Prediction: " + str(predited_Y))
    print("R-squared: " + str(r_squared(alpha, beta, x, y)))
    plt.plot(x, y)
    linear_fit_x = []
    linear_fit_y = []
    for i in range(1, 11):
        linear_fit_x.append(i)
        linear_fit_y.append(alpha + beta * i)
    plt.plot(linear_fit_x, linear_fit_y)
    plt.show()





if __name__ == '__main__':
    if not os.path.isfile(DATA_FILE):
        do_part_one()
    data_frame = pd.read_csv(DATA_FILE, thousands=',')
    # do_part_two(data_frame)
    do_part_three(data_frame)
