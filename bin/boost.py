#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
import numpy as np
import datetime as dt
#from pytz import UTC, timezone
#from tzwhere import tzwhere # pip install tzwhere

from sklearn.metrics import mean_squared_error
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn import svm


# functions to read command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('input_file', metavar='INPUT_FILE', nargs=1, help='...')
args = parser.parse_args()
file_ = args.input_file[0]

#### from utc to local time with dayligth saving 
##tzwhere = tzwhere.tzwhere()
##def to_localtime(lat, lon, date):
##    '''compute the local time from latitude longitude and time
##    with dayligth (from: https://goo.gl/CIhQzj)'''
##    date_utc = date.tz_localize(UTC) 
##    timezone_str = tzwhere.tzNameAt(lat, lon)
##    timezone_ = timezone(timezone_str)
##    # return to convert it to an ISO string of local time 
##    return date_utc.astimezone(timezone_).isoformat() 

# getting the file into a pandas datframe
# the conversion from string to date in the dataframe
# is taken from goo.gl/ewyYdV
headers = ['user_id', 'date', 'lat', 'lon', 'spot_id']
dtypes = {'user_id': 'int', 'date': 'str', 'lat': 'float', 
          'lon': 'float', 'spot_id': 'int' }
parse_dates = ['date']
data = pd.read_table(file_, sep='\s+', header=None, dtype=dtypes, 
        parse_dates=parse_dates, names=headers) 

### transforming by rows from date to local time
### using https://goo.gl/7exmUO
##data['localtime'] = data.apply(lambda row: to_localtime(row['lat'], row['lon'], row['date']), axis=1)
##

#### adding columns to the dataframe with the day of week and hour
###data['weekday'] = pd.to_datetime(data['localtime']).dt.dayofweek # Monday=0, Sunday=6
###data['hour'] = pd.to_datetime(data['localtime']).dt.hour

X = np.array(data.spot_id).reshape(-1, 1)
y = np.array(data.user_id)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
        test_size=0.33)


est = GradientBoostingRegressor(n_estimators=10000, learning_rate=0.01,
        max_depth=10000, random_state=0, loss='huber', verbose=5).fit(X_train, y_train)
print mean_squared_error(y_test, est.predict(X_test))    


