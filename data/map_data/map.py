#!/usr/bin/env python

import glob

import numpy as np
import matplotlib.pyplot as plt


axes = plt.gca()

# read and plot all arrondisements
for file_ in glob.glob('a*.xy'):
    lats = list(); lons = list()
    with open(file_) as f:
        for lines in f.readlines():
            lat, lon = lines.strip().split(",")
            lats.append(float(lat))
            lons.append(float(lon))
        plt.plot(lons, lats, '-k')

# get and plot the Seine
for file_ in glob.glob('seine*.xy'):
    lats = list(); lons = list()
    with open(file_) as f:
        for lines in f.readlines():
            lat, lon = lines.strip().split(",")
            lats.append(float(lat))
            lons.append(float(lon))
        plt.plot(lons, lats, '-b')

# Plot a point for example Eiffel Tower
plt.plot(2.2945, 48.8584, '*r', markersize=20) # see documentation for more markers


# set  other parameters and show the figure
axes.set_xlim([2.234, 2.454])
axes.set_ylim([48.801,48.917])
plt.title('Paris')
plt.show()


