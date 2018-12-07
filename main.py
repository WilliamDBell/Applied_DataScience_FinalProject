import requests
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
    x = [data['begin_code']]
    y = [data['Value']]
    model = linear_regr.fit(x, y)




if __name__ == '__main__':
    if not os.path.isfile(DATA_FILE):
        do_part_one()
    data_frame = pd.read_csv(DATA_FILE, thousands=',')
    do_part_two(data_frame)
    do_part_three(data_frame)
