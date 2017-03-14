#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import timeit

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances
from sklearn.neighbors import NearestNeighbors
plt.style.use('ggplot')  

from dspr.scikit_search import build_index_scikit, search_scikit
from dspr.fais_search import build_index_fais, search_fais


#############################
# GENERAL VARS
d = 256 # signature dimension will be fixed
k = 50

##############################
t_scikit = list() 
t_fais = list()
ns = [100, 200, 400, 800, 900, 1000, 
      2000,  4000, 8000] 
      
for n in ns:
    print n
    xb = np.random.random((n,d)).astype(np.float32)
    
    ################################
    # Testing SCIKIT
    index_scikit = build_index_scikit(xb, k, radius=1.0, algorithm='auto', leaf_size=30, metric='l2')
    
    b = list()
    for m in range(5):
        t0 = time.time()
        D_s, I_s = search_scikit(index_scikit, xb, k)
        b.append(time.time()-t0)
    t_scikit.append(np.median(b))
    
    ##############################
    # Testing fais 
    index_fais = build_index_fais(xb, d)
    b = list()
    for m in range(5):
        t0 = time.time()
        D_f, I_f = search_fais(index_fais, xb, k)
        b.append(time.time()-t0)
    t_fais.append(np.median(b))

fig, ax = plt.subplots() 
plt.loglog(ns, t_scikit, label='scikit')
plt.loglog(ns, t_fais, label='fais')
#ax.set_xticklabels(day)
#ax.set_title('Check-in by day of week')
plt.xlim(0, 10000)
plt.ylim(0, 100)
ax.set_ylabel('time [s]')
ax.set_xlabel('#samples')
ax.legend()
plt.show()

