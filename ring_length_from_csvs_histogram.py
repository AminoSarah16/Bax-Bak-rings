'''
This program opens some csv files.
Then retrieves the lenghtsand adds them all up with the condition to one big df.
Then plots the line profiles as histogram.
Göttingen, June 2022, Sarah Vanessa Schweighofer, MPI-NAT
'''

import os
from tkinter import filedialog
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils import *



def main():
    pd.set_option('display.max_rows', None)  # displays the whole df upon printing, toggle on if needed
    # let the user choose the folder where to save results
    root_path = filedialog.askdirectory()
    result_path = os.path.join(root_path, 'results')
    if not os.path.isdir(result_path):
        os.makedirs(result_path)

    ### open the csvs #######
    WT = df_from_csv()
    Bax_only = df_from_csv()
    Bak_only = df_from_csv()

    #########concatenate them#################
    frames = [WT, Bak_only, Bax_only]
    df = pd.concat(frames)
    df = df.reset_index()

    ##############################################################################################

    ###################################  visualize as histogram with seaborn  ###########################################
    sns.set_style("white")
    hist = sns.displot(x='length', data=df, hue="conditions", kde=True, palette=["#808080", "#D10FD1", "#0EB30E"], binwidth=0.1, binrange=(0, 6), height=8.27, aspect=11.7/8.27)
    # kde=True,
    # stat='frequency', or 'percent
    # height=8.27, aspect=11.7/8.27 so stellt man die Größe beim displor ein, bei anderene gehts über figsize; das sind die Werte für A4 in inches
    # kde = kernel density estimation distribution aka the line over te histogram, length measures in inch!!
    # multiple = "dodge", macht, dass die Balken voneinander wegrücken
    plt.title('Ring circumference', y=0.97, fontsize=24) # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel('Lengths [µm]', fontsize=24)
    plt.ylabel('Count', fontsize=24)
    plt.tight_layout() #damits keine legends abschneidet und so
    # add the vertical line for the median
    # plt.axvline(x=median, ymax=0.95, color='black', lw=2.5) #ymax makes the line not go into the title, the variable median comes from above
    plt.hist
    savepath = os.path.join(result_path, "lengths.png")
    plt.savefig(savepath)
    plt.show()
    # plt.close()

if __name__ == '__main__':
    main()