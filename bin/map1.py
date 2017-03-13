#!/usr/bin/env python

import glob

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

lat_paris = 48.8566
lon_paris = 2.3522
lat_correction=1/np.cos(lat_paris*np.pi/180.0)

fig = plt.figure(figsize=(17/2.54,11/2.54))
ax1 = fig.add_subplot(121, adjustable='box', 
        aspect=lat_correction)
ax2 = fig.add_subplot(122, adjustable='box', 
        aspect=lat_correction)

for file_ in glob.glob('data/map_data/*.xy'):
    xy = np.genfromtxt(file_, delimiter=',')
    ax1.plot(xy[:,1], xy[:,0], color="#777777", linewidth=2)
    ax2.plot(xy[:,1], xy[:,0], color="#777777", linewidth=2)
 

# get and plot the Seine
for file_ in glob.glob('data/map_data/seine*.xy'):
    xy = np.genfromtxt(file_, delimiter=',')
    ax1.plot(xy[:,1], xy[:,0], color="#6495ED", linewidth=3)
    ax2.plot(xy[:,1], xy[:,0], color="#6495ED", linewidth=3)

# load google sites columns 1,2
xy_goog = np.genfromtxt('data/google_sites.csv', delimiter=',', usecols=(0, 1))
ax1.plot(xy_goog[:,1], xy_goog[:,0], ".k", markersize=1)

xy_gowa = np.genfromtxt('data/loc-gowalla_totalCheckins_Paris.txt', usecols=(2, 3))
ax2.plot(xy_gowa[:,1], xy_gowa[:,0], ".k", markersize=1)


# Plot a point for example Eiffel Tower
ax1.plot(2.2945, 48.8584, '*r', markersize=10) # see documentation for more markers
ax2.plot(2.2945, 48.8584, '*r', markersize=10) # see documentation for more markers

ax1.set_xlim([2.22, 2.45])
ax1.set_ylim([48.80,48.92])
ax1.tick_params(labelbottom='off')  
ax1.tick_params(labelleft='off')  
ax1.set_title('Google Places')

ax2.set_xlim([2.22, 2.45])
ax2.set_ylim([48.80,48.92])
ax2.tick_params(labelbottom='off')  
ax2.tick_params(labelleft='off') 
ax2.set_title('Gowalla check-in')

plt.show()
#plt.savefig('docs/figures/map1.png')




