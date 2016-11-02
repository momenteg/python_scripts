#!/usr/bin/python

import os
import argparse
import glob


parser = argparse.ArgumentParser()
parser.add_argument("-d","--dag-file",type=str, help="Filename.dag",required=True,dest="dagfile")
parser.add_argument("-f","--submit-file",type=str, help="-file *.submit",required=False,dest="sub_file", default="muon_subtractor.submit")
parser.add_argument("-y","--year",type=str, help="year to process",required=True,dest="year")
args = parser.parse_args()

path_binned_file = "/home/gmomente/data/binned/{0}/".format(args.year) #run_117798_0_binned.root

string = ""

os.system("mkdir ~/data/subtracted/{0}".format(args.year))

filename_binned =  glob.glob(path_binned_file+"*.root")
for filename in filename_binned:
    run_number=os.path.basename(filename).split("run_")[1].split("_binned")[0] 
    jobName = "muon_subtractor_calc"
    string += "JOB {0}.{1} {2}\n".format(jobName, run_number, args.sub_file)
    string += "VARS {0}.{1} binned_data=\"{2}\" run_number=\"{3}\" year=\"{4}\" \n".format(jobName,run_number, filename, run_number, args.year)

string += "CONFIG dagman.config\nNODE_STATUS_FILE "+os.path.basename(args.dagfile)+".nodestatus 30\n"

f = open(args.dagfile,"w")
f.write(string)
f.close()




