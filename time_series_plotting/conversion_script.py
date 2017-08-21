#! /usr/bin/python
## Author: Giulio Momente'
## emails: momenteg@gmail.com / gmomente@icecube.wisc.edu

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import numpy as np
from root_numpy import root2array, tree2array
import glob
import sys
import datetime
from progress.bar import Bar
import time
import pandas as pd
import json
import shutil
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-year",  type=str,
                    help="year", required=True, dest="year")
parser.add_argument("-good_list_used",  type=bool,
                    help="good_list_used: use good run list (True/False)", required=False, default=True, dest="good_list_used")
args = parser.parse_args()


good_run_minimum_length= 28000 #8 hours == 28800 # 14400 == four hours #21500 == 6 hour.
path= '/localscratch/gmoment/subtracted_muons_data/root_files/{0}_cut_zenith/'.format(args.year)
json_file='good_run_list/good_list_{0}'.format(args.year)
name_output = '{0}_cut_zenith'.format(args.year)
dest = '/localscratch/gmoment/subtracted_muons_data/h5_files/'

hdf = pd.HDFStore(name_output+'.h5')
df=pd.DataFrame()
good_run_list=[]
low_cut_signi=-10

def good_runs_parse_from_json():
    json_data=open(json_file+'.json')
    goodruns = json.load(json_data)
    for runs in goodruns['runs']:
        if runs['good_i3']==True and runs['good_it']==True:
            good_run_list.append(runs['run'])

    return good_run_list

print(hdf)
filenames= glob.glob(path+'*.root')
filenames.sort()

bar = Bar('Processing', max=len(filenames))
good_run_list = good_runs_parse_from_json()

for filename in filenames:
    rfile = ROOT.TFile(filename)
    outtree = rfile.Get('outtree')
    tree = rfile.Get('tree')
    data_tree = tree2array(tree)
    data_outtree = tree2array(outtree)

    try:
        condition=np.where(args.good_list_used 
                ,(( data_tree['bin_time'].max() -  data_tree['bin_time'].min() ) > good_run_minimum_length and data_outtree['run_number'] in good_run_list )
                ,(( data_tree['bin_time'].max() -  data_tree['bin_time'].min() ) > good_run_minimum_length))
	if(condition):
	    begin_of_year=datetime.datetime(year=int(data_outtree['year'].mean()), month=1, day=1)
            day= begin_of_year + datetime.timedelta(seconds=data_tree['bin_time'].mean())
            index_signi_edge= np.where( np.logical_not( data_tree["signi_bin"]<=low_cut_signi) )#cutting the lower limit of significance
            d= {'day' : day.strftime('%Y-%m-%d'),
                'Significance_without_muons': data_tree['signi_bin'][index_signi_edge],
                'Significance_with_muons': data_tree['signi_bin_before'][index_signi_edge],
                'muon_number': data_tree['dst_chan_bin'][index_signi_edge].mean()
                }
            #df = pd.concat([df,pd.DataFrame(d)])
            df = pd.DataFrame(d)
            hdf.put('Timeseries', df, format='table', data_columns=True, append = True)
            bar.next()
            continue
        else:
            bar.next()
    except ValueError:
        bar.next()
        continue
    
#hdf.put('Timeseries', df, format='table', data_columns=True, append = True)
bar.finish()

infos={"minimum_lenght_run" : [good_run_minimum_length], 
        "good_list_used":args.good_list_used,
        'low_cut_signi':low_cut_signi}

pd_infos=pd.DataFrame(infos)
hdf.put('infos', pd_infos,format='table', data_columns=True, append = True)

hdf.close()

os.system('mv {0}.h5 {1}{2}.h5'.format(name_output,dest,name_output))
