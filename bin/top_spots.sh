#!/bin/bash

paris_data='data/loc-gowalla_totalCheckins_Paris.txt'
n_top_spots=10


# generate data/top_places.txt ... for a table in analysis

cat $paris_data | awk '{print $5}' | sort | uniq -c | \
    sort -k1,1nr | head -n $n_top_spots | awk '{print $2, $1}' > data/top_spots.lst

while read spot_id n_check; do
    pos=$(awk '{if($5==spot_id){print $3,$4}}' spot_id=$spot_id $paris_data | sort | uniq)
    echo "$spot_id $n_check $pos" 
done < data/top_spots.lst > data/top_spot_lat_lon.lst

while read spot n_check lat lon ; do
    echo "---------"
    echo " $spot $n_check " 
    awk 'BEGIN{FS=","}{d = sqrt(($1-lat)^2.0 + ($2-lon)^2.0);
         print d","n_check","s","$1","$2","$3}' \
       n_check=$n_check s=$spot lat=$lat lon=$lon data/google_sites.csv | sort -k1,1nr | head -n  10 | \
       awk -F, '{printf("%.d %s\n", $1*111.0*1000, $6)}'
done < data/top_spot_lat_lon.lst
