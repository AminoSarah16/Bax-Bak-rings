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
import numpy as np


def main():
    file = filedialog.askopenfile()
    print(file)

    df = pd.read_csv(file, encoding='latin1')  # latin1 encocing needed in order to be able to read special chars like "µ"
    print(df)
    Bax_percent = df['Percent Bax']
    Bax_median = Bax_percent.median()

    Bak_percent = df['Percent Bak']
    Bak_median = Bak_percent.median()



    ###################################   ###########################################
    print("The Bax median is " + str(Bax_median) + "The Bak median is " + str(Bak_median) + ". I analyzed " + str(len(df)) + " rings.")

    # visualize as histogram with seaborn
    sns.set_style("white")
    hist = sns.displot(x=Bax_percent, kde=True, color="#808080", binwidth=10, binrange=(0, 100), height=8.27, aspect=11.7/8.27) # height=8.27, aspect=11.7/8.27 so stellt man die Größe beim displor ein, bei anderene gehts über figsize; das sind die Werte für A4 in inches
    # kde = kernel density estimation distribution aka the line over te histogram, length measures in inch!!
    plt.title('Bax percent in the ring', y=0.97, fontsize=24) # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel('Amount of Bax [%]', fontsize=24)
    plt.ylabel('Number of rings', fontsize=24)
    plt.tight_layout() #damits keine legends abschneidet und so
    # add the vertical line for the median
    plt.axvline(x=Bax_median, ymax=0.95, color='black', lw=2.5) #ymax makes the line not go into the title, the variable median comes from above
    plt.hist
    plt.show()

    # same for Bak
    sns.set_style("white")
    hist = sns.displot(x=Bak_percent, kde=True, color="#808080", binwidth=10, binrange=(0, 100), height=8.27, aspect=11.7/8.27) # height=8.27, aspect=11.7/8.27 so stellt man die Größe beim displor ein, bei anderene gehts über figsize; das sind die Werte für A4 in inches
    # kde = kernel density estimation distribution aka the line over te histogram, length measures in inch!!
    plt.title('Bak percent in the ring', y=0.97, fontsize=24) # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel('Amount of Bak [%]', fontsize=24)
    plt.ylabel('Number of rings', fontsize=24)
    plt.tight_layout() #damits keine legends abschneidet und so
    # add the vertical line for the median
    plt.axvline(x=Bak_median, ymax=0.95, color='black', lw=2.5) #ymax makes the line not go into the title, the variable median comes from above
    plt.hist
    plt.show()



if __name__ == '__main__':
    main()