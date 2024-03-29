'''
This program opens a csv file.
Then plots the Pearson correlation coefficient.
Göttingen, Sept 2022, Sarah Vanessa Schweighofer, MPI-NAT
MIT License

Copyright (c) 2022, Sarah Vanessa Schweighofer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os
from tkinter import filedialog
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



def main():
    file = filedialog.askopenfile()  # open ‪P:\Private\practice\quantification_of_imaging_experiments\manual_ring_quantification_all-rings\Bax_Bak_percent.csv
    print(file)

    df = pd.read_csv(file, encoding='latin1')  # latin1 encocing needed in order to be able to read special chars like "µ"
    print(df)
    pearsons = df['Pearson coefficient']


    median = pearsons.median()

    # visualize as histogram with seaborn
    sns.set_style("ticks")
    plt.figure(figsize=(9, 6))  # needs to be before the plot call
    hist = sns.histplot(x=pearsons, kde=True, color="#808080", binwidth=0.1, binrange=(-1, 1)) # height=8.27, aspect=11.7/8.27 so stellt man die Größe beim displor ein, bei anderene gehts über figsize; das sind die Werte für A4 in inches, height=8.27, aspect=11.7/8.27
    # kde = kernel density estimation distribution aka the line over te histogram, length measures in inch!!
    # plt.title('Spatial Correlation of Bax and Bak in the ring', y=0.97, fontsize=24) # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    plt.xticks(fontsize=28, rotation=45)
    plt.yticks(fontsize=28)

    # sets params for the ticks themselves, not the labels
    plt.tick_params(direction='inout', length=6, width=2,
                    colors='k')  # , grid_color='r', grid_alpha=0.5) #direction : {'in', 'out', 'inout'}: Puts ticks inside the axes, outside the axes, or both.


    # plt.xlabel('Pearson Correlation Coefficients', fontsize=24)
    # plt.ylabel('Count', fontsize=24)
    plt.tight_layout() #damits keine legends abschneidet und so
    # add the vertical line for the median
    plt.axvline(x=median, ymax=0.95, color='black', lw=2.5) #ymax makes the line not go into the title, the variable median comes from above
    plt.hist
    plt.show()


if __name__ == '__main__':
    main()