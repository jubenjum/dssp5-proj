#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' make a map 
'''

import pandas as pd
import argparse
import matplotlib
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('input_file', metavar='INPUT_FILE', nargs=1, help='...')
args = parser.parse_args()

file_ = args.input_file[0]
data = pd.read_table(file_, sep='\s+|\t+|\s+\t+|\t+\s+|\xc2\xa0',
        engine='python', header=None, names=['user_id', 'date', 'lat', 'lon', 'check_id']) 

data.plot.scatter(x='lon', y='lat', s=2)
plt.axis('equal')
plt.show()

