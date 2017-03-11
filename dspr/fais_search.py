#!/usr/bin/env python

import os
import cPickle as pickle

import pandas as pd
import numpy as np
#from sklearn.neighbors import NearestNeighbors


# import faiss library or stop!
try:
    import faiss
except ImportError:
    print('faiss library not found ... ')
    print('install from faiss directory and load config file ... ')
    raise 

try:
    SPOT_SIGNATURES = os.environ['SPOT_SIGNATURES']
except:
    print('SPOT_SIGNATURES')


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


def build_index_FlatL2(xb, d):
    ''' I am using the variable conventions from 
    https://github.com/facebookresearch/faiss/wiki/Getting-started-tutorial
    
    the objective is to train an index 

    xb : numpy matrix with the signatures database with np.float32 values
    d  : signature dimension (130 if using google sites)
    
    the function returns the trained index  
    '''
    # building the index 
    index = faiss.IndexFlatL2(d)   # build the index
    assert index.is_trained
    index.add(xb)                  # add vectors to the index
    print('index ntotal={}'.format(index.ntotal))
    return index

def build_index_IVFFlat(xb, d, nlist=10):
    '''index with Voronoi cells in the d-dimensional space,
    and each signature database  falls in one of the cells

    xb : numpy matrix with the signatures database with np.float32 values
    d  : signature dimension (130 if using google sites)
    nlist : number of Veronoi spaces

    the function returns the trained index  
    '''
    quantizer = faiss.IndexFlatL2(d)  # the other index
    index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_L2)
    
    # here we specify METRIC_L2, by default it performs inner-product search
    assert not index.is_trained
    index.train(xb)
    assert index.is_trained
    index.add(xb)                  # add may be a bit slower as well
    return index 



def build_index_IVFFlatQ(xb, d, m=8, nlist=10):
    '''index with Voronoi cells in the d-dimensional space with 
    that vector projected to a m-bit quantized space, 
    each signature database falls in one of the cells. and d%m == 0

    xb : numpy matrix with the signatures database with np.float32 values
    d  : signature dimension (130 if using google sites)
    nlist : number of Veronoi spaces
    m : number of bits used in the quatization of the signatures

    the function returns the trained index  
    '''

    assert d%m == 0 # d must be a multiple of m


    quantizer = faiss.IndexFlatL2(d)  # this remains the same
    index = faiss.IndexIVFPQ(quantizer, d, nlist, m, 8)
    # 8 specifies that each sub-vector is encoded as 8 bits
    index.train(xb)
    index.add(xb)
    return index 


def search_knn_FlatL2(index, xq, k=5):
    ''' search K nearest-neighbor from the trained index, for the
    the query xq, the inputs are:

    index : trained index (with build_index_FlatL2)
    xq    : numpy matrix/vectors with the signatures to search in the database, 
            they should be np.float values 
    k     : the K for KNN graph

    it will return the distance D and the indexes I
    '''
    D, I = index.search(xq, k)     # actual search, D = L2 distance, I index with 
    return D, I 


def search_knn_IVFFlat(index, xq, k=5):
    '''
    search K nearest-neighbor from the trained index, from Veronoi subspaces, 
    using the query xq, the inputs are:
    
    index : trained index (with build_index_FlatL2)
    xq    : numpy matrix/vectors with the signatures to search in the database, 
            they should be np.float values 
    k     : the K for KNN graph

    it will return the distance D and the indexes I
    '''
    index.nprobe = 1             # default nprobe is 1, try a few more
    D, I = index.search(xq, k)    # actual search
    return D, I


def search_knn_IVFFlatQ(index, xq, k=5):
    '''
    search K nearest-neighbor from the trained index, from Veronoi subspaces, 
    using the query xq, the inputs are:
    
    index : trained index (with build_index_FlatL2)
    xq    : numpy matrix/vectors with the signatures to search in the database, 
            they should be np.float values 
    k     : the K for KNN graph

    it will return the distance D and the indexes I
    '''
    index.nprobe = 10            
    D, I = index.search(xq, k)    # actual search
    return D, I

if __name__ == '__main__':

    print('Doing search ...\n')
    d = 130 # signature dimension
    p_signatures = read_people_signatures(PEOPLE_SIGNATURES)
    xb = np.array([x for x in p_signatures['user_signature']], dtype=np.float32)

    # building index FlatL2, and 
    print('Doing FlatL2 ...')
    index_FlatL2 = build_index_FlatL2(xb, d)
    # I am intereted to know who is similar (friend, k=5) of pearson 0
    D_FL2, I_FL2 = search_knn_FlatL2(index_FlatL2, xb[:1] , k=5)
    print('Distances : {}\nneighbours={}'.format(D_FL2, I_FL2))
    ## using the IVFFLAT - Veronoi Algorithm 
    #print('Doing IVFFlat ...')
    #index_IVFFlat = build_index_IVFFlat(xb, d)
    #D_IVF, I_IVF = search_knn_IVFFlat(index_IVFFlat, xb[:1] , k=5)

    ## IVFFlatQ - Veronoi Quantized
    ## as the the quatization needs m must be mutiple of d, then I padded with 0 at the end
    ## of the person signatture to have m=8 and d=136
    #m = 8; new_d = 136 
    #xb_136 = np.pad(xb, (0, new_d-d), 'constant', constant_values=(0,0)) 
    #index_IVFFlatQ = build_index_IVFFlatQ(xb_136, new_d, m)
    #D_IVFQ, I_IVFQ = search_knn_IVFFlatQ(index_IVFFlatQ, xb[:1] , k=5)



