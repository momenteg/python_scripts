#!/usr/bin/python
import progressbar
import os
import argparse
import glob
#import progressbar
#from progressbar import ProgressBar

parser = argparse.ArgumentParser()
parser.add_argument("-d","--dag-file",type=str, help="Filename.dag",required=True,dest="dagfile")
parser.add_argument("-f","--submit-file",type=str, help="-file *.submit",required=False,dest="sub_file", default="muon_binner.submit")
parser.add_argument("-y","--year",type=str, help="year to process",required=True,dest="year")
args = parser.parse_args()

path_sndata_file = "/data/exp/IceCube/"+args.year+"/internal-system/sndaq/*/" #sndata_117293_0.tar.gz
path_dst_file = "/data/exp/IceCube/"+args.year+"/filtered/DST_IC79/*/" #PFFilt_PhysicsTrig_PhysicsFiltering_Run00118090_Subrun00000000_00000065.root

string = ""

os.system("mkdir ~/data/binned/{0}".format(args.year))

filename_sndaq =  glob.glob(path_sndata_file+"*.tar.gz")
pbar = progressbar.ProgressBar()
for filename in pbar(filename_sndaq):
    name= os.path.basename(filename)
    run_number = name.split(".tar")[0].split("sndata_")[1]
    filename_dst =  glob.glob(path_dst_file+'*' +run_number.split("_")[0] + '_*.root')
    jobName = "muon_binner_calc"
    try:
        dst_file= filename_dst[0].split("_Subrun")[0] +'*.root'
    except:
        continue
    string += "JOB {0}.{1} {2}\n".format(jobName, run_number, args.sub_file)
    string += "VARS {0}.{1} sndata=\"{2}\" run_number=\"{3}\" dst=\"{4}\" year=\"{5}\" \n".format(jobName, run_number, filename, run_number, dst_file, args.year)

string += "CONFIG dagman.config\nNODE_STATUS_FILE "+os.path.basename(args.dagfile)+".nodestatus 30\n"

f = open(args.dagfile,"w")
f.write(string)
f.close()




