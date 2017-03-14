#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' make a map 
'''

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('ggplot')


### script to plot the figures of number of datapoints by venieu
### I used google_sites_types.csv

# functions to read command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('input_file', metavar='INPUT_FILE', nargs=1, help='...')
args = parser.parse_args()
file_ = args.input_file[0]

# getting the file into a pandas datframe
# the conversion from string to date in the dataframe
# is taken from goo.gl/ewyYdV

headers = ['lat', 'lon', 'name', 'google_hash', 'type']
dtypes = {'lat': 'float', 'lon': 'float', 'name': 'str', 'google_hash':'str', 'type':'str'}
data = pd.read_table(file_, sep=',', header=None, dtype=dtypes, names=headers) 

# plot by day
f1 = plt.figure(1)
count_bytype = np.array(data.groupby('type').size()) 
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

