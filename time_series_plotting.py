#! /usr/bin/python
## Author: Giulio Momente'
## emails: momenteg@gmail.com / gmomente@icecube.wisc.edu

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import time
import gc
import datetime

mean_wo = pd.DataFrame()
mean_w = pd.DataFrame()
std_w = pd.DataFrame()
std_wo = pd.DataFrame()

start_time=datetime.datetime.now() #taking current time as starting time

data_files=['2012.h5','2013.h5','2014.h5','2015.h5', '2016.h5', '2008_2011.h5'] 
#data_files=['2008_2011.h5','2014.h5','2015.h5', '2016.h5'] 
#data_files=['2012.h5','2013.h5'] 


for data_file in data_files:
	print data_file
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
	print mean_wo.info()
	print mean_w.info()
	del df, grouped, mean_wo_tmp, mean_w_tmp, std_w_tmp, std_wo_tmp
	gc.collect()

std_wo=std_wo.reset_index()
std_w=std_w.reset_index()
mean_wo=mean_wo.reset_index()
mean_w=mean_w.reset_index()

#setting the field day as date
std_wo['day']= pd.to_datetime(std_wo['day'], format='%Y-%m-%d')
std_w['day']= pd.to_datetime(std_w['day'], format='%Y-%m-%d')
mean_w['day']= pd.to_datetime(mean_w['day'], format='%Y-%m-%d')
mean_wo['day']= pd.to_datetime(mean_w['day'], format='%Y-%m-%d')


fig_mean = plt.figure()
ax= fig_mean.add_subplot(1,1,1)

fig_std = plt.figure()
ax1= fig_std1.add_subplot(1,1,1)

plt.plot(mean_wo['day'], mean_wo['mean'], label= 'mean w/o muons')
plt.grid(True)
plt.ylabel('Mean w/o muons')
plt.legend(loc='best')
mean_wo=plt.gca()
mean_wo.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m\n%Y'))
plt.savefig('plot/mean_w_muon_subtraction.pdf')
plt.show()

plt.plot(mean_w['day'], mean_w['mean'], label= 'mean w muons')
plt.grid(True)
plt.ylabel('Mean w muons')
plt.legend(loc='best')
mean_w=plt.gca()
mean_w.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m\n%Y'))
plt.savefig('plot/mean_wo_muon_subtraction.pdf')
plt.show()

ax.plot(mean_wo['day'], mean_wo['mean'], label= 'mean w/o muons')
ax.plot(mean_w['day'], mean_w['mean'], label= 'mean w muons')
ax.legend(loc='best')
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m\n%Y'))
ax.savefig('plot/mean_compared.pdf')


plt.plot(std_w['day'], std_w['std'], label= 'std w muons')
plt.grid(True)
plt.ylabel('Std')
plt.legend(loc='best')
std_w=plt.gca()
std_w.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m\n%Y'))
plt.savefig('plot/std_wo_muon_subtraction.pdf')
plt.show()

plt.plot(std_wo['day'], std_wo['std'], label= 'std w/o muon')
plt.grid(True)
plt.ylabel('Std')
plt.legend(loc='best')
std_wo=plt.gca()
std_wo.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m\n%Y'))
plt.savefig('plot/std_w_muon_subtraction.pdf')
plt.show()

ax1.plot(std_wo['day'], std_wo['std'], label= 'std w/o muon')
ax1.plot(std_w['day'], std_w['std'], label= 'std w muons')
ax1.legend(loc='best')
ax1.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m\n%Y'))
ax1.savefig('plot/mean_compared.pdf')

print "It took " + datetime.timedelta(datetime.datetime.now() - start_time) + " seconds to execute this"  
