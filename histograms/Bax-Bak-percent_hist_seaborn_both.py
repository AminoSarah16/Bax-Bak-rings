'''
This program opens a folder with csv files.
Then calculates the Pearson correlation coefficient.
Göttingen, March 2022, Sarah Vanessa Schweighofer, MPI-NAT
'''

import os
from tkinter import filedialog
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



def main():
    file = filedialog.askopenfile()  # open ‪P:\Private\practice\quantification_of_imaging_experiments\manual_ring_quantification_all-rings\Bax_Bak_percent.csv
    print(file)

    df = pd.read_csv(file, encoding='latin1')  # latin1 encocing needed in order to be able to read special chars like "µ"
    print(df)
    percent = df['Percent']
    baxk = df['Baxk']

    file2 = filedialog.askopenfile() # open ‪P:\Private\practice\quantification_of_imaging_experiments\manual_ring_quantification_all-rings\results_all.csv
    print(file2)

    df2 = pd.read_csv(file2, encoding='latin1')  # latin1 encocing needed in order to be able to read special chars like "µ"
    print(df2)
    Bax_percent = df2['Percent Bax']
    Bax_median = Bax_percent.median()

    Bak_percent = df2['Percent Bak']
    Bak_median = Bak_percent.median()

    ###################################   ###########################################
    # print("The Bax median is " + str(Bax_median) + "The Bak median is " + str(Bak_median) + ". I analyzed " + str(len(df)) + " rings.")

    # same for Both
    sns.set_style("ticks")
    plt.figure(figsize=(9, 6))  # needs to be before the plot call
    hist = sns.displot(x=percent, hue=baxk, kde=False, palette=["#0EB30E", "#D10FD1"], binwidth=10, binrange=(0, 100), height=8.27, aspect=11.7/8.27, legend=False) # height=8.27, aspect=11.7/8.27 so stellt man die Größe beim displor ein, bei anderene gehts über figsize; das sind die Werte für A4 in inches
    # plt.title('BAX and BAK percents in the ring', y=0.97, fontsize=24) # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    plt.xticks(fontsize=28, rotation=45)
    plt.yticks(fontsize=28)

    # sets params for the ticks themselves, not the labels
    plt.tick_params(direction='inout', length=6, width=2,
                    colors='k')  # , grid_color='r', grid_alpha=0.5) #direction : {'in', 'out', 'inout'}: Puts ticks inside the axes, outside the axes, or both.

    #plt.xticks(fontsize=20)
    #plt.yticks(fontsize=20)
    #plt.xlabel('Amount of BAX or BAK [%]', fontsize=24)
    #plt.ylabel('Number of rings', fontsize=24)
    #plt.tick_params(direction='out', length=6, width=2, colors='k')
    plt.tight_layout() #damits keine legends abschneidet und so
    # add the vertical line for the median
    plt.axvline(x=Bax_median, ymax=0.95, color='green', lw=2.5)
    plt.axvline(x=Bak_median, ymax=0.95, color='magenta', lw=2.5) #ymax makes the line not go into the title, the variable median comes from above
    plt.hist
    plt.show()

if __name__ == '__main__':
    main()