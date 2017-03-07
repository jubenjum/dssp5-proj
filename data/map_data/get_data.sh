#!/bin/bash

# arrondissement shapes from http://wiki.openstreetmap.org/wiki/Paris
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=20727 > a01.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9542  > a02.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=20742 > a03.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9597  > a04.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=20873 > a05.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9527  > a06.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9521  > a07.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=20872 > a08.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9537  > a09.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9528  > a10.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9533  > a11.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9525  > a12.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9530  > a13.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9522  > a14.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9520  > a15.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9517  > a16.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9519  > a17.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9531  > a18.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9552  > a19.gpx
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=9529  > a20.gpx

# la seine - https://wiki.openstreetmap.org/wiki/WikiProject_France/Cours_d'eau
curl http://ra.osmsurround.org/exportRelation/gpx?relationId=962076 > seine.gpx

