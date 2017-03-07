#!/usr/bin/env python

import json
import sys
from collections import OrderedDict
from copy import deepcopy
import string
import cPickle as pickle
import glob
import os.path
import pprint


import numpy as np
import pandas as pd


pp = pprint.PrettyPrinter(indent=4)

# types supported by google from https://developers.google.com/places/supported_types
TYPES_ = { 'accounting':0,
           'administrative_area_level_1':0,
           'administrative_area_level_2':0,
           'administrative_area_level_3':0,
           'administrative_area_level_4':0,
           'administrative_area_level_5':0,
           'airport':0,
           'amusement_park':0,
           'aquarium':0,
           'art_gallery':0,
           'atm':0,
           'bakery':0,
           'bank':0,
           'bar':0,
           'beauty_salon':0,
           'bicycle_store':0,
           'book_store':0,
           'bowling_alley':0,
           'bus_station':0,
           'cafe':0,
           'campground':0,
           'car_dealer':0,
           'car_rental':0,
           'car_repair':0,
           'car_wash':0,
           'casino':0,
           'cemetery':0,
           'church':0,
           'city_hall':0,
           'clothing_store':0,
           'colloquial_area':0,
           'convenience_store':0,
           'country':0,
           'courthouse':0,
           'dentist':0,
           'department_store':0,
           'doctor':0,
           'electrician':0,
           'electronics_store':0,
           'embassy':0,
           'establishment':0,
           'finance':0,
           'fire_station':0,
           'floor':0,
           'florist':0,
           'food':0,
           'funeral_home':0,
           'furniture_store':0,
           'gas_station':0,
           'general_contractor':0,
           'geocode':0,
           'grocery_or_supermarket':0,
           'gym':0,
           'hair_care':0,
           'hardware_store':0,
           'health':0,
           'hindu_temple':0,
           'home_goods_store':0,
           'hospital':0,
           'insurance_agency':0,
           'intersection':0,
           'jewelry_store':0,
           'laundry':0,
           'lawyer':0,
           'library':0,
           'light_rail_station':0,
           'liquor_store':0,
           'local_government_office':0,
           'locality':0,
           'locksmith':0,
           'lodging':0,
           'meal_delivery':0,
           'meal_takeaway':0,
           'mosque':0,
           'movie_rental':0,
           'movie_theater':0,
           'moving_company':0,
           'museum':0,
           'natural_feature':0,
           'neighborhood':0,
           'night_club':0,
           'painter':0,
           'park':0,
           'parking':0,
           'pet_store':0,
           'pharmacy':0,
           'physiotherapist':0,
           'place_of_worship':0,
           'plumber':0,
           'point_of_interest':0,
           'police':0,
           'political':0,
           'postal_code':0,
           'postal_code_prefix':0,
           'postal_code_suffix':0,
           'postal_town':0,
           'post_box':0,
           'post_office':0,
           'premise':0,
           'real_estate_agency':0,
           'restaurant':0,
           'roofing_contractor':0,
           'room':0,
           'route':0,
           'rv_park':0,
           'school':0,
           'shoe_store':0,
           'shopping_mall':0,
           'spa':0,
           'stadium':0,
           'storage':0,
           'store':0,
           'street_address':0,
           'street_number':0,
           'sublocality':0,
           'sublocality_level_1':0,
           'sublocality_level_2':0,
           'sublocality_level_3':0,
           'sublocality_level_4':0,
           'sublocality_level_5':0,
           'subpremise':0,
           'subway_station':0,
           'synagogue':0,
           'taxi_stand':0,
           'train_station':0,
           'transit_station':0,
           'travel_agency':0,
           'university':0,
           'veterinary_care':0,
           'zoo':0,
        
        }


# the following line is not needed on python >3.0 
TYPES_ = OrderedDict(sorted(TYPES_.items(), key=lambda t: t[0])) 

