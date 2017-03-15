#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import random
import timeit

import numpy as np
import pandas as pd
import networkx as nx
import networkx.algorithms.approximation as nxa

import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances
from sklearn.neighbors import NearestNeighbors


from dspr.people import People, read_people_signatures,  parallel_comp_user_signature
from dspr.scikit_search import build_index_scikit, search_scikit
from dspr.fais_search import build_index_fais, search_fais

## set these variables in the config and then in bash do ". config"
try:
    SPOT_SIGNATURES = os.environ['SPOT_SIGNATURES']
except:
    print('SPOT_SIGNATURES')


try:
    PEOPLE_SIGNATURES = os.environ['PEOPLE_SIGNATURES']
except:
    print('SPOT_SIGNATURES')


#############################
# GENERAL VARS
d = 130 # signature dimension
k = 5
random.seed(1)

## files
pkl_file = 'data/spot_sig.pkl'
pandas_pickle = 'data/sites_pandas.pkl'
spot_signatures = 'data/spot_signatures.npz' # contain only the an numpy array with signatures
data_gowalla_paris = 'data/loc-gowalla_totalCheckins_Paris.txt'
people_signatures_file = 'data/people_signature.pkl'


##############################
### RESULT FROM THE REAL DATA
##############################


##############################
# LOADING DATASET
# people signatures
p_signatures = read_people_signatures(PEOPLE_SIGNATURES)
xb = np.array([x for x in p_signatures['user_signature']], dtype=np.float32)
# normalizing, not optimal but works
for n in range(len(xb)):
    s_ = xb.sum()
    if s_ != 0:
        xb[n] = xb[n]/s_

#xq = xb[:1] # query first value
xq = xb # query all values



################################
# Testing SCIKIT
print('Doing scikit NearestNeighbors ...')
index_scikit = build_index_scikit(xb, k, radius=1.0, algorithm='auto', leaf_size=30, metric='l2')
D_s, I_s = search_scikit(index_scikit, xq, k)
#print('Distances : {}\nneighbours={}'.format(D_s, I_s))
G_scikit=nx.Graph()
G_scikit.add_nodes_from(range(len(I_s)))
for n in I_s:
    G_scikit.add_edges_from(([(n[0], x) for x in n if x!=n[0]]))

print nx.info(G_scikit)

##############################
# Testing FAIS 
print('Doing faiss ...')
index_fais = build_index_fais(xb, d)
D_f, I_f = search_fais(index_fais, xq , k)
#print('Distances : {}\nneighbours={}'.format(D_f, I_f))
G_fais=nx.Graph()
G_fais.add_nodes_from(range(len(I_f)))
for n in I_f:
    G_fais.add_edges_from(([(n[0], x) for x in n if x!=n[0]]))

print nx.info(G_fais)


def apply_fun(fun, G1, G2):
    print '{}: {} {}'.format( fun.__name__, fun(G1), fun(G2))


func_ = [nx.transitivity, nxa.min_weighted_vertex_cover] #, nxa.maximum_independent_set, nxa.ramsey_R2]
func_ = [nx.transitivity, nxa.ramsey_R2]


################################
# looking for different metrics

print '~~~~~~~~~~~~~~~~~~~~~~'
print 'number of samples: {}'.format(len(I_f))
# are both the same?
print 'Is isomorphic: {}'.format(nx.is_isomorphic(G_scikit,G_fais))
print 'could be isomorphic: {}'.format(nx.could_be_isomorphic(G_scikit,G_fais))

# scores that needs more than 
# how dense are the connections
print 'median #triangles: {} {}'.format(np.median(nx.triangles(G_scikit).values()), 
                                        np.median(nx.triangles(G_fais).values()) )

# Compute graph transitivity, the fraction of all possible triangles present in G
print 'average clustering: {} {}'.format(nx.average_clustering(G_scikit), nx.average_clustering(G_fais))
print '#cliques: {} {}'.format( len(list(nx.find_cliques(G_scikit))), len(list(nx.find_cliques(G_fais))))
print '#min_maximal_matching : {} {}'.format(len(nxa.min_maximal_matching(G_scikit)), 
        len(nxa.min_maximal_matching(G_fais)) )

for fun in func_:
    apply_fun(fun, G_scikit, G_fais)

