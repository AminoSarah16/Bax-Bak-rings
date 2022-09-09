'''
NORMALIZATION SCRIPT 2
This program opens line plot raw csv files.
Then calculates the relative Bax or Bak values by using the min-max-value csv created with Bax-Bak-min-max_over-replicate.py.
Then saves a new csv of these relative values.
From this it then plots the line profile with matplotlib and saves it as png.
User needs to just run the script, everything is asked for.
Göttingen, August 2022, Sarah Vanessa Schweighofer, MPI-NAT
'''

import os
from tkinter import filedialog
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np



def main():
    # let the user choose the folder containing the tables
    root_path = filedialog.askdirectory()  # prompts user to choose directory. From tkinter

    ###### open the csv with all the min and max values from this repliccate, created with "Bax-Bak-min-max_over-replicate.py"
    result_path = os.path.join(root_path, 'results')
    file_path = os.path.join(result_path, "mins_maxes.csv")
    min_max = pd.read_csv(file_path, encoding='latin1')  # better already sort the csv manually before importing

    ###### calculate min and max intensity of all the rings in this replicate #####################
    Bax_min = min_max["Bax min"].min()  # in order to calculate the min of the Bax values
    Bak_min = min_max["Bak min"].min()  # in order to calculate the min of the Bax values
    Bax_max = min_max["Bax max"].max()
    Bak_max = min_max["Bak max"].max()

    # prints out the number of files in the selected folder with the wanted file format and adds them to a list
    file_format = ".csv"
    filenames = [filename for filename in sorted(os.listdir(root_path)) if filename.startswith(("Plot_"))]
    print("There are {} files with this format.".format(len(filenames)))
    if not filenames:  # pythonic for if a list is empty
        print("There are no files with this format.")
    for filename in filenames:
        print(filename)
        file_path = os.path.join(root_path, filename)
        df = pd.read_csv(file_path, encoding='latin1')  # latin1 encocing needed in order to be able to read special chars like "µ"
        print(df)

        ########## normalize the raw values to the overall brightness of this channel in this raplicate #######
        Bax_norm = (df["Bax Intensities"] - Bax_min) / (Bax_max - Bax_min)
        Bak_norm = (df["Bak Intensities"] - Bak_min) / (Bak_max - Bak_min)

        ##### create a new csv with these normalized values ######
        df2 = pd.concat([df["µm"], Bax_norm, Bak_norm], axis=1)
        print(df2)

        new_filename = filename[12:-4]
        print(new_filename)
        output_file = os.path.join(result_path, new_filename + "_normalized-by-rings-replicate.csv")
        print(output_file)
        df2.to_csv(output_file)
        ################################################################################################################

        #### plot the whole story with pandas/matplotlib ###########################################################################
        my_x_ticks = df["µm"]
        plt.figure(figsize=(11.7, 8.27))
        plt.plot(my_x_ticks, Bax_norm, label='Bax', color='#0EB30E')
        plt.plot(my_x_ticks, Bak_norm, label='Bak', color='#D10FD1')

        plt.xticks(my_x_ticks) #df["nm"]
        plt.locator_params(axis='x', nbins=10)

        # TODO: set size of the tickmark labels with matplotlib
        # plt.set_xticklabels(plot.get_xticks(), size=16)
        #     # plot.set_yticklabels(plot.get_yticks(), size=16)

        plt.title(filename, y=0.9, fontsize=24)  # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.xlabel('length [µm]', fontsize=24)
        plt.ylabel('normalized fluorescence intensity [a.u.]', fontsize=24)
        plt.legend(fontsize=16, title_fontsize=24, loc="lower right")

        new_filename = filename[12:-4]
        output_file = os.path.join(result_path, new_filename + "line-plot_normalized-to-repl-rings.png")
        plt.savefig(output_file)

        ## plt.show() #needs to come after savefig, otherwise saved plot will be blank...
        ##############################################################################################################


if __name__ == '__main__':
    main()