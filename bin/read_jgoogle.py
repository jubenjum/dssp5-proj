#!/usr/bin/env python

import json
import argparse
import sys
from collections import OrderedDict
from copy import deepcopy


# types supported by google
types_ = { 'accounting':0,
           'administrative_area_level_1counting':0,
           'administrative_area_level_2counting':0,
           'administrative_area_level_3counting':0,
           'administrative_area_level_4counting':0,
           'administrative_area_level_5counting':0,
           'airportcounting':0,
           'amusement_parkcounting':0,
           'aquariumcounting':0,
           'art_gallerycounting':0,
           'atmcounting':0,
           'bakerycounting':0,
           'bankcounting':0,
           'barcounting':0,
           'beauty_saloncounting':0,
           'bicycle_storecounting':0,
           'book_storecounting':0,
           'bowling_alleycounting':0,
           'bus_stationcounting':0,
           'cafecounting':0,
           'campgroundcounting':0,
           'car_dealercounting':0,
           'car_rentalcounting':0,
           'car_repaircounting':0,
           'car_washcounting':0,
           'casinocounting':0,
           'cemeterycounting':0,
           'churchcounting':0,
           'city_hallcounting':0,
           'clothing_storecounting':0,
           'colloquial_areacounting':0,
           'convenience_storecounting':0,
           'countrycounting':0,
           'courthousecounting':0,
           'dentistcounting':0,
           'department_storecounting':0,
           'doctorcounting':0,
           'electriciancounting':0,
           'electronics_storecounting':0,
           'embassycounting':0,
           'establishmentcounting':0,
           'financecounting':0,
           'fire_stationcounting':0,
           'floorcounting':0,
           'floristcounting':0,
           'foodcounting':0,
           'funeral_homecounting':0,
           'furniture_storecounting':0,
           'gas_stationcounting':0,
           'general_contractorcounting':0,
           'geocodecounting':0,
           'grocery_or_supermarketcounting':0,
           'gymcounting':0,
           'hair_carecounting':0,
           'hardware_storecounting':0,
           'healthcounting':0,
           'hindu_templecounting':0,
           'home_goods_storecounting':0,
           'hospitalcounting':0,
           'insurance_agencycounting':0,
           'intersectioncounting':0,
           'jewelry_storecounting':0,
           'laundrycounting':0,
           'lawyercounting':0,
           'librarycounting':0,
           'light_rail_station':0,
           'liquor_storecounting':0,
           'local_government_officecounting':0,
           'localitycounting':0,
           'locksmithcounting':0,
           'lodgingcounting':0,
           'meal_deliverycounting':0,
           'meal_takeawaycounting':0,
           'mosquecounting':0,
           'movie_rentalcounting':0,
           'movie_theatercounting':0,
           'moving_companycounting':0,
           'museumcounting':0,
           'natural_featurecounting':0,
           'neighborhoodcounting':0,
           'night_clubcounting':0,
           'paintercounting':0,
           'parkcounting':0,
           'parkingcounting':0,
           'pet_storecounting':0,
           'pharmacycounting':0,
           'physiotherapistcounting':0,
           'place_of_worshipcounting':0,
           'plumbercounting':0,
           'point_of_interestcounting':0,
           'policecounting':0,
           'politicalcounting':0,
           'postal_codecounting':0,
           'postal_code_prefixcounting':0,
           'postal_code_suffixcounting':0,
           'postal_towncounting':0,
           'post_boxcounting':0,
           'post_officecounting':0,
           'premisecounting':0,
           'real_estate_agencycounting':0,
           'restaurantcounting':0,
           'roofing_contractorcounting':0,
           'roomcounting':0,
           'routecounting':0,
           'rv_parkcounting':0,
           'schoolcounting':0,
           'shoe_storecounting':0,
           'shopping_mallcounting':0,
           'spacounting':0,
           'stadiumcounting':0,
           'storagecounting':0,
           'storecounting':0,
           'street_addresscounting':0,
           'street_numbercounting':0,
           'sublocalitycounting':0,
           'sublocality_level_1counting':0,
           'sublocality_level_2counting':0,
           'sublocality_level_3counting':0,
           'sublocality_level_4counting':0,
           'sublocality_level_5counting':0,
           'subpremisecounting':0,
           'subway_stationcounting':0,
           'synagoguecounting':0,
           'taxi_standcounting':0,
           'train_stationcounting':0,
           'transit_stationcounting':0,
           'travel_agencycounting':0,
           'universitycounting':0,
           'veterinary_carecounting':0,
           'zoocounting':0,
        
        }

types_ = OrderedDict(sorted(types_.items(), key=lambda t: t[0])) 


def read_jgoogle(json_file):
    ''' read_jgoogle reads a google jason site and returns its content as
    a dictionary that contains a coded   

    the json files have the folloging structure:

        results->
        geometry/location/lat,lon                        <-- usefull
        geometry/viewpoint/Northeast,southwest/lat,lon
        icon
        id                                               <-- usefull     
        name                                             <-- usefull
        photos/heigth,html_attributions,photo_reference,width
        place_id                                         <-- ?
        reference
        scope
        types                                            <-- usefull
        vicinity                                         <-- usefull

        the fist level on the json has the label html_attributions and it 
        is empty for the queries I have done

    '''

    # decode json file
    with open(json_file) as jfile:
        try:
            all_data = json.load(jfile)
        except:
            print '...ERR... {}'.format(json_file)   
            sys.exit()


    data = all_data["results"]
    for d in data:
        copy_type_ = deepcopy(types_)
        lat = d['geometry']['location']['lat']
        lon = d['geometry']['location']['lng'] 
        name = d['name']
        place_id = d['place_id']
        types = d['types']
        
        # coding the google types into a hash 
        try:
            for t in types:
                print(u'{},{},"{}","{}","{}"'.format(lat, lon, name, place_id[:10], t))
        except:
            print(u'{}'.format(json_file))
            copy_type_[t] = 1
            print t
        hash_type = ''.join(['{:1d}'.format(s) for s in copy_type_.values()])
        print('{},{},"{}","{}",{}'.format(lat, lon, name, place_id[:10], hash_type))
    
def main(json_file):
    read_jgoogle(json_file)



if __name__ == '__main__':
    import argparse

    # functions to read command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('json_file', metavar='JSON_FILE', nargs=0, 
            help='read google json from places')
    args = parser.parse_args()
    json_file = args.json_file[0]
    main(json_file)
