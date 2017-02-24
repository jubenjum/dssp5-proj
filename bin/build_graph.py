#!/usr/bin/env python

import argparse
import sys

import networkx as nx
import pandas as pd
import numpy as np

from data import read_gowalla


# functions to read command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('edges_file', metavar='INPUT_FILE', nargs=1, help='...')
parser.add_argument('paris_file', metavar='INPUT_FILE', nargs=1, help='...')
args = parser.parse_args()
edges_file_ = args.edges_file[0]
paris_file_ = args.paris_file[0]

# reading the node; nodes on gowalla are integer values 
# separated by a space
df = pd.read_table(edges_file_, sep='\s+', header=None, names=['n1', 'n2']) 

# creating a the graph
G = nx.from_pandas_dataframe(df, 'n1', 'n2')

# select people that has visited the city
df_gowalla = read_gowalla(paris_file_)



