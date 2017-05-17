#!/usr/bin/python

import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import seaborn
import subprocess
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

def filling_df_debug(a):
    dataframe = pd.DataFrame()
    df_from_each_file = (pd.read_table(file_, names=["distance","signi"], sep = " ") for file_ in a)
    dataframe = pd.concat(df_from_each_file, ignore_index=True)
    return dataframe

def filling_df_signal(a):
    dataframe = pd.DataFrame()
    dummy_df = pd.DataFrame()
    b = (pd.read_table(file_, names=["first_row"], nrows=1, sep = " ") for file_ in a)
    dummy_df = pd.concat(b, ignore_index=True)
    df_from_each_file = (pd.read_table(file_, names=["signi", "multi"], skiprows=1, sep = " ") for file_ in a)
    dataframe = pd.concat(df_from_each_file, ignore_index=True)
    print("unique of the first rows: ", dummy_df.first_row.unique())
    return dataframe

def plot_signi_vs_distance(signi_vs_dist_LL,signi_vs_dist_BH):
    fig_signi_vs_distance = plt.figure(figsize=(15,10))
    ax= fig_signi_vs_distance.add_subplot(1,1,1)
    ax.plot(signi_vs_dist_LL.distance, signi_vs_dist_LL.signi, 'g.', label="LL 2012/0 NH + IH binning=all", alpha=0.5)
    ax.plot(signi_vs_dist_BH.distance, signi_vs_dist_BH.signi, 'b.', label="BH 2011/2 NH + IH binning=all", alpha=0.5)
    ax.set_title("LL+BH Distribution Signi vs Distance (2012-10) NH+IH - star distribution uniform")
    ax.legend()
    ax.set_yscale('log')
    ax.set_xlabel('Distance [Kpc]')
    ax.set_ylabel('Significance')
    fig_signi_vs_distance.savefig('plots/signi_vs_dist_LL+BH.png')

def plot_significance(signal_LL, signal_BH):
    norm_factor= 0.01
    fig_signi = plt.figure(figsize=(15,10))
    ax1= fig_signi.add_subplot(1,1,1)
    ax1.hist(norm_factor*signal_LL[(norm_factor*signal_LL.signi) < 200].signi.values, bins =100, color="g", alpha=0.5, label="signi*{} LL".format(norm_factor));
    ax1.hist(norm_factor*signal_BH[(norm_factor*signal_BH.signi) < 200].signi.values, bins =100, color="b", alpha=0.5, label="signi*{} BH".format(norm_factor));
    ax1.set_yscale('log')
    ax1.set_xlim(-10,200)
    ax1.set_title("Distribution significance signal 2012-10 - star distribution uniform ")
    ax1.set_xlabel('Significance')
    ax1.legend(loc=2)
    fig_signi.savefig('plots/significance.png')

def main():
    list_signi_vs_distance_LL=[]
    list_signi_vs_distance_BH = []
    list_signal_LL = []
    list_signal_BH = []
    neutr_types=["HI","HN"]
    binnings = ["500ms","1.0s", "1.5s", "4s", "10s","all"]

    LL_signal= "mount_mogon/201*/signals/*LL*star_distr_0*"
    LL_debug= "mount_mogon/201*/debug/*LL*star_distr_0*"
    BH_signal= "mount_mogon/201*/signals/*BH*star_distr_0*"
    BH_debug= "mount_mogon/201*/debug/*BH*star_distr_0*"

    signi_vs_dist_LL = pd.DataFrame()
    signal_LL = pd.DataFrame()
    signi_vs_dist_BH = pd.DataFrame()
    signal_BH = pd.DataFrame()
    signi_vs_distance_debug = pd.DataFrame()

    mount_mogon()

    list_signi_vs_distance_LL = read_data(LL_debug)
    list_signal_LL = read_data(LL_signal)
    list_signi_vs_distance_BH = read_data(BH_debug)
    list_signal_BH = read_data(BH_signal)

    print("populating dataframes")
    signi_vs_dist_LL = filling_df_debug(list_signi_vs_distance_LL)
    signal_LL = filling_df_signal(list_signal_LL)
    signi_vs_dist_BH = filling_df_debug(list_signi_vs_distance_BH)
    signal_BH = filling_df_signal(list_signal_BH)
    print(len(signi_vs_dist_LL.index))

    print("start plotting")
    plot_signi_vs_distance(signi_vs_dist_LL,signi_vs_dist_BH)
    plot_significance(signal_LL,signal_BH)
    print("Done.")


if __name__ == "__main__":
    main()
