import requests
import csv
import json
import os.path

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


def get_turkey_data(url, params, file_path):
    response = requests.get(url, params=params)
    with open(DATA_FILE, "wb") as file:
        file.write(response.content)

if __name__ == '__main__':
    if not os.path.isfile(DATA_FILE):
        get_turkey_data(GET_URL, GET_PARAMS, DATA_FILE)