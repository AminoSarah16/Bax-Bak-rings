'''
This program opens a csv file.
Then calculates the Pearson correlation coefficient.
Then shifts the two correlated series one position and adds the lowest value on top, then calculates the Pearson again and so on.
Spits out a curve with the Pearsons plotted in y and the deltaD plotted in x.
Göttingen, August 2022, Sarah Vanessa Schweighofer, MPI-NAT
'''


import os
from tkinter import filedialog
import pandas as pd
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


def main():
    pearsons = []
    file = filedialog.askopenfile()
    print(file)

    table = pd.read_csv(file, encoding='latin1')  # latin1 encocing needed in order to be able to read special chars like "µ"
    print(table)

    Bax = table["Bax Intensities"]  # in order to calculate the mean of each column
    print(len(Bax))
    Bak = table["Bak Intensities"]
    lengths = table["Âµm"]

    pearson = Bax.corr(Bak, method="pearson")  # easier way to correlate two specifi series with each other!
    print(pearson)

    pearsons.append(pearson)

    pearson = Bak.corr(Bax, method="pearson")
    print(pearson)

    ################ shift the Bax series one down and fill top with last value until reached top again#########
    for i in range(len(Bax)-1): ## -1 damit der das letzte nicht macht, weil das wäre dann wieder glecih wie die Ursprunswerte
        # convert Series to numpy array and select last, which is needed to fill the series from the top:
        last = Bax.values[-1]
        print(last)
        Bax = Bax.shift(1, fill_value=last)  # shifts the series one down
        print(Bax)

        pearson = Bax.corr(Bak, method="pearson")
        print(pearson)
        pearsons.append(pearson)
    print(pearsons)
    ############################################################################################################

    ####################### plot all the pearsons against delta D ##################
    plot = sns.lineplot(x=lengths, y=pearsons, color="k", linewidth=3)
    # Größe des finalen Plots
    plot.figure.set_figwidth(11.7)
    plot.figure.set_figheight(8.27)

    plot.set_ylim(-1, 1)
    # plt.title('spatial correlation', fontsize=24)  # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    plt.xlabel('\u0394 d [µm]', fontsize=20)
    plt.ylabel('Pearson', fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.tick_params(direction='inout', length=6, width=2, colors='k')
    plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.5))
    # plt.legend(fontsize=16, title_fontsize=20)

    # add mean line
    plt.axhline(y=0, color='#808080', linestyle='-', linewidth=3)

    # #### add first hitting zero point to graphic ############
    # plt.scatter(lengths[first_hitting_zero], pearson_arr[first_hitting_zero], s=56, marker="o", c="green")
    #
    # #### add first local minimum to graphic ############
    # plt.scatter(lengths[first_local_mimimum], pearson_arr[first_local_mimimum], s=56, marker="o", c="black")

    # Zeigs her
    plt.plot()
    plt.show()
    #####################################################################################


if __name__ == '__main__':
    main()