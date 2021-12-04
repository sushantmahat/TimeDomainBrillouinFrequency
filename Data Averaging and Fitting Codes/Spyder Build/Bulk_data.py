# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 11:31:47 2021

@author: smahat2
"""

import ExpDec_Res_Sine_fxn as sig_fit
import Average_over_run_fixed as avg
import glob
import numpy as np


file_prefix   = 'Acoustic'
return_prefix = 'averaged_'

#import and average data:
true_str      = file_prefix + '*'
file_names    = glob.glob(true_str)

for n, i in enumerate(file_names):
    avg.average_now(i, return_prefix)

#do the analysis:

fit_results = []
    
for n, i in enumerate(file_names):
    fit_results.append(sig_fit.fit_fxn(return_prefix + i, 5))
    

#output summary file ( tab delimited)

output_smr = open('Averaged_Summary_' + file_prefix, 'w')

for n, i in enumerate(fit_results):
    output_smr.write(file_names[n] + '\t ' )
    for j in i:
        output_smr.write(str(j) + '\t')
    output_smr.write("\n")
    
output_smr.close()