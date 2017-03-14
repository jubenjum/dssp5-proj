#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import random


import numpy as np
import pandas as pd
import networkx as nx
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
k = 50
random.seed(1)

## files
pkl_file = 'data/spot_sig.pkl'
pandas_pickle = 'data/sites_pandas.pkl'
spot_signatures = 'data/spot_signatures.npz' # contain only the an numpy array with signatures
data_gowalla_paris = 'data/loc-gowalla_totalCheckins_Paris.txt'
people_signatures_file = 'data/people_signature.pkl'


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
xq = xb # query first value


################################
### Testing SCIKIT
##print('Doing scikit NearestNeighbors ...')
##index_scikit = build_index_scikit(xb, k, radius=1.0, algorithm='auto', leaf_size=30, metric='l2')
##D_s, I_s = search_scikit(index_scikit, xq, k=5)
##print('Distances : {}\nneighbours={}'.format(D_s, I_s))


##############################
# Testing SCIKIT
print('Doing faiss ...')
index_fais = build_index_fais(xb, d)
D_f, I_f = search_fais(index_fais, xq , k)
##print('Distances : {}\nneighbours={}'.format(D_f, I_f))

# graph selection
I = I_f

#### building a general the knn-graph on networkx ...
##G=nx.Graph()
##G.add_nodes_from(range(len(I)))
##for n in I:
##    G.add_edges_from(([(n[0], x) for x in n if x!=n[0]]))
##labels={}
##nx.draw_circular(G, node_color='y', edge_color='#909090',
##	node_size=1, label=labels)
##plt.axis('equal')
##plt.show()

# load data
p = People(pandas_pickle)
p.sites_from_pickle(pandas_pickle)
p.get_spot_signature(pkl_file)

# common to all figures
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
labels={}
len_I = range(len(I))

###### signatures from a random user 
p.get_people_data(data_gowalla_paris)
idx_ = p.get_user_idx(194166)
print 'similar to 194166={}'.format(I[idx_][0]) 

G=nx.Graph()
G.add_nodes_from(len_I)
edges_ = [(I[idx_][0], x) for x in I[idx_] if x != I[idx_][0]]
G.add_edges_from(edges_)
nx.draw_circular(G, node_color='r', edge_color='k', node_size=1, 
    ax=ax1, label=labels)
ax1.set_title('rand user [194166]', fontsize=10)
ax1.set_axis_off()
ax1.set_aspect('equal')

 
##### extract site signature for eiffel tower and compare it with users
eiffel = p.sites_find_closer_site(48.8584, 2.2945, 10)
eiffel_signature = np.array([x for x in eiffel['spot_signature']], dtype=np.float32).sum(axis=0)
eiffel_signature = np.array([eiffel_signature/eiffel_signature.sum()])
# who is the most similar to Eiffel signature?
D, I = search_fais(index_fais, eiffel_signature, k)
r_I = random.randint(0, k)
print 'similar to eiffel={}'.format(I[0][r_I])
# select randomly from friends

G=nx.Graph()
G.add_nodes_from(len_I)
G.add_edges_from([(I[0][r_I], x) for x in I[0] if x != I[0][r_I] ])
nx.draw_circular(G, node_color='r', edge_color='k', node_size=0.5, 
    ax=ax2, label=labels)
ax2.set_title('Eiffel Tower', fontsize=10)
ax2.set_axis_off()
ax2.set_aspect('equal')


##### compute the user signature for tourist lambda
df = parallel_comp_user_signature('data/log-gowalla_tourist.txt', pandas_pickle, d, n_neighbours=10, n_jobs=1)
turist_type_signature = df['user_signature'].values[0]
turist_type_signature = turist_type_signature.astype(np.float32)
turist_type_signature = np.array([turist_type_signature/turist_type_signature.sum()])
print 'similar to turist={}'.format(I[0][0])
D, I = search_fais(index_fais, turist_type_signature, k)
r_I = random.randint(0, k)

G=nx.Graph()
G.add_nodes_from(len_I)
G.add_edges_from([(I[0][r_I], x) for x in I[0] if x != I[0][r_I]])
nx.draw_circular(G, node_color='r', edge_color='k', node_size=1, 
    ax=ax3, label=labels)
ax3.set_title('Tourist', fontsize=10)
ax3.set_axis_off()
ax3.set_aspect('equal')


### a local ... with some check-ins
df = parallel_comp_user_signature('data/log-gowalla_juanbenjumea.txt', pandas_pickle, d, n_neighbours=10, n_jobs=1)
me = df['user_signature'].values[0]
me = me.astype(np.float32)
me = np.array([me/me.sum()])
D, I = search_fais(index_fais, me, k)
r_I = random.randint(0, k)
print 'similar to me={}'.format(I[0][r_I])

G=nx.Graph()
G.add_nodes_from(len_I)
G.add_edges_from([(I[0][r_I], x) for x in I[0] if x != I[0][r_I] ])
nx.draw_circular(G, node_color='r', edge_color='k', node_size=1, 
    ax=ax4, label=labels)
ax4.set_title('Juan B', fontsize=10)
ax4.set_axis_off()
ax4.set_aspect('equal')

plt.axis('equal')
plt.show()
##raw_input()
