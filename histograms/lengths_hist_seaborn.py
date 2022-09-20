'''
This program opens the superscript.
Then plots the lengths.
Göttingen, March 2022, Sarah Vanessa Schweighofer, MPI-NAT
'''

import seaborn as sns
import matplotlib.pyplot as plt
from utils.utils import *



def main():
    df = df_from_csv()
    print(df)

    ###### get the series #####################
    length = df["Length"]

    median = length.median()
    ################################################################################################################

    #### plot the whole story with pandas/matplotlib ###########################################################################
    # visualize as histogram with seaborn
    sns.set_style("ticks")
    # sns.axes_style({'axes.spines.left': True, 'axes.spines.bottom': True, 'axes.spines.right': True, 'axes.spines.top': True})
    sns.displot(x=length, kde=False, color="#808080", binwidth=0.1, binrange=(0, 4), height=8.27, aspect=11.7/8.27) # height=8.27, aspect=11.7/8.27 so stellt man die Größe beim displor ein, bei anderene gehts über figsize; das sind die Werte für A4 in inches
    # kde = kernel density estimation distribution aka the line over te histogram, length measures in inch!!
    # plt.title('Ring sizes', y=0.97, fontsize=24) # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    # plt.box(on=True)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.tick_params(direction='out', length=6, width=2, colors='k')
    plt.xlabel('Ring circumference [µm]', fontsize=24)
    plt.ylabel('Count', fontsize=24)
    plt.tight_layout() #damits keine legends abschneidet und so

    plt.axvline(x=median, ymax=0.95, color='black', lw=2.5)  # ymax makes the line not go into the title, the variable median comes from above
    # add the vertical line for the median
    plt.hist
    plt.show()

    ###################################  write text file with median and number of analyzed rings  ###########################################
    # savepath = os.path.join(root_path, "lengths.txt")
    # with open(savepath, "w") as f:  # Opens file and casts as f
    #     f.write("The median is " + str(median) + ". I analyzed " + str(len(df)) + " rings.")  # Writing
    #     # File closed automatically


if __name__ == '__main__':
    main()