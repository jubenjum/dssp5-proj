#!/usr/bin/env python
''' module with functions to read data from gowalla and
other sources
'''

import pandas as pd


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



