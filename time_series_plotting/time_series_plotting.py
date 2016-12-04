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

#data_files=['2008_2011.h5','2012.h5','2013.h5','2014.h5','2015.h5', '2016.h5'] 
data_files=['2012.h5','2013.h5'] 
path= '/localscratch/gmoment/subtracted_muons_data/h5_files/'


for data_file in data_files:
	print data_file
	df = pd.read_hdf(path + data_file)
	grouped = df.groupby('day')
	#muon_number = pd.concat([muon_number, grouped['muon_number'].agg([np.mean])])
	mean_wo = pd.concat([mean_wo,grouped['Significance_without_muons'].agg([np.mean])])
	mean_w = pd.concat([mean_w, grouped['Significance_with_muons'].agg([np.mean])])
	std_w = pd.concat([std_w, grouped['Significance_with_muons'].agg([np.std])])
	std_wo = pd.concat([std_wo, grouped['Significance_without_muons'].agg([np.std])])
	print mean_wo.info()
	print mean_w.info()
	del df, grouped 
	gc.collect()

std_wo=std_wo.reset_index()
std_w=std_w.reset_index()
mean_wo=mean_wo.reset_index()
mean_w=mean_w.reset_index()
print "done"

#setting the field day as date
std_wo['day']= pd.to_datetime(std_wo['day'], format='%Y-%m-%d')
std_w['day']= pd.to_datetime(std_w['day'], format='%Y-%m-%d')
mean_w['day']= pd.to_datetime(mean_w['day'], format='%Y-%m-%d')
mean_wo['day']= pd.to_datetime(mean_w['day'], format='%Y-%m-%d')


fig_mean = plt.figure()
ax= fig_mean.add_subplot(1,1,1)

fig_std = plt.figure()
ax1= fig_std.add_subplot(1,1,1)


ax.plot(mean_wo['day'], mean_wo['mean'], label= 'mean w/o muons')
ax.plot(mean_w['day'], mean_w['mean'], label= 'mean w muons')
ax.legend(loc='best')
fig_mean.autofmt_xdate()
#ax.set_major_formatter(matplotlib.dates.DateFormatter('%m\n%Y'))
fig_mean.savefig('plot/mean_compared.pdf')

ax1.plot(std_wo['day'], std_wo['std'], label= 'std w/o muon')
ax1.plot(std_w['day'], std_w['std'], label= 'std w muons')
ax1.legend(loc='best')
fig_std.autofmt_xdate()
#ax1.set_major_formatter(matplotlib.dates.DateFormatter('%m\n%Y'))
fig_std.savefig('plot/std_compared.pdf')

# plt.plot(muon_number['day'], muon_number['mean'], 'go' label= 'muon number')
# plt.grid(True)
# plt.ylabel('# muons')
# plt.legend(loc='best')
# muon_plt=plt.gca()
# muon_plt.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m\n%Y'))
# plt.savefig('plot/muon_number.jpg')
# plt.show()

print "It took " + str(datetime.datetime.now() - start_time) + " seconds to execute this"  
