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

    table = pd.read_csv(file, encoding='latin1')  # latin1 encocing needed in order to be able to read special chars like "µ"
    print(table)

    Bax = table["Bax Intensities"]
    Bak = table["Bak Intensities"]

    pearson = Bax.corr(Bak, method="pearson")  # correlate two specific series with each other!
    print(pearson)

    pearson = Bak.corr(Bax, method="pearson")
    print(pearson)


if __name__ == '__main__':
    main()
