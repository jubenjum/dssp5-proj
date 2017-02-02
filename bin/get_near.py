#!/usr/bin/env python


import argparse
import json
import urllib2
import os
import sys

def no_key():
    print('set the GOOGLE_DEV_KEY environmental variable with your ',
          'personal key')
    sys.exit(1)


try:
    env_google_key = os.environ['GOOGLE_DEV_KEY']
except:
    no_key()


def get_near(lat,lon, dist):
    '''get nearest venues from from coordinates 
    (lat,lon) and a distance (m), return json
    string.
    
    for example for Tour Eiffel:
    
    >> get_near(48.8584, 2.2945, 50) 
    { result ... }

    '''
    global env_google_key

    loc='{},{}'.format(lat, lon)
    rad=str(dist) # in m
    
    # type_='restaurant' # https://goo.gl/w52AAE if not set will get all
    try:
        key=env_google_key
    except:
        no_key() 
    
    # building the address
    url = 'https://maps.googleapis.com/'
    url+= 'maps/api/place/nearbysearch/json?location={}'.format(loc)
    url+= '&radius={rad}&key={key}'.format(rad=rad, key=key)

    # getting information from google webpage
    req = urllib2.Request(url=url)
    f = urllib2.urlopen(req)
    return f.read()

# functions to read command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('lat', metavar='LATITUDE', nargs=1, help='latitude')
parser.add_argument('lon', metavar='LONGITUDE', nargs=1, help='logitude')
parser.add_argument('dist', metavar='distance', nargs=1, help='dist(m)')
args = parser.parse_args()

# 10m ~ 0.0001 deg


lat=float(args.lat[0])
lon=float(args.lon[0])
dist=int(float(args.dist[0]))

print get_near(lat,lon,dist)



