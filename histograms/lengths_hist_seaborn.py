'''
This program opens the csv written by the superscript.
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

    plt.figure(figsize=(9, 6))  # needs to be before the plot call
    # sns.axes_style({'axes.spines.left': True, 'axes.spines.bottom': True, 'axes.spines.right': True, 'axes.spines.top': True})
    sns.histplot(x=length, kde=True, color="#808080", binwidth=0.1, binrange=(0, 4)) # height=8.27, aspect=11.7/8.27 so stellt man die Größe beim displor ein, bei anderene gehts über figsize; das sind die Werte für A4 in inches
    # kde = kernel density estimation distribution aka the line over te histogram, length measures in inch!!
    # plt.title('Ring sizes', y=0.97, fontsize=24) # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    # plt.box(on=True)

    plt.xticks(fontsize=28, rotation=45)
    plt.yticks(fontsize=28)

    # sets params for the ticks themselves, not the labels
    plt.tick_params(direction='inout', length=6, width=2, colors='k')  # , grid_color='r', grid_alpha=0.5) #direction : {'in', 'out', 'inout'}: Puts ticks inside the axes, outside the axes, or both.


    # plt.xlabel('Ring circumference [µm]', fontsize=24)
    # plt.ylabel('Count', fontsize=24)
    plt.tight_layout() #damits keine legends abschneidet und so


    # add the vertical line for the median
    plt.axvline(x=median, ymax=0.95, color='black', lw=2.5)  # ymax makes the line not go into the title, the variable median comes from above
    plt.show()

    ###################################  write text file with median and number of analyzed rings  ###########################################
    # savepath = os.path.join(root_path, "lengths.txt")
    # with open(savepath, "w") as f:  # Opens file and casts as f
    #     f.write("The median is " + str(median) + ". I analyzed " + str(len(df)) + " rings.")  # Writing
    #     # File closed automatically


if __name__ == '__main__':
    main()