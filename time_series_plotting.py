#! /usr/bin/python
## Author: Giulio Momente'
## emails: momenteg@gmail.com / gmomente@icecube.wisc.edu

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time


start_time=time.time() #taking current time as starting time

data_files=['2013.h5','2014.h5','2015.h5', '2016.h5'] 

for data_file in data_files:
	df = pd.read_hdf(data_file)
	grouped = df.groupby('day')
	mean_wo_tmp=grouped['Significance_without_muons'].agg([np.mean])
	mean_w_tmp=grouped['Significance_with_muons'].agg([np.mean])
	std_wo_tmp=grouped['Significance_without_muons'].agg([np.std])
	std_w_tmp=grouped['Significance_with_muons'].agg([np.std])
	mean_wo = pd.concat([mean_wo, mean_wo_tmp])
	mean_w = pd.concat([mean_w, mean_w_tmp])
	std_w = pd.concat([std_w,std_w_tmp])
	std_wo = pd.concat([std_wo,std_wo_tmp])
	del df, grouped, mean_wo_tmp, mean_w_tmp, std_w_tmp, std_wo_tmp

std_wo=std_wo.reset_index()
std_w=std_w.reset_index()
mean_wo=mean_wo.reset_index()
mean_w=mean_w.reset_index()

#setting the field day as date
std_wo['day']= pd.to_datetime(std_wo['day'], format='%Y-%m-%d')
std_w['day']= pd.to_datetime(std_w['day'], format='%Y-%m-%d')
mean_w['day']= pd.to_datetime(mean_w['day'], format='%Y-%m-%d')
mean_wo['day']= pd.to_datetime(mean_w['day'], format='%Y-%m-%d')


plt.plot(mean_wo['day'], mean_wo['mean'], label= 'mean w muon subtracted')
plt.grid(True)
plt.xticks(rotation=45)  # Changed here
plt.ylabel('Mean w/o muons')
plt.legend()
plt.savefig('plot/mean_w_muon_subtraction.pdf')
plt.show()

plt.plot(mean_w['day'], mean_w['mean'], label= 'mean w/o muon subtracted')
plt.grid(True)
plt.xticks(rotation=45)  # Changed here
plt.ylabel('Mean w muons')
plt.legend()
plt.savefig('plot/mean_wo_muon_subtraction.pdf')
#plt.savefig('plot/mean_compared.pdf')
plt.show()


plt.plot(std_w['day'], std_w['std'], label= 'std w/o muon subtracted')
plt.grid(True)
plt.ylabel('Std')
plt.xticks(rotation=45)  # Changed here
plt.legend()
plt.savefig('plot/std_wo_muon_subtraction.pdf')
plt.show()

plt.plot(std_wo['day'], std_wo['std'], label= 'std w muon subtracted')
plt.grid(True)
plt.ylabel('Std')
plt.xticks(rotation=45)  # Changed here
plt.legend()

plt.savefig('plot/std_w_muon_subtraction.pdf')
#plt.savefig('plot/std_compared.pdf')
plt.show()

print "It took {} seconds to execute this".format((time.time() - start_time) )
