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

    ###### get the series #####################
    Bax_int_rel = df["Bax Intensities"]
    Bak_int_rel = df["Bak Intensities"]
    ################################################################################################################

    #### plot the whole story with pandas/matplotlib ###########################################################################
    my_x_ticks = df["µm"] #sometimes it adds this weird charcater: then use df["Âµm"]
    plt.figure(figsize=(12, 8))

    plt.plot(my_x_ticks, Bax_int_rel, label='BAX', color='#0EB30E')
    plt.plot(my_x_ticks, Bak_int_rel, label='BAK', color='#D10FD1')

    plt.xticks(my_x_ticks) #df["nm"]
    plt.locator_params(axis='x', nbins=10)

    # plt.title('Example line profile', y=0.9, fontsize=24)  # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    plt.xticks(fontsize=28, rotation=45)
    plt.yticks(fontsize=28)

    # sets params for the ticks themselves, not the labels
    plt.tick_params(direction='inout', length=6, width=2, colors='k') #, grid_color='r', grid_alpha=0.5) #direction : {'in', 'out', 'inout'}: Puts ticks inside the axes, outside the axes, or both.

    plt.xlabel('length [µm]', fontsize=32)
    plt.ylabel('normalized fluorescence intensity [a.u.]', fontsize=32)
    # plt.legend(fontsize=28, title_fontsize=24, loc="upper right")
    plt.tight_layout()

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