def read_jgoogle(json_file, verbose=False):
    ''' read_jgoogle reads a google jason site and returns its content as
    a dictionary that contains a coded   

    json_file : json query output from google
    verbose : if True it will print to the stdout 

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
    if not os.path.exists(json_file):
        raise IOError('json_file file doest exit')

    # decode json file
    with open(json_file) as jfile:
        try:
            all_data = json.load(jfile)
        except:
            print '...ERR... {}'.format(json_file)   
            sys.exit()

    all_decoded = list()
    data = all_data["results"]
    for d in data:
        decoded_data = dict()
        spot_signature = deepcopy(TYPES_)
        decoded_data['lat'] = d['geometry']['location']['lat']
        decoded_data['lon'] = d['geometry']['location']['lng'] 
        decoded_data['name'] = d['name']
        decoded_data['place_id'] = d['place_id'][:8]
        site_types = d['types']

        # coding the google types into a hash 
        try:
            # the place_id printed on the stdout will be cut then it won't be long lines
            # a place can have multiple types, for example in Eiffel Tower you can get
            # point of interest AND restaurant AND ....
            for type_ in site_types:
                spot_signature[type_] = 1
        except:
            error_ = u'ERROR in {} file'.format(json_file)
            print(error_.encode('utf-8') )
            raise NameError(error_)

       
        # signature of the place that will  be included in the personal trace 
        if verbose:
            t_ = u'{},'.format(decoded_data['lat'])
            t_+= u'{},'.format(decoded_data['lon']) 
            t_+= u'"{}",'.format(decoded_data['name']) 
            t_+= u'"{}",'.format(decoded_data['place_id']) 
            t_+= ''.join(['{:1d}'.format(s) for s in spot_signature.values()])
            print(t_.encode('utf-8'))

        # including the signature into the decoded data
        # decoded_data have lat, lon, name, place_id, and the spot_signature that is list
        decoded_data['spot_signature'] = spot_signature.values()
        all_decoded.append(decoded_data) 
        #pp.pprint(decoded_data)

    return all_decoded


def pickle_spot_signature(input_dir='data/sites/*.json', 
        spot_sgn_file='data/spot_sig.pkl'):
    ''' get all information from all json files in the directory dir_
    and save the data in a pickle
    '''
    spot_signatures = list()
    for json_file in glob.glob(input_dir):
        res = read_jgoogle(json_file, verbose=False)
        # avoid to include empty or repeted data
        if res and res not in spot_signatures: 
            spot_signatures+=read_jgoogle(json_file, verbose=False)
    
    with open(spot_sgn_file, 'wb') as pkl:
        pickle.dump(spot_signatures, pkl)


def unpickle_spot_signature(pickle_sig='data/spot_sig.pkl'):
    ''' unpickle the spot signature save by pickle_spot_signature
    '''
    if not os.path.exists(pickle_sig):
        raise IOError('file doest exit')
    
    with open(pickle_sig, 'rb') as pkl_file:
        spot_signatures = pickle.load(pkl_file)
    
    #pp.pprint(spot_signatures)
    return spot_signatures


class Sites(object):
    ''' stores site information from google sites
    '''

    def __init__(self, pkl_file):
        self.pkl_file = pkl_file
        if not os.path.exists(self.pkl_file):
            raise IOError('file doest exit')  

        #self.get_spot_signature(self, self.pkl_file) 

    def find_closer(self, lat, lon, n=5):
        '''given a latitude an longitude return the n closest values,
        for example the output Eiffel tower, the distnce is in degrees, 
        that it is equivalent to 111km by deg 

        >> print s.find_closer(48.8584, 2.2945, 1)
                    lat       lon              name  place_id  \
        8597  48.858369  2.294485  Eifl tower (Sun)  ChIJa9dx   
        
                                                 spot_signature      dist  
        8597  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ...  0.000035  
        
        '''
        
        self.data['dist'] = self.data.apply(lambda x: 
                np.sqrt((x['lat']-lat)**2.0 + (x['lon'] - lon)**2.0), 
                axis=1) 
        return self.data.sort(['dist'], ascending=[1]).head(n)

    def _to_pandas(self):
        '''convert spot_signature from dict to pandas dataframe'''
        self.data = pd.DataFrame.from_dict(self.spot_signatures)

    def get_spot_signature(self, pickle_sig):
        ''' get spot signature from pickle file set on the var pickle_sig'''
        if not os.path.exists(pickle_sig):
            raise IOError('file doest exit')
        
        with open(pickle_sig, 'rb') as pkl_file:
            self.spot_signatures = pickle.load(pkl_file)

        self._to_pandas()


if __name__ == '__main__':

    # test for Eiffel Tower 
    pkl_file = 'data/spot_sig.pkl'
    s = Sites(pkl_file)
    s.get_spot_signature(pkl_file)
    print s.find_closer(48.8584, 2.2945, 1)
     

