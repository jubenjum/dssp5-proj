#!/bin/bash

# wget -O paris.osm "http://api.openstreetmap.org/api/0.6/map?bbox=2.2222,48.8129,2.4517,48.9116"

# arrondissement shapes from http://wiki.openstreetmap.org/wiki/Paris
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=20727 | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a01.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9542  | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a02.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=20742 | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a03.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9597  | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a04.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=20873 | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a05.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9527  | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a06.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9521  | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a07.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=20872 | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a08.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9537  | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a09.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9528  | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a10.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9533  | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a11.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9525  | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a12.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9530  | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a13.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9522  | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a14.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9520  | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a15.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9517  | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a16.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9519  | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a17.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9531  | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a18.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9552  | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a19.xy
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9529  | grep 'trkpt' | cut -d'"' -f2,4 --output-delimiter=',' > a20.xy

## la seine - https://wiki.openstreetmap.org/wiki/WikiProject_France/Cours_d'eau
#curl http://ra.osmsurround.org/exportRelation/gpx?relationId=962076 > seine.gpx

