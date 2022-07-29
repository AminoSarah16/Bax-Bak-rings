'''
Opens a csv file.
User needs to choose the respective folder and input the changes.
Then draws a box plot of percentages, total vs 2D rings.
Results table obtained from Imaris analysis of 4PiSTORM data of Bax rings
Göttingen, 28.07.22 Sarah Vanessa Schweighofer, MPI-NAT
'''


import os
import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from utils import *

def main():
    pd.set_option('display.max_rows', None)  # displays the whole df upon printing, toggle on if needed

    ### open the first csv #######
    df = df_from_csv()
    print(df)
    print(len(df))
    percent = df["percent 2D/total"]*100


    ####### VIOLIN-PLOT################################
    viol = sns.violinplot(data=percent, inner="points", color="#808080")
    plt.title('percent of BAX rings detected in 2D', y=1, fontsize=16)  # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    plt.xlabel('')
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        labelbottom=False)  # labels along the bottom edge are off
    plt.ylabel('number of rings [%]', fontsize=16)
    # plt.viol
    # plt.savefig("P:/Private/practice/quantification_of_imaging_experiments/Cox8A-vs-DNA-release/" + "nucleoids_outside.png")
    plt.show()
    # plt.close()
    #######################################################

    ###### BOX-PLOT ########################################################################################
    box = sns.boxplot(data=percent, color="#808080")
    plt.title('percent of BAX rings detected in 2D', y=1, fontsize=16)  # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    plt.xlabel('')
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        labelbottom=False)  # labels along the bottom edge are off
    plt.ylabel('number of rings [%]', fontsize=16)

    # Add in points to show each observation
    sns.stripplot(data=percent, size=4, color=".3", linewidth=0)

    plt.box
    # plt.savefig("P:/Private/practice/quantification_of_imaging_experiments/Cox8A-vs-DNA-release/" + "area-Tom-vs-Cox_percent.png")
    plt.show()
    # plt.close()

    ##### PIE-CHART using matplotlib ########
    pie, ax = plt.subplots(figsize=[10, 6])
    # labels = data.keys()
    plt.pie(x=percent, autopct="%.1f%%", pctdistance=0.5) #abels=labels, explode=[0.05] * 4,
    plt.title('percent of BAX rings detected in 2D', y=1, fontsize=16)
    # pie.savefig("DeliveryPieChart.png")
    plt.show()



if __name__ == '__main__':
    main()