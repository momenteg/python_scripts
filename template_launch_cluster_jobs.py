#!/usr/bin/python
# -*- coding: utf-8 -*-
#HPC platform: LSF 

import os, sys
import glob
import datetime
import random
import time

py2v1 = '/cvmfs/icecube.opensciencegrid.org/py2-v1/setup.sh;\n'
LD_LIBRARY_PATH = 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/etapfs02/icecubehpc/amauser/sndaq/sndaq_trunk/install/lib/;\n'
cd = 'cd /etapfs02/icecubehpc/amauser/sndaq/sndaq_trunk/install;\n'
execute = './bin/sni3_muon_subtractor'
year='2013'      
path_data_file= '/etapfs02/icecubehpc/amauser/data/sndaq_data_rebinned/'+year+'/'
subtracted_data = '/etapfs02/icecubehpc/amauser/data/subtracted_data/' #copy of the data can be found in /tati/data/icecube/sndaq_data_rebinned_2013_2016
job_ram    = 'Reserve2G' # $bapp -- shows assortment 
job_time   = '5:00' #  hh:mm
job_type   = 'etapshort'  #  long/short


scriptname = 'conversion_' +year+'.sh'

f = open(scriptname, 'w')
f.write('#!/bin/bash\n') 
f.write(py2v1)
f.write(LD_LIBRARY_PATH)
f.write(cd)
f.write('mkdir ' + subtracted_data + year + ';\n')

subtracted_data=subtracted_data + year +'/'


filename =  glob.glob(path_data_file+'*.root')
num_files=len(filename)

for i in range(0,num_files):
	name= os.path.basename(filename[i])
	f.write('touch ' + subtracted_data + 'subtracted_' + str(name) + ';\n' )
	f.write(execute + ' -ic79-muon-cut  -output ' + subtracted_data + 'subtracted_' + str(name) + ' ' + filename[i] +';\n')


f.close()
os.system('chmod +x '+scriptname)
os.system('bsub -q ' + job_type + ' -app ' + job_ram + ' -W ' + job_time + ' -o ' + scriptname + '.o  -e '+scriptname + '.e    ./'+scriptname) 
#os.system('bsub -q ' + job_type + ' -app ' + job_ram + ' -W ' + job_time + ' ./'+scriptname) 


