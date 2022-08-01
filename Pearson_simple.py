'''
This program opens a csv file.
Then calculates the Pearson correlation coefficient.
Göttingen, March 2022, Sarah Vanessa Schweighofer, MPI-NAT
'''


import os
from tkinter import filedialog
import pandas as pd



def main():

    file = filedialog.askopenfile()
    print(file)
    table = pd.read_csv(file, usecols=["Bax Intensities", "Bak Intensities"])
    print(table)

    pearson = table.corr(method="pearson")
    print(pearson)

    pearson = pearson.iat[0, 1] #as it spits out a correlation matrixbetween all coolumns in a dataframe, again as datafram itself, Ineed to pick the value out of the datafram, tha corrleates the two columns with each other
    print(pearson)


if __name__ == '__main__':
    main()