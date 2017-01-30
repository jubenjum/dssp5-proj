#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' make a map 
'''

import argparse
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from pytz import UTC, timezone
from tzwhere import tzwhere # pip install tzwhere

tzwhere = tzwhere.tzwhere()

def to_localtime(lat, lon, date):
    '''compute the local time from latitude longitude and time
    with dayligth (from: https://goo.gl/CIhQzj)'''
    date_utc = date.tz_localize(UTC) 
    timezone_str = tzwhere.tzNameAt(lat, lon)
    timezone_ = timezone(timezone_str)
    # return to convert it to an ISO string of local time 
    return date_utc.astimezone(timezone_).isoformat() 

# functions to read command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('input_file', metavar='INPUT_FILE', nargs=1, help='...')
args = parser.parse_args()
file_ = args.input_file[0]

# getting the file into a pandas datframe
# the conversion from string to date in the dataframe
# is taken from goo.gl/ewyYdV
headers = ['user_id', 'date', 'lat', 'lon', 'spot_id']
dtypes = {'user_id': 'int', 'date': 'str', 'lat': 'float', 
          'lon': 'float', 'spot_id': 'int' }
parse_dates = ['date']
data = pd.read_table(file_, sep='\s+', header=None, dtype=dtypes, 
        parse_dates=parse_dates, names=headers) 

data.plot.scatter(x='lon', y='lat', s=2)
plt.axis('equal')
plt.show()

