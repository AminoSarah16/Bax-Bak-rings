import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
import numpy as np
import pandas as pd

###### basic pandas funcionality to read a csv and make a dataframe out of it. file location is being asked via tkinter
def df_from_csv():
    file = filedialog.askopenfile()
    df = pd.read_csv(file, encoding='latin1')  # better already sort the csv manually before importing
    return df
#####################################################################################################################


###### basic pandas funcionality to read a xls and make a dataframe out of it. file location is being asked via tkinter
def df_from_xls():
    file = filedialog.askopenfile()
    df = pd.read_excel(file, encoding='latin1')  # better already sort the csv manually before importing
    return df
#####################################################################################################################