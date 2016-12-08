#!/usr/bin/python

import os, sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-binned_data",  type=str,
                    help="sndata binned data", required=True, dest="binned_data")
parser.add_argument("-run_number",  type=str,
                    help="run number (for the output file and )", required=True, dest="run_number")
parser.add_argument("-year",  type=str,
                    help="year", required=True, dest="year")
args = parser.parse_args()

leap_second_runs = {"2015":"126553"}
elapsed=""
th_run_number= leap_second_runs.get(args.year)

if th_run_number is not None and int(args.run_number.split("_")[0]) > int(th_run_number):
	 elapsed=" --elapsed-second+ "



scriptname='muon_subtractor_'+args.run_number+'.sh'

f = open(scriptname, 'w')


f.write("eval `/cvmfs/icecube.opensciencegrid.org/py2-v1/setup.sh`;\n")
f.write("export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/afritz/sndaq/afritz/trunk/install/lib/;\n")
f.write("cd /home/afritz/sndaq/afritz/trunk/install;\n")

f.write("touch ~/data/subtracted/"+ args.year+"/run_" + args.run_number + "_subtracted.root;\n")
f.write("./bin/sni3_muon_subtractor_updated " + elapsed + " -output  /data/user/gmomente/subtracted/"+ args.year+"/run_" + args.run_number + "_subtracted.root " + args.binned_data + " ;\n")
f.write("cd ~/;\n")
#f.write("pwd;\n")
#f.write("rm -r ~/*"+args.run_number+"*.root ~/*.xml;\n")
f.close()
os.system('chmod +x '+scriptname)
os.system('./'+scriptname)

