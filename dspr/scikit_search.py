#!/usr/bin/env python

import os

import numpy as np
from sklearn.neighbors import NearestNeighbors

from dspr.people import read_people_signatures

__all__ = ['build_index_scikit', 'search_scikit']


try:
    SPOT_SIGNATURES = os.environ['SPOT_SIGNATURES']
except:
    print('SPOT_SIGNATURES')


try:
    PEOPLE_SIGNATURES = os.environ['PEOPLE_SIGNATURES']
except:
    print('SPOT_SIGNATURES')


def build_index_scikit(xb, k, radius, algorithm, leaf_size, metric):
    ''' '''
    index_scikit = NearestNeighbors(k, radius, algorithm, leaf_size, metric)
    index_scikit.fit(xb)
    return index_scikit


def search_scikit(index, xq, k):
    ''' '''
    D, I = index.kneighbors(xq, k, return_distance=True) 
    return D, I 


if __name__ == '__main__':

    print('Doing search ...\n')
    d = 130 # signature dimension
    k = 5
    p_signatures = read_people_signatures(PEOPLE_SIGNATURES)
    
    # I am values than faiss to do the tests  
    xb = np.array([x for x in p_signatures['user_signature']], dtype=np.float32)
    
    # normalizing 
    for n in range(len(xb)):
        s_ = xb.sum()
        if s_ != 0:
            xb[n] = xb[n]/s_ 

    # building index FlatL2, and 
    print('Doing NearestNeighbors ...')
    index_scikit = build_index_scikit(xb, k=5, radius=1.0, algorithm='auto', leaf_size=30, metric='l2')
    D, I = search_scikit(index_scikit, xb[:1], k=5) 
    print('Distances : {}\nneighbours={}'.format(D, I))


