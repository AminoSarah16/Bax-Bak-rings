'''
This program let's the user choose a csv files.
Then plots percent Bax vs Pearson.
Göttingen, August 2022, Sarah Vanessa Schweighofer, MPI-NAT
'''

import os
from tkinter import filedialog
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob2
import numpy as np


def main():
    file = filedialog.askopenfile() #open ‪P:\Private\practice\quantification_of_imaging_experiments\manual_ring_quantification_all-rings\results_all.csv
    print(file)

    df = pd.read_csv(file, encoding='latin1')  # latin1 encocing needed in order to be able to read special chars like "µ"
    print(df)

    length = df['Length']
    print(length)

    Bak_percent = df['Percent Bak']
    Bax_percent = df['Percent Bax']

    #############################calculate running median##################################
    length_slices = []
    length_slice_indices = []
    rollmedians = []
    rollmed_lengths = []
    # take windows of 400 nm
    window_size = 0.4

    #create starting value
    x = 0.4

    #schleife mit stepsize
    while x < 3.9: #3.9 is biggest ring found in the data
        #find all the values in a certain window of the series (= a slice)
        length_slice = length[(length >= x) & (length < (x+window_size))].sort_values() #find all the values between x and (x plus stepsize) and sort the list ascending
        print(x)
        print(length_slice)
        length_slices.append(length_slice)

        # find the index values of the values in the slice
        length_slice_index = length_slice.index
        length_slice_indices.append(length_slice_index)
        print(length_slice_index)

        #find the according Bak values at the given indices
        Bak_values = Bak_percent.iloc[length_slice_index]
        print(Bak_values)

        #calculate the median in each slice
        median = Bak_values.mean()
        rollmedians.append(median)

        #create length column with adequate window size
        rollmed_lengths.append(x)


        x += window_size/4  # increase x with window size durch 2 oder 4 um wirklich nen rolling zu haben!!!


    print(length_slices)
    print(length_slice_indices)
    print(rollmedians)
    print(len(rollmedians))
    print(len(rollmed_lengths))




    ################################PLOT####################################################
    # sns.scatterplot(x="Length", y="Percent Bax", data=df, color="#0EB30E")
    sns.scatterplot(x=length, y=Bak_percent, color="#808080", size= 1, legend=False)

    # add rolling median to the plot
    sns.lineplot(x=rollmed_lengths, y=rollmedians, color="#34e1eb")

    # wie weit soll die y axe gehen
    plt.ylim(0, 100)
    # plt.legend(labels=["BAX", "BAK"], fontsize=16, title_fontsize=20, loc='upper right')
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    #second y axis für Bax
    ax2 = plt.twinx()
    sns.scatterplot(x=length, y=Bax_percent, color="#808080", size= 1, ax=ax2, legend=False)
    plt.ylim(100, 0)

    #Überschrift und axis labels
    plt.xlabel('Length [µm]', fontsize=16)
    # plt.ylabel('Amount of BAX vs BAK [%]', fontsize=16)

    # add 50% line
    plt.axhline(y=50, color='black', linestyle='-')

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    #erstlle den Plot
    plt.plot()

    output_file = "P:/Private/practice/quantification_of_imaging_experiments/manual_ring_quantification_all-rings/result_plots/20220830_Bak_percent_with_rolling-mean.svg"
    plt.savefig(output_file)

    # zeigs her
    plt.show()


if __name__ == '__main__':
    main()