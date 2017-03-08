#!/bin/bash

# 10m ~ 1e-4 deg <- precision
###awk '{printf("%07.4f_%07.4f_100\n", $3, $4)}' \
###    data/loc-gowalla_totalCheckins_Paris.txt | sort -u > list_coords
###
###for l in $(cat list_coords); do
###    lat=$(echo $l | cut -d'_' -f1)
###    lon=$(echo $l | cut -d'_' -f2)
###    dist=$(echo $l | cut -d'_' -f3)
###    name=$(echo "LAT"$lat"_LON"$lon"_DIST"$dist'.json')
###    echo $name
###    ./bin/get_near.py $lat $lon $dist > data/sites/$name
###    sleep $(( ( RANDOM % 5 )  + 1 ))
###done

#
# if got out of the google query days limit (2500)
for f in $(grep OVER_QUERY_LIMIT -l data/sites/*); do
    lat=$(echo $f | cut -c15-21)
    lon=$(echo $f | cut -c27-32)
    dist=$(echo $f | cut -c38-39)
    echo $f
    ./bin/get_near.py $lat $lon $dist > $f 
    sleep $(( ( RANDOM % 2 )  + 1 ))
done



