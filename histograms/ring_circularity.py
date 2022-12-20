'''
This program opens ...ROI_measurements_FIJI.csv files
Then plots the ring circularities.
Göttingen, Sept 2022, Sarah Vanessa Schweighofer, MPI-NAT
'''


import os
from tkinter import filedialog
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils.utils import *

def main():
    names = []  # empty list for all filenames, both of these are gonna be our columns in the final csv.
    circularities = []
    # let the user choose the folder containing the images to be converted
    root_path = filedialog.askdirectory()  # prompts user to choose directory. From tkinter

    # prints out the number of files in the selected folder with the .tiff file format
    file_ending = "area-results_FIJI.csv"
    file_list = []
    # spaziert durch alle Subdirectories und sucht sich alle Files und packt sie in ne neue Liste, die ich oben neu kreiert habe
    for root, dirs, files in os.walk(root_path):
        for name in files:
            file_list.append(os.path.join(root, name))
            print(name)
    print(file_list)
    filenames = [filename for filename in file_list if filename.endswith(file_ending)]
    print("There are {} files with this format.".format(len(filenames)))
    if not filenames:  # pythonic for if a list is empty
        print("There are no files with this format.")

    for filename in filenames:
        print(filename)
        names.append(filename)
        file_path = os.path.join(root_path, filename)
        df = pd.read_csv(file_path, encoding='latin1')  # latin1 encocing needed in order to be able to read special chars like "µ"
        print(df)

        ###### get the series #####################
        circularity = df["Round"]  # choose between circularity ("Circ."), roundness ("Round") and aspect ration ("AR)
        print(circularity)
        circularities.append(circularity)

    print(circularities)

    circ_seris = pd.concat(circularities, ignore_index=True)
    print(circ_seris)
    median = circ_seris.median()
    print(median)
    min = circ_seris.min()
    max = circ_seris.max()
    print(min, max)


    #### plot the whole story with seaborn/matplotlib #########################################################
    sns.set_style("ticks")
    plt.figure(figsize=(9, 6)) #needs to be before the plot call
    sns.histplot(x=circ_seris, kde=True, color="#808080", binwidth=0.02, binrange=(0, 1))
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.tick_params(direction='out', length=6, width=2, colors='k')
    plt.xlabel('Roundness', fontsize=24)
    plt.ylabel('Count', fontsize=24)
    plt.tight_layout()  # damits keine legends abschneidet und so

    plt.axvline(x=median, ymax=0.95, color='black', lw=2.5)  # ymax makes the line not go into the title, the variable median comes from above

    plt.show()







if __name__ == '__main__':
    main()