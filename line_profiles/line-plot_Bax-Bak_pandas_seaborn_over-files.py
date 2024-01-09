'''
This program opens a csv files.
Then calculates the relative Bax or Bak values and saves a new csv.
From this it then plots the line profile with matplotlib and saves it as png.
User needs to just run the script, everything is asked for.
Göttingen, March 2022, Sarah Vanessa Schweighofer, MPI-NAT
MIT License

Copyright (c) 2022, Sarah Vanessa Schweighofer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
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

        ###### calculate mean intensity of the line profile and normalize every value to this mean and save the new df #####################
        Bax_mean = df["Bax Intensities"].mean()  # in order to calculate the mean of each colum
        Bak_mean = df["Bak Intensities"].mean()

        Bax_int_rel = df["Bax Intensities"] / Bax_mean
        Bak_int_rel = df["Bak Intensities"] / Bak_mean

        df2 = pd.concat([df["µm"], Bax_int_rel, Bak_int_rel], axis=1)
        print(df2)

        df2.to_csv(file_path + "_normalized.csv")
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

        plt.title(filename, y=0.9, fontsize=24)  # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.xlabel('length [µm]', fontsize=24)
        plt.ylabel('normalized fluorescence intensity [a.u.]', fontsize=24)
        plt.legend(fontsize=16, title_fontsize=24, loc="lower right")

        plt.savefig(file_path + "_line-plot.png")
        # plt.show() #needs to come after savefig, otherwise saved plot will be blank...
        ##############################################################################################################


if __name__ == '__main__':
    main()