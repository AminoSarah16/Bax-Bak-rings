'''
This program opens a folder with subfolders where I hopefully find files named "results.csv.
Then createes one big results file.
Göttingen, August 2022, Sarah Vanessa Schweighofer, MPI-NAT
'''

import os
from tkinter import filedialog
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob2
from natsort import natsort_keygen  #needed to sort naturally in Python



def main():
    appended_data = []
    # let the user choose the folder containing the images to be converted
    root_path = filedialog.askdirectory()  # prompts user to choose directory. From tkinter

    # prints out the number of files in the selected folder with the .tiff file format
    file_name = "results.csv"
    file_list = []
    # spaziert durch alle Subdirectories und sucht sich alle Files und packt sie in ne neue Liste, die ich oben neu kreiert habe
    for root, dirs, files in os.walk(root_path):
        for name in files:
            file_list.append(os.path.join(root, name))
            print(name)
    print(file_list)
    filenames = [filename for filename in file_list if filename.endswith(file_name)]
    print("There are {} files with this format.".format(len(filenames)))
    if not filenames:  # pythonic for if a list is empty
        print("There are no files with this format.")

    for filename in filenames:
        file_path = os.path.join(root_path, filename)
        table = pd.read_csv(file_path, encoding='latin1', index_col=None) #latin1 encocing needed in order to be able to read special chars like "µ"
        print(table)

        appended_data.append(table)

    #make a dataframe
    appended_data = pd.concat(appended_data, ignore_index=True)  #actually make a dataframe out of the appended tables
    print(appended_data)
    df = appended_data.sort_values(['Filename'], key=natsort_keygen()) #Key= natsort in order to sort the filenames naturally
    print(df)
    df = df.drop(columns=df.columns[0:1]).reset_index(drop=True)  #remove the annoying index columns from the individual results file and reset the index
    print(df)


    savepath = os.path.join(root_path, "results_all.csv")
    df.to_csv(savepath)


if __name__ == '__main__':
    main()