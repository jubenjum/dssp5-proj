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
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from dspr.sites import Sites 

__all__ = ['People', 'read_people_signatures', 'read_gowalla', 'parallel_comp_user_signature' ]


# initilize environmental variables
try:
    NUM_JOBS = int(os.environ['NUM_JOBS'])
except:
    NUM_JOBS = 1


try:
    SPOT_SIGNATURES = os.environ['SPOT_SIGNATURES']
except:
    print('SPOT_SIGNATURES')
    raise


try:
    PEOPLE_SIGNATURES = os.environ['PEOPLE_SIGNATURES']
except:
    print('SPOT_SIGNATURES')


def read_people_signatures(people_signature_file):
    ''' read the people signature pickles file that contains a pandas dataframe
    with user_id and its user_signature build from the spot signatures 
    '''
    with open(people_signature_file) as pfile:
        people_signatures = pickle.load(pfile)
    return people_signatures 


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

    
    def get_user_idx(self, user_id):
        '''given a user_id return the pandas idx, it will help to know other information
        for the user
        '''
        if not self.people_param['people_signatures']:
               self.people_param['people_signatures'] = read_people_signatures(PEOPLE_SIGNATURES)
	try:
            s_ = self.people_param['people_signatures']
            idx_ = s_[s_['user_id'] == user_id].index[0]
        except:
            raise ValueError('no PEOPLE_SINGATURE // problem in get_user_idx ... nothing found')
        
        return idx_


    def get_user_signature(self, user_id):
        '''get user signature as an np array'''
        if not self.people_param['people_signatures']: 
            self.people_param['people_signatures'] = read_people_signatures(PEOPLE_SIGNATURES)

	try:
            s_ = self.people_param['people_signatures']  
            r_ = s_[s_['user_id'] == user_id]['user_signature'].values[0]
            r_ = r_.astype(np.float32) # or with copy=False
	
	except:
	    raise ValueError('no PEOPLE_SINGATURE // get_user_signature')
	
        return r_


    def save_people_signatures(self, people_signatures_file):
        ''' save peoples signature in a pickle '''
        self.people_param['people_signatures'].to_pickle(people_signatures_file)


    def compute_user_signature(self):
        '''for each user compute the user signature that is the sum of spot signatures 
        where the pearson has been'''
	self.people_param['people_signatures'] = _compute_user_signature(self.people_param['pandas_data'], \
	         self.people_param['d'], self.sites_param['pandas_data'])


def _compute_user_signature(people_data, d, spot_data):
    ''' single thread computation of user signature (used insde People class) '''
    df = pd.DataFrame(columns=('user_id','user_signature'))
    for user in people_data['user_id'].unique():
       _r = h_func_signature(user, people_data, d, spot_data)
       df = df.append(_r, ignore_index=True) 

    return df 

def h_func_signature(user, pandas_data, d, spot_data, n_neighbours=5):
    ''' computing the people signatures from their checkins using n_neighbours'''
    user_signatures = np.zeros((1, d), dtype=int)
    for lat_, lon_ in pandas_data[pandas_data['user_id'] == user][['lat','lon']].as_matrix():
        idx_ =  spot_data.apply(lambda x: np.sqrt((x['lat']-lat_)**2.0 \
                + (x['lon'] - lon_)**2.0), axis=1).sort_values(ascending=[1]).head(n_neighbours).index.tolist()
        _sig = np.array([x for x in spot_data.spot_signature.iloc[idx_]], dtype=int)
        user_signatures = np.append(user_signatures, _sig, axis=0)
    user_signature = np.sum(user_signatures, axis=0)
    df_user = pd.DataFrame([[user, user_signature]], columns=('user_id','user_signature'))
    print '{} = {}'.format(user, user_signature)
    return df_user


def parallel_comp_user_signature(pandas_data, pandas_pickle, d, n_neighbours, n_jobs=1):
    ''' the same that _compute_user_signature but multithread '''
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

    from sklearn.metrics import pairwise_distances
    # test for Eiffel Tower 
    pkl_file = 'data/spot_sig.pkl'
    pandas_pickle = 'data/sites_pandas.pkl'
    spot_signatures = 'data/spot_signatures.npz' # contain only the an numpy array with signatures
    data_gowalla_paris = 'data/loc-gowalla_totalCheckins_Paris.txt'
    people_signatures_file = 'data/people_signature.pkl'
    d = 130 # the number of dimensions
    
    # compute all user signatures
    #df = parallel_comp_user_signature(data_gowalla_paris, pandas_pickle, d, n_neighbours=10, n_jobs=NUM_JOBS)
    #df.to_pickle(people_signatures_file) # contains user and user_signature

    p = People(pandas_pickle)
    if os.path.exists(pandas_pickle):
        print "Read pandas pickle ..."
        p.sites_from_pickle(pandas_pickle)
    else :
        p.get_spot_signature(pkl_file)
   
    fig, ax = plt.subplots(1)
    # compute all people signatures from the get_people_data
    p.get_people_data(data_gowalla_paris)
    random_user_signature = p.get_user_signature(194166.0)
    random_user_signature = random_user_signature/random_user_signature.sum()
    ax.plot(random_user_signature, label='random user [id=194166]')

    # extract site signature for eiffel tower
    eiffel = p.sites_find_closer_site(48.8584, 2.2945, 10)
    eiffel_signature = np.array([x for x in eiffel['spot_signature']], dtype=np.float32).sum(axis=0)
    eiffel_signature = eiffel_signature/eiffel_signature.sum()
    ax.plot(eiffel_signature, label='Eiffel Tower', linewidth=2)
    
    # compute the user signature for tourist lambda
    df = parallel_comp_user_signature('data/log-gowalla_tourist.txt', pandas_pickle, d, n_neighbours=10, n_jobs=1)
    turist_type_signature = df['user_signature'].values[0]
    turist_type_signature = turist_type_signature.astype(np.float32)
    turist_type_signature = turist_type_signature/turist_type_signature.sum() 
    ax.plot(turist_type_signature, label='Tourist')
    ax.set_xlabel('features/signatures')
    ax.set_ylabel('normalized counting')
    ax.legend()

    # a local ... with some check-ins 
    df = parallel_comp_user_signature('data/log-gowalla_juanbenjumea.txt', pandas_pickle, d, n_neighbours=10, n_jobs=1)
    me = df['user_signature'].values[0]
    me = me.astype(np.float32)
    me = me/me.sum()
    plt.plot(me/me.sum(), label='Juan B')
    plt.legend()

    ## joining all signatures to compute 
    fig, ax_ = plt.subplots(1)
    data_points = np.array([random_user_signature, eiffel_signature, turist_type_signature, me])  
    all_ = np.array([random_user_signature, eiffel_signature, turist_type_signature, me])
    l2_sim =  1-pairwise_distances(all_, metric='l2') # similitude 1=same, 0=diff,  0.5=orthogonal
    labels_ = ['rand user', 'Eiffel Tower', 'Tourist','Juan B']
    column_labels = labels_
    row_labels = labels_
    data = np.array(l2_sim)
    fig, ax = plt.subplots(1,figsize=(14,5))
    ax_.pcolor(data, cmap=plt.cm.Reds)
    ax_.set_xticks(np.arange(data.shape[1])+0.5, minor=False)
    ax_.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
    ax_.invert_yaxis()
    ax_.yaxis.tick_right()
    ax_.set_xticklabels(row_labels, minor=False, rotation=0, fontsize=20)
    ax_.set_yticklabels(column_labels, minor=False, fontsize=20)
    ax_.set_title("L2 similarities");
    print l2_sim
    plt.show()
    raw_input()
