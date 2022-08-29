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


def main():
    file = filedialog.askopenfile()
    print(file)

    df = pd.read_csv(file, encoding='latin1')  # latin1 encocing needed in order to be able to read special chars like "µ"
    print(df)

    plot = sns.scatterplot(x="Length", y="Pearson coefficient", data=df, color="#808080")
    plot.set_ylim(-1, 1)
    plt.plot()
    plt.show()


if __name__ == '__main__':
    main()