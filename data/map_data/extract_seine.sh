#!/bin/bash

geojson=paris_france_osm_line.geojson

if [ ! -f $geojson ]; then 
    echo "file $geojson not found ";
    echo "get it from https://mapzen.com/data/metro-extracts/metro/paris_france/"
    echo "file paris_france.osm2pgsql-geojson.zip"
    exit 0;
fi


if ! file $geojson
    echo "file not "
    exit 0
fi


# for each line in the file geojon extract lat lon in a differente file

# how many vectors?
n_vectors=$(grep 'La Seine' paris_france_osm_line.geojson | wc -l)

for line in $(seq 1 $n_vectors); do
    n_=$(printf "%02d" $line)
    grep 'La Seine' $geojson | sed "${line}q;d" | tr '[' '\n' | awk 'NR > 2 {print}' | \
        awk '{print $2, $1}' | tr ', ' ' ,' > seine${n_}.xy
done


