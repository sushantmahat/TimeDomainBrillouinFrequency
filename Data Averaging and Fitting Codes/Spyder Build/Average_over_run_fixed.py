# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 12:11:09 2021

@author: Mahat
"""

import numpy as np
import pandas as pd

#hardcoded for corrupt data; ignore. use average_now going forward
def average_old(file_name):
    raw_file  = file_name
    col_names = ['stg_pos','time delay','V_in','V_out','ratio','DVD'] 
    
    data_pd = pd.read_csv(raw_file,sep='\t', names=col_names)
    
    #get the last 20 data points () we got repeats due to wrong data taking; fixed for later sets
    
    
    data_non_re = data_pd.iloc[-4020:] 
    
    data_non_re['time delay'] = data_non_re['time delay'].round(decimals = 0)
    
    data_averaged = data_non_re.groupby('time delay').mean()
    
    #print(data_averaged)
    
    data_averaged.to_csv('averaged' + raw_file)
    
    #data_non_re.to_csv('raw_file'+'averaged', index = False)
    #print(data_pd.head())
    #print(data_sorted.nunique())

#main function:    
def average_now(file_name, return_prefix = 'averaged_'):
    raw_file  = file_name
    col_names = ['stg_pos','time delay','V_in','V_out','ratio','DVD'] 
    
    data_non_re  = pd.read_csv(raw_file,sep='\t', names=col_names)
    
    #get the last 20 data points () we got repeats due to wrong data taking; fixed for later sets
    
    
       
    data_non_re['time delay'] = data_non_re['time delay'].round(decimals = 0)
    
    data_averaged = data_non_re.groupby('time delay').mean()
    
    #print(data_averaged)
    
    data_averaged.to_csv(return_prefix + raw_file)
    
    #data_non_re.to_csv('raw_file'+'averaged', index = False)
    #print(data_pd.head())
    #print(data_sorted.nunique())
       
    




