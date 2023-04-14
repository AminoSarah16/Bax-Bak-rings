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


def main():
    file = filedialog.askopenfile() #open ‪P:\Private\practice\quantification_of_imaging_experiments\manual_ring_quantification_all-rings\results_all.csv
    print(file)

    df = pd.read_csv(file, encoding='latin1')  # latin1 encocing needed in order to be able to read special chars like "µ"
    print(df)

    pearson = df['Pearson coefficient']
    Bax_percent = df['Percent Bax']
    # Bax_percent = df['Percent Bax']

    # #############################calculate running median##################################
    # Bax_slices = []
    # Bax_slice_indices = []
    # rollmeans = []
    # rollmean_sizes = []
    # # take windows of 10 %
    # window_size = 10
    #
    # # create starting value at %
    # x = 0
    #
    # # schleife mit stepsize
    # while x < 65:  # 100% is the maximal possible BAK amount
    #     # find all the values in a certain window of the series (= a slice)
    #     Bax_slice = Bax_percent[(Bax_percent >= x) & (Bax_percent < (x + window_size))].sort_values()  # find all the values between x and (x plus stepsize) and sort the list ascending
    #     print(x)
    #     print(Bax_slice)
    #     Bax_slices.append(Bax_slice)
    #
    #     # find the index values of the values in the slice
    #     slice_index = Bax_slice.index
    #     Bax_slice_indices.append(slice_index)
    #     print(slice_index)
    #
    #     # find the according Pearson values at the given indices
    #     PCC_values = pearson.iloc[slice_index]
    #     print(PCC_values)
    #
    #     # calculate the median in each slice
    #     mean = PCC_values.mean()
    #     rollmeans.append(mean)
    #
    #     # create length column with adequate window size
    #     rollmean_sizes.append(x)
    #
    #     x += window_size / 4  # increase x with window size durch 2 oder 4 um wirklich nen rolling zu haben!!!
    #
    # print(Bax_slices)
    # print(Bax_slice_indices)
    # print(rollmeans)
    # print(len(rollmeans))
    # print(len(rollmean_sizes))


    plot = sns.regplot(x=Bax_percent, y=pearson, data=df, scatter_kws={"color": "#808080", "s":3}, line_kws={"color": "#34e1eb", 'linewidth':1}) # color="#808080", , size= 1, legend=False)

    # # add rolling median to the plot
    # sns.lineplot(x=rollmean_sizes, y=rollmeans, color="#34e1eb")

    # wie weit soll die y axe gehen
    plt.xlim(0, 100)
    plt.ylim(-1, 1)
    # ich will nur alle 0.5 Einheiten einen Tickmark
    plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.5))

    #keine Axis labels
    plot.set(xlabel=None)
    plot.set(ylabel=None)


    plt.plot()
    plt.show()


if __name__ == '__main__':
    main()