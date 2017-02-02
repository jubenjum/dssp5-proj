#!/usr/bin/env python

#awk '{print 1000*111*sqrt(($3-$6)^2+($4-$7)^2)}' gowalla-noisy > n1
#awk '{print 1000*111*sqrt(($3-$8)^2+($4-$9)^2)}' gowalla-noisy > n2
#awk '{print 1000*111*sqrt(($3-$10)^2+($4-$11)^2)}' gowalla-noisy > n3

import argparse
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('input_file', metavar='INPUT_FILE', nargs=1, help='...')
args = parser.parse_args()
file_ = args.input_file[0]

#headers=['dist']
#data = pd.read_table(file_, header=None, names=headers)
#d = np.array(data.dist)
#print data.describe(percentiles=[.01,.1, .2, .3, .4, .5, .6, .7, .8, .9, .99])

## Create non-uniform bins.  Unit in seconds.
#bins = np.logspace(0, np.log(d.max()), 100)
## Get histogram of random data
#y, x = np.histogram(d, bins=bins, normed=True)
## Correct bin placement
#x = x[1:]
#plt.scatter(x,y)
#plt.show()

headers = ['user_id', 'date', 'lat', 'lon', 'spot_id', 
        'latR1','lonR1', 'latR2','lonR2', 'latR3','lonR3']
dtypes = {'user_id': 'int', 'date': 'str', 'lat': 'float', 
          'lon': 'float', 'spot_id': 'int',
          'latR1': 'float','lonR1': 'float',
          'latR2': 'float', 'lonR2': 'float',
          'latR3' : 'float', 'lonR3' : 'float' }
parse_dates = ['date']
data = pd.read_table(file_, sep=r'\t+',
        engine='python', header=None, 
        parse_dates=parse_dates, names=headers)
lat = np.array(data.lat, dtype=np.float64)
lon = np.array(data.lon, dtype=np.float64)
latR1 = np.array(data.latR1, dtype=np.float64)
lonR1 = np.array(data.lonR1, dtype=np.float64)
distR1 = 111.0*1000.0*np.sqrt((lat-latR1)**2.0 + (lon-lonR1)**2.0)
for d in distR1:
    print '{}'.format(d)

