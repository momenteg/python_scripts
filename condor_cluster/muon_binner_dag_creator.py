#!/usr/bin/python
import progressbar
import os
import argparse
import glob
import commands
import re
import numpy as np
import datetime
#import progressbar
#from progressbar import ProgressBar

start_time=datetime.datetime.now() #taking current time as starting time


parser = argparse.ArgumentParser()
parser.add_argument("-d","--dag-file",type=str, help="Filename.dag",required=True,dest="dagfile")
parser.add_argument("-f","--submit-file",type=str, help="-file *.submit",required=False,dest="sub_file", default="muon_binner.submit")
parser.add_argument("-y","--year",type=str, help="year to process",required=True,dest="year")
args = parser.parse_args()

path_sndata_file = {"2011":"/data/exp/IceCube/2011/internal-system/sndaq/*/", 
"2012":"/data/exp/IceCube/2012/internal-system/sndaq/*/", 
"2013":"/data/exp/IceCube/2013/internal-system/sndaq/*/", 
"2014":"/data/exp/IceCube/2014/internal-system/sndaq/*/", 
"2015":"/data/exp/IceCube/2015/internal-system/sndaq/*/",
"2016":"/data/exp/IceCube/2016/internal-system/sndaq/*/"} 
#path_dst_file = "/data/exp/IceCube/2012/filtered/DST_IC86/2011/*/" #data 2011, not good really, maybe there is better data somewhere else
#path_dst_file = "/data/exp/IceCube/"+args.year+"/filtered/DST_IC79/*/" #PFFilt_PhysicsTrig_PhysicsFiltering_Run00118090_Subrun00000000_00000065.root
path_dst_file={"2011":"/data/exp/IceCube/2012/filtered/DST_IC86/2011/*/",
"2012":"/data/exp/IceCube/2012/filtered/DST_IC86/2012/*/", #be carefull this path is for Jan 2012 - apr 2012
#"2012":"/data/exp/IceCube/2012/filtered/level2/*/", #be carefull this path is for may 2012 - dec 2012
"2013":"/data/exp/IceCube/2013/filtered/level2/",
"2014":"/data/exp/IceCube/2014/filtered/level2/*/",
"2015":"/data/exp/IceCube/2015/filtered/level2/*/",
"2016":"/data/exp/IceCube/2016/filtered/level2/*/"}
string = ""
if args.year == "2012":
	print("ATTENTION read comment inside this script")

f = open(args.dagfile,"w")
os.system("mkdir /data/user/gmomente/binned/{0}".format(args.year))
filename_sndaq =  glob.glob(path_sndata_file[args.year]+"*.tar.gz")
pbar = progressbar.ProgressBar()
filename_sndaq.sort()
filename_sndaq=list(set(filename_sndaq))
for filename in pbar(filename_sndaq):
    name= os.path.basename(filename)
    run_number = name.split(".tar")[0].split("sndata_")[1]
    filename_dst = commands.getstatusoutput("find "+ path_dst_file[args.year]+" -name '*"+ run_number.split("_")[0]+"*.root'")
    filename_dst=re.split('\n', filename_dst[1])[0]
    jobName = "muon_binner_calc"
    if filename_dst:
        dst_file= filename_dst.split(run_number.split("_")[0])#+run_number.split("_")[0] +'*.root'
        dst_file=np.where(len(dst_file) == 3, dst_file[0]+run_number.split("_")[0]+dst_file[1]+run_number.split("_")[0] +'*.root', dst_file[0]+run_number.split("_")[0] +'*.root') 
    else:
        continue
    string += "JOB {0}.{1} {2}\n".format(jobName, run_number, args.sub_file)
    string += "VARS {0}.{1} sndata=\"{2}\" run_number=\"{3}\" dst=\"{4}\" year=\"{5}\" \n".format(jobName, run_number, filename, run_number, dst_file, args.year)
    f.write(string)
    string = ""

string += "CONFIG dagman.config\nNODE_STATUS_FILE "+os.path.basename(args.dagfile)+".nodestatus 30\n"

#f = open(args.dagfile,"w")
f.write(string)
f.close()

print "It took " + str(datetime.datetime.now() - start_time) + " seconds to execute this"  



