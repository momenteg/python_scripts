#!/usr/bin/python

import pandas as pd
import numpy as np
import glob
import matplotlib
import matplotlib.pyplot as plt
import seaborn
import os
import re

def mount_mogon():
    print("mounting mogon via sshfs")
    string_ = "sshfs -o nonempty dummy_user@dummy_address:/etapfs02/icecubehpc/gmoment/output_hidden_supernova/ mount_mogon/ "
    os.system(string_)

def read_data(dummy_var):
    print("reading data from: ", dummy_var  )
    list_ = glob.glob(dummy_var)
    print("number of files: ", len(list_))
    return list_

def filling_df_with_types(a, b, c):
    list_dummy=[]
    regex=re.compile(".*("+a+").*.("+b+").*")
    list_dummy=[m.group(0) for l in c for m in [regex.search(l)] if m]
    #print(len(list_dummy))
    d = (pd.read_table(file_, names=["distance","signi"], sep = " ") for file_ in list_dummy);
    dummy_df = pd.concat(d, ignore_index=True)
    dummy_df["type"] = a
    dummy_df["bin"] = b
    return dummy_df


def plotting_with_types(signi_vs_distance_debug,a):
    print(a)
    plt.plot(signi_vs_distance_debug[(signi_vs_distance_debug.type=="HI")].distance, signi_vs_distance_debug[(signi_vs_distance_debug.type=="HI")].signi, "r.", label="HI - {}".format(a), alpha=0.5)
    plt.plot(signi_vs_distance_debug[(signi_vs_distance_debug.type=="HN")].distance, signi_vs_distance_debug[(signi_vs_distance_debug.type=="HN")].signi, "g.", label="HN - {}".format(a), alpha =0.5)
    plt.title("LL distribution Signi vs Distance (2012-10) - binning: {}".format(a))
    plt.legend()
    plt.yscale('log')
    plt.xlabel('Distance [Kpc]')
    plt.ylabel('Significance')
    plt.savefig('plots/signi_vs_dist_bin_{}.png'.format(a))
    plt.clf()

def main():
    # Get current size
    fig_size = plt.rcParams["figure.figsize"]

    # Set figure width to 15 and height to 10
    fig_size[0] = 15
    fig_size[1] = 10
    plt.rcParams["figure.figsize"] = fig_size

    mount_mogon()
    list_signi_vs_distance_LL=[]
    LL_debug= "mount_mogon/2010/debug/*LL*star_distr_0*"
    neutr_types=["HI","HN"]
    binnings = ["500ms","1.0s", "1.5s", "4s", "10s","all"]
    signi_vs_distance_debug = pd.DataFrame()

    list_signi_vs_distance_LL = read_data(LL_debug)

    for types in neutr_types:
        for binning in binnings:
            signi_vs_distance_debug=signi_vs_distance_debug.append(filling_df_with_types(types, binning, list_signi_vs_distance_LL))

    print("start plotting")

    for bin_size in ["500ms","1.0s", "1.5s", "4s", "10s"]:
        plotting_with_types(signi_vs_distance_debug[(signi_vs_distance_debug.bin==bin_size)],bin_size)



    print("Done")

if __name__ == "__main__":
    main()
