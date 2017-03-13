#!/bin/bash

# latitude longitude of the seleted city
lat=48.85
lon=2.35
search_radius=0.27 # ~30km (1deg=111km)


# th file loc-gowalla_totalCheckins.txt contains the fields
# user_id date lat lon check_id
data_file=$1
awk '{if(sqrt((lat-$3)^2.0 + (lon-$4)^2.0)<=r) {print $0}}' \
    r=$search_radius lat=$lat lon=$lon $data_file 

