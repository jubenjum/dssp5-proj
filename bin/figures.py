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

# functions to read command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('input_file', metavar='INPUT_FILE', nargs=1, help='...')
args = parser.parse_args()
file_ = args.input_file[0]

## from utc to local time with dayligth saving 
tzwhere = tzwhere.tzwhere()
def to_localtime(lat, lon, date):
    '''compute the local time from latitude longitude and time
    with dayligth (from: https://goo.gl/CIhQzj)'''
    date_utc = date.tz_localize(UTC) 
    timezone_str = tzwhere.tzNameAt(lat, lon)
    timezone_ = timezone(timezone_str)
    # return to convert it to an ISO string of local time 
    return date_utc.astimezone(timezone_).isoformat() 

# getting the file into a pandas datframe
# the conversion from string to date in the dataframe
# is taken from goo.gl/ewyYdV

headers = ['user_id', 'date', 'lat', 'lon', 'spot_id']
dtypes = {'user_id': 'int', 'date': 'str', 'lat': 'float', 
          'lon': 'float', 'spot_id': 'int' }
parse_dates = ['date']
data = pd.read_table(file_, sep='\s+', header=None, dtype=dtypes, 
        parse_dates=parse_dates, names=headers) 

# transforming by rows from date to local time
# using https://goo.gl/7exmUO
data['localtime'] = data.apply(lambda row: to_localtime(row['lat'], row['lon'], row['date']), axis=1)


# adding columns to the dataframe with the day of week and hour
data['weekday'] = pd.to_datetime(data['localtime']).dt.dayofweek # Monday=0, Sunday=6
data['hour'] = pd.to_datetime(data['localtime']).dt.hour

# plot by day
f1 = plt.figure(1)
count_byday = np.array(data.groupby('weekday').size()) 
fig, ax = plt.subplots()
day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
ax.bar(np.arange(len(day)), count_byday, align='center', color='green', ecolor='black')
ax.set_xticks(range(len(day)))
ax.set_xticklabels(day)
ax.set_xlabel('Day of week')
ax.set_ylabel('#Check-ins')
ax.set_title('Check-in by day of week')

# plot by day/hour
f2 = plt.figure(2)
fig, axarr = plt.subplots(7, 1, sharex='row', sharey='col')
for day_num in range(len(day)):
    data_ = data.loc[data['weekday'] == day_num]
    r = data_['hour'].value_counts()
    hour, n_checkins = r.index, r.values
    axarr[day_num].text(0.8, 0.8, '{}'.format(day[day_num]), 
            horizontalalignment='center', 
            transform=axarr[day_num].transAxes)
    axarr[day_num].stem(hour, n_checkins, markerfmt='bo')  
    #axarr[day_num].set_xticks(range(24))
    #axarr[day_num].set_xticklabels()

plt.show()

#plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
#plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)
raw_input()

