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
from multiprocessing import Process, Value, Lock

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



class Counter(object):
    ''' shared counter from goo.gl/Z3HJTj '''
    def __init__(self, initval=0):
        self.val = Value('i', initval)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    def value(self):
        with self.lock:
            return self.val.value


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
        ''' '''
        self.people_param['pkl_pandas'] = pandas_pickle
        self.people_param['pandas_data'].to_pickle(pandas_pickle) # pandas to_pickle

    def people_from_pickle(self, pandas_pickle):
        '''read the Gowalla pandas pickle'''
        self.sites_param['pandas_data'] =  pd.read_pickle(pandas_pickle)

    def get_people_data(self, data_file):
        ''' get peoples data from txt file using read_gowalla '''
        self.people_param['data_file'] = data_file
        self.people_param['pandas_data'] = read_gowalla(self.people_param['data_file'])


    def compute_path_signature(self):
        '''for each user compute the path signature that is the sum of spot signatures 
        where the pearson has been'''

        def u_func(user):
            '''just try to paralilize this part of the code ... '''
            user_signatures = np.zeros((1, self.people_param['d']), dtype=int)
            for lat_, lon_ in self.people_param['pandas_data']\
                [self.people_param['pandas_data']['user_id'] == user][['lat','lon']].as_matrix():
                _sig = np.array([x for x in self.sites_find_closer_site(lat_, lon_, 5)\
                                                       ['spot_signature']], dtype=int)
                user_signatures = np.append(user_signatures, _sig, axis=0)
            user_signature = np.sum(user_signatures, axis=0)
	    df_user = pd.DataFrame([[user, user_signature]],
			columns=('user_id','user_signature'))
            self.df = self.df.append(df_user, ignore_index=True) 
            print '{} = {}'.format(user, user_signature)

        self.df = pd.DataFrame(columns=('user_id','user_signature'))
        
	# multithread ... user_id can be non integer?
	users_ = [ int(x) for x in self.people_param['pandas_data']['user_id'].unique()]
	Parallel(n_jobs=2)(delayed(u_func)(u) for u in users_)
        
	# # single thread
	# for user in self.people_param['pandas_data']['user_id'].unique():
	#     u_func(user)

        self.people_param['people_signatures'] = self.df

    def save_people_signatures(self, people_signatures_file):
        ''' save peoples signature in a pickle '''
        self.people_param['people_signatures'].to_pickle(people_signatures_file)


if __name__ == '__main__':
    
    # test for Eiffel Tower 
    pkl_file = 'data/spot_sig.pkl'
    pandas_pickle = 'data/sites_pandas.pkl'
    spot_signatures = 'data/spot_signatures.npz' # contain only the an numpy array with signatures
    data_gowalla_paris = 'data/loc-gowalla_totalCheckins_Paris.txt'
    p = People()
    if os.path.exists(pandas_pickle):
        print "Read pandas pickle ..."
        p.sites_from_pickle(pandas_pickle)
    else :
        p.get_spot_signature(pkl_file)
    
    p.get_people_data(data_gowalla_paris)
    p.compute_path_signature()
    people_signatures_file = 'data/people_signature.pkl'
    p.save_people_signatures(people_signatures_file)

