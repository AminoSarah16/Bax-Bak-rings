'''
This program opens csv files of ring line profiles in one folder.
Then reads out all Bax and Bak values and calculates the min and max for all the samples in the folder and saves it in a new csv.
From this it then opens all the csvs again and saves new csvs with normalized values to this general MIN/MAX values..
User needs to just run the script, everything else is asked for.
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
    # prints out the number of files in the selected folder with the wanted file format and adds them to a list
    file_format = ".csv"
    filenames = [filename for filename in sorted(os.listdir(root_path)) if filename.startswith(("Plot_"))]
    print("There are {} files with this format.".format(len(filenames)))
    if not filenames:  # pythonic for if a list is empty
        print("There are no files with this format.")

    Bax_maxes = []  # empty list for all mins and maxes, all of these are gonna be our columns in the final csv.
    Bak_maxes = []
    Bax_mins = []
    Bak_mins = []

    for filename in filenames:
        print(filename)
        file_path = os.path.join(root_path, filename)
        df = pd.read_csv(file_path, encoding='latin1')  # latin1 encocing needed in order to be able to read special chars like "µ"
        print(df)

        ###### save all maximumn and minumum Bax and Bak values in one large csv #####################
        Bax_max = df["Bax Intensities"].max()  # in order to calculate the max of each colum
        Bak_max = df["Bak Intensities"].max()
        Bax_min = df["Bax Intensities"].min()
        Bak_min = df["Bak Intensities"].min()

        Bax_maxes.append(Bax_max)
        Bak_maxes.append(Bak_max)
        Bax_mins.append(Bax_min)
        Bak_mins.append(Bak_min)

    # create the min/max output table

    data = {"filenames": filenames,
            "Bax max": Bax_maxes,
            "Bak max": Bak_maxes,
            "Bax min": Bax_mins,
            "Bak min": Bak_mins}

    print(data)

    df = pd.DataFrame(data)

    result_path = os.path.join(root_path, 'results')
    if not os.path.isdir(result_path):
        os.makedirs(result_path)
    savepath = os.path.join(result_path, "mins_maxes.csv")
    df.to_csv(savepath)


if __name__ == '__main__':
    main()