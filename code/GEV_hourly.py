# -*- coding: utf-8 -*-
"""
@author: giandomenico mastrantoni | giandomenico.mastrantoni@uniroma1.it
"""

# CALCULATION OF PROBABILITY CURVES WITH GEV ANALYSIS ON HOURLY PRECIPITATION.

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
#from matplotlib.legend_handler import HandlerLine2D

from matplotlib.pylab import figure
figure(num=None, figsize=(15,8), dpi=96, facecolor='w', edgecolor='black')


import lmoments3 as lm3
from lmoments3 import distr

from os import listdir

# list of pluvio station files and set the choice from there.
files = listdir(r"C:\Users\giand\Documents\PhD_Scienze_della_Terra\Database_Hazard\Roma\Stazioni Pluviometriche\1951-2021_processed\orarie")

stazioni = []
for file in files:
    files_cln = file.strip('.xlsx')
    stazioni.append(files_cln)
del files_cln, file

print(*stazioni, sep='\n')

# #------
# # User input to select the station of interest.
# stazione = input('Please, input one station among those listed above: ')
# year_maximum_orarie = pd.read_excel(filepath, index_col='Year')
# # load the chosen station
# filepath = "C:/Users/giand/Documents/PhD_Scienze_della_Terra/Database_Hazard/Roma/Stazioni Pluviometriche/1951-2021_processed/orarie/" + stazione + '.xlsx'
# #-----------
   
# hourly cumulated rainfall
h = [1, 3, 6, 12, 24]


# function to compute GEV parameters.
def TR_GEV_h(year_maximum_orarie):
    rainfall_ = {}
    
    # return years T (2,4,10,20,50,100)
    T = np.array([2,4,10,20,50,100])
    # T = np.array([2,5,10])
    for year in T:
        tr_list = []
        
        for i in range(len(h)):
            LMU = lm3.lmom_ratios(year_maximum_orarie.iloc[:,i])
            gevfit = distr.gev.lmom_fit(year_maximum_orarie.iloc[:,i], lmom_ratios=LMU)
            c, scale, loc = gevfit['c'], gevfit['scale'], gevfit['loc']
        
            rapp = scale/c
            ln = np.log((year-1)/year)
            power = np.power(-ln, c)
            tr = rapp * (1-power) + loc
            tr_list.append(tr)
            
        rainfall_['{0}'.format(year)] = tr_list
    rainfall_rt = pd.DataFrame(rainfall_, index=h)
    path = r'1951-2021_processed\orarie_results\temp\rainfall_rt_orarie_{}.xlsx'.format(stazione)
    # rainfall_rt.to_excel(path, float_format='%.3f')
    
    return rainfall_rt


## Plot function with fitted return period curves.
from scipy.optimize import curve_fit

def powlaw(x, a, b) :
    return a * np.power(x, b)

# iterate over all available stations
for stazione in stazioni:
    filepath = "C:/Users/giand/Documents/PhD_Scienze_della_Terra/Database_Hazard/Roma/Stazioni Pluviometriche/1951-2021_processed/orarie/" + stazione + '.xlsx'
    year_maximum_orarie = pd.read_excel(filepath, index_col='Year')
    if year_maximum_orarie.shape[0] < 10:
        print(stazione + ' has insufficient lenght of data for specified moments')
        
    else:
        rainfall_rt = TR_GEV_h(year_maximum_orarie)

        # fitting power law on GEV results.
        figure(num=None, figsize=(15,8), dpi=96, facecolor='w', edgecolor='black')
        for year in rainfall_rt.columns:
            plt.scatter(rainfall_rt.index, rainfall_rt[year])
            
            popt, pcov = curve_fit(powlaw, rainfall_rt.index, rainfall_rt[year])
            plt.plot(np.arange(1,24.5, 0.5), powlaw(np.arange(1,24.5, 0.5), *popt), label=year)
        
        plt.ylabel('Cumulated rain [mm]', fontsize=18)
        plt.xticks(h, fontsize=14)
        plt.yticks(np.arange(0,220, 20), fontsize=14)
        plt.xlabel('Hours', fontsize=18)
        plt.legend(title="Years", 
                loc=2, fontsize='medium', title_fontsize='large', fancybox=True)
        plt.title('W. Station: '+ stazione + ' (Roma)', fontsize=24)
        plt.gca().spines['top'].set_linewidth(2)
        plt.gca().spines['bottom'].set_linewidth(2)
        plt.gca().spines['left'].set_linewidth(2)
        plt.gca().spines['right'].set_linewidth(2)
        plt.grid(color='black', alpha=0.1)
        # plt.savefig(r'C:\Users\giand\Documents\PhD_Scienze_della_Terra\Database_Hazard\Roma\Stazioni Pluviometriche\1951-2021_processed\orarie_results\rt_orarie_{}.svg'.format(stazione), format='svg')
        plt.show()
