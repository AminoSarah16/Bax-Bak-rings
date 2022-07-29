'''
This program opens a csv files.
Then plots the line profile with matplotlib
Göttingen, March 2022, Sarah Vanessa Schweighofer, MPI-NAT
'''

import os
from tkinter import filedialog
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np



def main():
    df = df_from_csv()
    print(df)

    ###### calculate mean intensity of the line profile and normalize every value to this mean #####################
    Bax_mean = df["Bax Intensities"].mean()  # in order to calculate the mean of each colum
    Bak_mean = df["Bak Intensities"].mean()

    Bax_int_rel = df["Bax Intensities"] / Bax_mean
    Bak_int_rel = df["Bak Intensities"] / Bak_mean
    ################################################################################################################

    #### plot the whole story with pandas/matplotlib ###########################################################################
    my_x_ticks = df["µm"]
    plt.figure(figsize=(11.7, 8.27))
    plt.plot(my_x_ticks, Bax_int_rel, label='Bax', color='#0EB30E')
    plt.plot(my_x_ticks, Bak_int_rel, label='Bak', color='#D10FD1')

    plt.xticks(my_x_ticks) #df["nm"]
    plt.locator_params(axis='x', nbins=10)

    # TODO: set size of the tickmark labels with matplotlib
    # plt.set_xticklabels(plot.get_xticks(), size=16)
    #     # plot.set_yticklabels(plot.get_yticks(), size=16)

    plt.title('Example line profile', y=0.9, fontsize=24)  # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel('length [µm]', fontsize=24)
    plt.ylabel('normalized fluorescence intensity [a.u.]', fontsize=24)
    plt.legend(fontsize=16, title_fontsize=24, loc="lower right")

    plt.show()
    ##############################################################################################################


###### basic pandas funcionality to read a csv and make a dataframe out of it. file location is being asked via tkinter
def df_from_csv():
    file = filedialog.askopenfile()
    df = pd.read_csv(file)  # better already sort the csv manually before importing
    return df
#####################################################################################################################

if __name__ == '__main__':
    main()