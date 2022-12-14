'''
This program let's the user choose a csv files.
Then plots percent Bax vs Pearson.
Göttingen, August 2022, Sarah Vanessa Schweighofer, MPI-NAT
'''

import os
from tkinter import filedialog
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob2
from utils.utils import *


def main():
    file = filedialog.askopenfile()
    print(file)

    df = pd.read_csv(file, encoding='latin1')  # latin1 encocing needed in order to be able to read special chars like "µ"
    print(df)

    length = df['Length']
    pearson = df['Pearson coefficient']

    rollmeans, rollmean_x = rolling_mean(0.4, 0.4, length, pearson, 3.9, 4)

    plot = sns.scatterplot(x="Length", y="Pearson coefficient", data=df, color="#808080", size= 1, legend=False)

    # add rolling median to the plot
    sns.lineplot(x=rollmean_x, y=rollmeans, color="#34e1eb")

    # wie weit soll die y axe gehen
    plt.ylim(-1, 1)
    # ich will nur alle 0.5 Einheiten einen Tickmark
    plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.5))

    plt.plot()
    plt.show()


if __name__ == '__main__':
    main()