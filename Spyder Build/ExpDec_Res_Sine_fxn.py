# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 11:54:16 2021
created to be function 
personal note:
Origin fitting is getting more cumbersome by the day.
Most of my data sets only require a simple polynomial fitting followed by Sine fitting.
I will try to automate the Sine fitting process, but worst case scenario
approximation of some the frequency parameters might be needed.

Code notes:
    
Stand alsone program. Run on any data that has been csv data that has the 
appropriate heading. If raw data does not have heading, I suggest you add 
some column headings manually. The ones that are absolutely required are the
timde delay and the V_in ccolumns. Code should run a two column csv file just fine.

The code does two things: Polynomial fit to data provided to substract background from it
followed by a Sine fit to the residual.

The polynomial fit is of the order 5 since that is smooth enough to capture any background.

The palan is to get the sine fitting process to infer the approximate frequency by
using FFT. 

I will convert some of these routines to functions just so I can call them in my 
Bulk_data.py routine.


@author: smahat2
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp 
from scipy import optimize

#define Sine funciton for Sine fitting at end of routine:

def s_fxn(x, A, f, p , c):
    return A * np.sin(2 * np.pi * f * x + p) + c

#initilization; some of these will be input values if I decide to make this into a function
#filename  = 'averagedAcoustic08_MgO_110_Ni_105_deg_x10_20_avg'     
#poly_odr  = 5


def fit_fxn(filename, poly_odr):
    #make pandas: should have the proper column headings if I applied the average function on them.
    main_data = pd.read_csv(filename)
    
    #internal testing, comment out:
    #print(main_data.head())
    
    
    #do the fit with an appropriate polynomial function of order poly_oder (default 5)
    poly_coeff   = np.polynomial.polynomial.polyfit(main_data['time delay'], main_data['V_in'], poly_odr)
    poly_fun     = np.polynomial.Polynomial(poly_coeff) #this is now a polynomial function that takes in x
    
    #feed time delay values to calculate polynomial background; add it at end of dataframe:
    main_data.insert(len(main_data.columns), 'poly fit', poly_fun(main_data['time delay']))
    #calculate residuals and store it at end of dataframe:
    main_data.insert(len(main_data.columns), 'poly res', main_data['V_in'] - main_data['poly fit'] ) 
    
    #internal testing, comment out:
    #print(main_data.head())
    
    
    
    #figure to check the fit is being carried out correctly:
    fig_ax = main_data.plot.scatter(x = 'time delay', y = 'V_in',color = 'blue', fontsize = 15, title = filename) #define set of figure axis
    main_data.plot(x = 'time delay', y = 'poly fit', label = 'Background fit', linewidth = 2, color = 'green', ax = fig_ax)
    
    #Additional formatting for graph shown:
    #fig_ax.set(xlabel = 'Time Delay / ps', ylabel = 'V_in / uV', fontsize = 15 ) #fontsize throws error, kept in as memo for future
    fig_ax.set_xlabel('Time Delay / ps', fontsize = 15 )
    fig_ax.set_ylabel('V_in / uV', fontsize = 15 )
    
    
    
    #Find initial value for the sine fit parameters:
    #Note: parameter A and f are both unknown. A can be approximated as the max possible value of residual
    #Note: parac should be 0 since this is residual from line of best fit 
    paraA = main_data['poly res'].max()
    parac = 0
    #Note: data doesn't start at zero
    parap = main_data['time delay'].min()
    #next few lines handle f:
    paraf = 50 / 1000 #default; good guess for the samples I deal with now.
    #account for step size used to take data; units is ps 
    stepS   = main_data['time delay'][2] - main_data['time delay'][1]
    #do a fft of the dataset and get the absolute value 
    fft_Arr = sp.fft(main_data['poly res'])
    fft_pwr = np.abs(fft_Arr) ** 2
    #define frequency based on range and the stepS. This will set frequency to per ps.
    fft_farr = np.fft.fftfreq(len(fft_pwr) , stepS / 1) 
    
    #might as well add them to the main dataframe; can allow for calculation of A through other means
    main_data.insert(len(main_data.columns), 'Residual FFT', fft_pwr)
    main_data.insert(len(main_data.columns), 'Associated F', fft_farr)
    
    ''' 
    #un/comment this portion to un/see FFT graph 
    
    fig_axFFT = main_data.plot(x = 'Associated F', y = 'Residual FFT', logy= 1, ylim = [1e-1, 1e6], color = 'blue', fontsize = 15, title = filename)
    fig_axFFT.set_xlabel('frequency 1 / ps', fontsize = 15)
    fig_axFFT.set_ylabel('Amplitude', fontsize = 15)
    '''
    
    #find the primary frequency associated with the largest FFT peak and assign paraf:
    paraf = main_data['Associated F'][main_data['Residual FFT'].idxmax()]
    
    
    #internal testing, comment out:
    #print('frequency is ' + str(paraf*1000) + ' GHz' )
    
    #Fit Sinosoidal fit to residual:
    sin_para, para = sp.optimize.curve_fit(s_fxn, main_data['time delay'], main_data['poly res'], p0 = [paraA, paraf, parap, parac] )
    
    #internal testing, comment out:
    #print('best fit is' + str(sin_para))
    
    #keep track of this data:
    main_data.insert(len(main_data.columns), 'Sine Res Fit', s_fxn(main_data['time delay'], sin_para[0], sin_para[1], sin_para[2], sin_para[3]))
    
    
    
    fig_ax2 = main_data.plot.scatter(x = 'time delay', y = 'poly res', color = 'blue', label = 'Residual', fontsize = 15, title = filename)
    main_data.plot(x = 'time delay', y = 'Sine Res Fit', linewidth = 2, color = 'green', label = 'Sine Fit', ax = fig_ax2)
    
    #Additional formatting for graph shown:
    #fig_ax.set(xlabel = 'Time Delay / ps', ylabel = 'V_in / uV', fontsize = 15 )
    fig_ax2.set_xlabel('Time Delay / ps', fontsize = 15 )
    fig_ax2.set_ylabel('Residual V_in / uV', fontsize = 15 )
    
    #make a file to save process:
    main_data.to_csv('fitted_poly_odr_' + str(poly_odr)+ ' ' + filename)
    
    #fit analysis:
    fit_res = main_data['Sine Res Fit'] - main_data['poly res']
    sq_fit  = fit_res**2
    err_fit = (sq_fit.sum()/len(sq_fit))**0.5
    
    #internal testing, comment out:
    #print(err_fit) 
    #print(main_data.head())
    
    return [paraA, paraf, parap, parac, err_fit]
   
#internal testing, comment out:
#print(fit_fxn(filename, poly_odr))

