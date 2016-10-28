#! /usr/bin/python
## Author: Giulio Momente'
## emails: momenteg@gmail.com / gmomente@icecube.wisc.edu


import ROOT
import numpy as np
from root_numpy import root2array, tree2array
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import glob
import sys
import datetime
from progress.bar import Bar
import time
from scipy.optimize import curve_fit
from scipy.stats import norm
import math
import pandas as pd

good_run_minimum_length= 14400	#four hours
good_fit_low = 1e-4
good_fit_upp = 1
path= '/localscratch/gmoment/subtracted_muons_data/root_files/2012/'
hdf = pd.HDFStore('2012.h5')


bar = Bar('Processing', max=len(glob.glob(path + '*.root')))

for filename in glob.glob(path + '*.root'):
	#print filename + "\n"
	rfile = ROOT.TFile(filename)
	outtree = rfile.Get('outtree')
	tree = rfile.Get('tree')
	data_tree = tree2array(tree)
	data_outtree = tree2array(outtree)

	try:
		if ( data_tree['bin_time'].max() -  data_tree['bin_time'].min() ) < good_run_minimum_length : #run shorter than 4 hours!
			bar.next()
			continue
		if (data_outtree['SignificanceSlope'] <  good_fit_low or data_outtree['SignificanceSlope'] > good_fit_upp):
			bar.next()
			continue
	except ValueError:
		bar.next()
		continue

	outtree = rfile.Get('outtree')
	summary_tree= tree2array(outtree)

	begin_of_year=datetime.datetime(year=int(summary_tree['year'].mean()), month=1, day=1)
	day= begin_of_year + datetime.timedelta(seconds=data_tree['bin_time'].mean())
	d= {'day' : day.strftime('%Y-%m-%d'),'Significance_without_muons': data_tree['signi_bin'],'Significance_with_muons': data_tree['signi_bin_before']}
	df = pd.DataFrame(d)
	hdf.put('Timeseries', df, format='table', data_columns=True, append = True)
	bar.next()
bar.finish()

#df.index = df['day']
#del df['day']


hdf.close()
