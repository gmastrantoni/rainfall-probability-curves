# -*- coding: utf-8 -*-
"""
@author: giandomenico mastrantoni | giandomenico.mastrantoni@uniroma1.it
"""
# %%
import os
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
#from matplotlib.legend_handler import HandlerLine2D

from matplotlib.pylab import rcParams
from matplotlib.pylab import figure
#rcParams['figure.figsize'] = 15, 8
figure(num=None, figsize=(15,8), dpi=96, facecolor='w', edgecolor='black')


import lmoments3 as lm3
from lmoments3 import distr
#from scipy.stats import genextreme
#%matplotlib auto

# %%
# load pluviometric records
folder_roma = r"C:/Users/giand/Documents/PhD_Scienze_della_Terra/Database_Hazard/Roma/Stazioni Pluviometriche/1951-2021_processed/"
roma_file = r"precipitazioni_1951-2021_all_stations.csv"
filepath = os.path.join(folder_roma, roma_file)

data = pd.read_csv(filepath, parse_dates=[0])

day, month, year = [], [], []
for date in data['Data']:
    day.append(date.day)
    month.append(date.month)
    year.append(date.year)

data['day'] = day
data['month'] = month
data['year'] = year
del(day, month, year, date)
#data.mm.hist(bins=50)
# Removing data before 6-luglio-1951
filtro = data.Data >= '1951-07-06'
data_flt = data[filtro]

print(*data.columns[1:-3], sep='\n')

stazione = input('\n'+ 'Please, input one station among those listed above: ')
df_stazione = data_flt[[stazione, 'Data']].rename(columns={stazione:'mm'})

# %%
# COMPUTE CUMULATIVE RAINFALL PER 2,5,10,30,60,90,120,180 DAYS
cum_days = [2,5,10,20,30,60,90,120,180,365]
# cum_days = [3,5,7,10]
cumulative_ = {}
for i in cum_days:
    cumulative_['{0}'.format(i)] = df_stazione.mm.rolling(i, min_periods=1).sum()
del(i)


df_cum = pd.DataFrame(cumulative_)
#df_cum.dropna(axis=0, inplace=True)
df_cum['year'] = data_flt.year
#df_cum['month'] = data.month
#df_cum['day'] = data.day

# COMPUTE MAXIMUM VALUE BY YEAR and CUMULATIVE DAYS
year_maximum_cum = df_cum.groupby('year').max()
year_maximum_cum_cln = year_maximum_cum.reset_index(drop=True)
year_maximum_cum_cln.dropna(axis=0, inplace=True)


# function to compute GEV parameters.
def TR_GEV():
    rainfall_ = {}
    
    # return years T (2,4,10,20,50,100)
    T = np.array([2,4,10,20,50,100])
    T = np.array([2,5,10])
    for year in T:
        tr_list = []
        
        for i in range(len(cum_days)):
            LMU = lm3.lmom_ratios(year_maximum_cum_cln.iloc[:,i])
            gevfit = distr.gev.lmom_fit(year_maximum_cum_cln.iloc[:,i], lmom_ratios=LMU)
            c, scale, loc = gevfit['c'], gevfit['scale'], gevfit['loc']
        
            rapp = scale/c
            ln = np.log((year-1)/year)
            power = np.power(-ln, c)
            tr = rapp * (1-power) + loc
            tr_list.append(tr)
            
        rainfall_['{0}'.format(year)] = tr_list
    rainfall_rt = pd.DataFrame(rainfall_, index=cum_days)
    
    return rainfall_rt

rainfall_rt = TR_GEV()

# save rainfall tr
# rainfall_rt.to_excel(os.path.join(folder, 'rainfall_rt_{}.xlsx'.format(stazione)))

#%%
## Plot function with fitted return period curves.
from scipy.optimize import curve_fit

def powlaw(x, a, b) :
    return a * np.power(x, b)
figure(num=None, figsize=(18,10), dpi=96, facecolor='w', edgecolor='black')
for year in rainfall_rt.columns:
    plt.scatter(rainfall_rt.index, rainfall_rt[year])
    
    popt, pcov = curve_fit(powlaw, rainfall_rt.index, rainfall_rt[year])
    plt.plot(np.arange(1,366), powlaw(np.arange(1,366), *popt), label=year)

plt.ylabel('Cumulated rain [mm]', fontsize=18)
plt.xticks(cum_days, fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Days', fontsize=18)

plt.legend(title="Years", 
            loc=2, fontsize='medium', title_fontsize='large', fancybox=True)
plt.title('W. Station: '+ stazione, fontsize=24)
plt.gca().spines['top'].set_linewidth(2)
plt.gca().spines['bottom'].set_linewidth(2)
plt.gca().spines['left'].set_linewidth(2)
plt.gca().spines['right'].set_linewidth(2)
plt.grid(color='black', alpha=0.1)
# plt.savefig(os.path.join(folder, 'rt_{}.svg'.format(stazione)), format='svg', bbox_inches='tight')
plt.show()
