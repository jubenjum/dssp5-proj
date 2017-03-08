#!/usr/bin/env python

'''
Classes and functions to read data from gowalla 

'''

import os
import sys
import itertools

import string
import cPickle as pickle
import glob
import os.path
import pprint

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from dspr.sites import Sites 


# initilize environmental variables
try:
    NUM_JOBS = os.environ['NUM_JOBS']
except:
    NUM_JOBS = 1


def read_gowalla(file_name):
    ''' read the gowalla file and return
    a pandas frame 
    '''
    
    # gowalla file doesn't have a header but the
    # columns are contains the following fields ...
    headers = ['user_id', 'date', 'lat', 'lon', 'spot_id']
    
    # the data types for each column are
    dtypes = {'user_id': 'int', 'date': 'str', 'lat': 'float', 
          'lon': 'float', 'spot_id': 'int'}
    
    # date and time is in UTC 
    parse_dates = ['date']

    return pd.read_table(file_name, sep='\s+', header=None, dtype=dtypes, 
        parse_dates=parse_dates, names=headers) 


class People(Sites):
    ''' People class stores Gowalla data and methods to access '''

    # d is the dimensions of the features 130 for google site data
    people_param = {'data_file' : '', 'pandas_data' : '', 
                    'd' : 130, 'people_signatures' : ''}

    def __init__(self, parent=None, **kwargs):
        '''      '''
        super(Sites, self).__init__()
        global NUM_JOBS # umm not the best but  
        self.NUM_JOBS = NUM_JOBS

        if kwargs:
            self.people_param.update(kwargs)

        self.initialize_args(kwargs)

    def initialize_args(self, kwargs):
        ''' '''
        if self.people_param['data_file']:
            people_param['pandas_data'] = read_gowalla(self.people_param['data_file'])
    
    def people_to_pickle(self, pandas_pickle):
        ''' to pickle '''
        self.people_param['pkl_pandas'] = pandas_pickle
        self.people_param['pandas_data'].to_pickle(pandas_pickle) # pandas to_pickle

    def people_from_pickle(self, pandas_pickle):
        '''read the Gowalla pandas pickle'''
        if not os.path.exists(pandas_pickle):
            raise OSError("file pandas_pickle doesnt not set")
        self.sites_param['pandas_data'] =  pd.read_pickle(pandas_pickle)

    def get_people_data(self, data_file):
        ''' get peoples data from txt file using read_gowalla '''
        self.people_param['data_file'] = data_file
        self.people_param['pandas_data'] = read_gowalla(self.people_param['data_file'])


    def save_people_signatures(self, people_signatures_file):
        ''' save peoples signature in a pickle '''
        self.people_param['people_signatures'].to_pickle(people_signatures_file)


    def compute_path_signature(self):
        '''for each user compute the path signature that is the sum of spot signatures 
        where the pearson has been'''
	self.people_param['people_signatures'] = _compute_path_signature(self.people_param['pandas_data'], \
	         self.people_param['d'], self.sites_param['pandas_data'])


def _compute_path_signature(people_data, d, spot_data):
    ''' single thread computation of path signature (used insde People class) '''
    df = pd.DataFrame(columns=('user_id','user_signature'))
    for user in people_data['user_id'].unique():
       _r = h_func_signature(user, people_data, d, spot_data)
       df = df.append(_r, ignore_index=True) 

    return df 

def h_func_signature(user, pandas_data, d, spot_data):
    ''' parallel version of the  '''
    n = 5
    user_signatures = np.zeros((1, d), dtype=int)
    for lat_, lon_ in pandas_data[pandas_data['user_id'] == user][['lat','lon']].as_matrix():
        idx_ =  spot_data.apply(lambda x: np.sqrt((x['lat']-lat_)**2.0 \
                + (x['lon'] - lon_)**2.0), axis=1).sort_values(ascending=[1]).head(n).index.tolist()
        _sig = np.array([x for x in spot_data.spot_signature.iloc[idx_]], dtype=int)
        user_signatures = np.append(user_signatures, _sig, axis=0)
    user_signature = np.sum(user_signatures, axis=0)
    df_user = pd.DataFrame([[user, user_signature]], columns=('user_id','user_signature'))
    print '{} = {}'.format(user, user_signature)
    return df_user


def parallel_comp_path_signature(pandas_data, pandas_pickle, d, n_jobs=1):
    ''' the same that _compute_path_signature but multithread '''
    global NUM_JOBS
    pandas_data = read_gowalla(pandas_data)
    with open(pandas_pickle, 'rb') as pkl_file_:
        spot_signatures = pickle.load(pkl_file_)
        spot_data = pd.DataFrame.from_dict(spot_signatures)

    df = pd.DataFrame(columns=('user_id','user_signature'))
    users_ = [ int(x) for x in pandas_data['user_id'].unique()]
    with Parallel(n_jobs=n_jobs) as parallel: 
        _r = parallel(delayed( h_func_signature)(u, pandas_data, d, spot_data) for u in users_)
        df = df.append(_r, ignore_index=True)

    return df 


if __name__ == '__main__':
    
    # test for Eiffel Tower 
    pkl_file = 'data/spot_sig.pkl'
    pandas_pickle = 'data/sites_pandas.pkl'
    spot_signatures = 'data/spot_signatures.npz' # contain only the an numpy array with signatures
    data_gowalla_paris = 'data/loc-gowalla_totalCheckins_Paris.txt'
    people_signatures_file = 'data/people_signature.pkl'
    
    d = 130
    df = parallel_comp_path_signature(data_gowalla_paris, pandas_pickle, d, n_jobs=3)
    df.to_pickle(people_signatures_file) # contains user and user_signature


    #p = People(pandas_pickle)
    #if os.path.exists(pandas_pickle):
    #    print "Read pandas pickle ..."
    #    p.sites_from_pickle(pandas_pickle)
    #else :
    #    p.get_spot_signature(pkl_file)
    #
    #p.get_people_data(data_gowalla_paris)
    #p.compute_path_signature()
    #p.save_people_signatures(people_signatures_file)

