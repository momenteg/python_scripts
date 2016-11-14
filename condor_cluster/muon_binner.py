#!/usr/bin/python

import os, sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-sndata",  type=str,
                    help="sndata tar file with path", required=True, dest="sndata")
parser.add_argument("-run_number",  type=str,
                    help="run number (for the output file and )", required=True, dest="run_number")
parser.add_argument("-dst",  type=str,
                    help="dst CHAIN files with path", required=True, dest="dst")
parser.add_argument("-year",  type=str,
                    help="year", required=True, dest="year")
args = parser.parse_args()

output_path="/data/user/gmomente/binned/{0}".format(args.year)
scriptname='muon_binner_'+args.run_number+'.sh'

f = open(scriptname, 'w')


f.write("eval `/cvmfs/icecube.opensciencegrid.org/py2-v1/setup.sh`;\n")
f.write("export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/afritz/sndaq/afritz/trunk/install/lib/;\n")
f.write("mkdir $_CONDOR_SCRATCH_DIR/"+args.year+"/;\n")
f.write("tar -zxf " + args.sndata + " -C $_CONDOR_SCRATCH_DIR/"+args.year+"/;\n")
f.write("cd /home/afritz/sndaq/afritz/trunk/install;\n")
#f.write("echo $LD_LIBRARY_PATH;\n" )
f.write("./bin/sni3_muon_binner_for_monitoring --cut-zenith --output-file "+output_path+"/run_" + args.run_number + "_binned.root --dst-file-list " + args.dst + " --end $_CONDOR_SCRATCH_DIR/"+ args.year+"/"+os.path.basename(args.sndata).split(".tar")[0]  +"*.root;\n")
#f.write("cd ~/;\n")
#f.write("pwd;\n")
#f.write("rm -r ~/*"+args.run_number+"*.root ~/*.xml;\n")
f.close()
os.system('chmod +x '+scriptname)
os.system('./'+scriptname)
