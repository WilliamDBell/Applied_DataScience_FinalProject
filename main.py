import requests

api_key = '2520FD98-BA2D-356A-8A02-9FE608339890' # key

get_url = 'http://quickstats.nass.usda.gov/api/api_GET' # url to request data

get_params = {
    'key' : api_key,
    'commodity_desc' : 'TURKEYS',
    'year__GE' : '1989',
    'year__LE' : '2018',
    'state_alpha' : 'VA',
    'short_desc' : 'TURKEYS, YOUNG, SLAUGHTER, FI - SLAUGHTERED, MEASURED IN HEAD'
    }

data = requests.get(get_url, params=get_params).json()
