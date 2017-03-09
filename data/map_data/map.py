#!/usr/bin/env python

import glob

import numpy as np
import matplotlib.pyplot as plt


for file_ in glob.glob('a*.xy'):
    xy = np.genfromtxt(file_, delimiter=',')
    plt.plot(xy[:,0], xy[:,1], '-k')

# get and plot the Seine
for file_ in glob.glob('seine*.xy'):
    xy = np.genfromtxt(file_, delimiter=',')
    plt.plot(xy[:,0], xy[:,1], color="#6495ED")

# Plot a point for example Eiffel Tower
plt.plot(2.2945, 48.8584, '*r', markersize=20) # see documentation for more markers

# set  other parameters and show the figure
#plt.axis('equal')
plt.axes().set_xlim([2.25, 2.45])
plt.axes().set_ylim([48.8,48.9])

plt.title('Paris', fontsize=20)
plt.show()


