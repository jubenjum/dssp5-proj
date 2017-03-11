#!/usr/bin/env python

import glob

import numpy as np
import matplotlib.pyplot as plt

lat_paris = 48.8566
lon_paris = 2.3522


fig = plt.figure()
#ax = fig.add_subplot(1,1,1)
ax = fig.add_subplot(1,1,1, adjustable='box', 
        aspect=1/np.cos(lat_paris*np.pi/180.0))

for file_ in glob.glob('a*.xy'):
    xy = np.genfromtxt(file_, delimiter=',')
    ax.plot(xy[:,1], xy[:,0], '-k')

# get and plot the Seine
for file_ in glob.glob('seine*.xy'):
    xy = np.genfromtxt(file_, delimiter=',')
    plt.plot(xy[:,1], xy[:,0], color="#6495ED")

# Plot a point for example Eiffel Tower
ax.plot(2.2945, 48.8584, '*r', markersize=20) # see documentation for more markers

# set  other parameters and show the figure
#plt.axis('equal')

ax.set_xlim([2.25, 2.425])
ax.set_ylim([48.8,48.92])


#ax.title('Paris', fontsize=20)
plt.show()


