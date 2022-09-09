'''
This program opens a folder with subfolders with csv files.
Then plots the deltaD vs median Pearson correlation coefficient.
Spits out a csv and curve.
Göttingen, August 2022, Sarah Vanessa Schweighofer, MPI-NAT
'''

import os
from tkinter import filedialog
import pandas as pd
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from utils import *


def main():
    names = []  # empty list for all filenames, both of these are gonna be our columns in the final csv.

    # let the user choose the folder containing the images to be converted
    root_path = filedialog.askdirectory()  # prompts user to choose directory. From tkinter

    # prints out the number of files in the selected folder with the .tiff file format
    file_ending = "pearsons_delta_d.csv"
    file_list = []
    # spaziert durch alle Subdirectories und sucht sich alle Files und packt sie in ne neue Liste, die ich oben neu kreiert habe
    for root, dirs, files in os.walk(root_path):
        for name in files:
            file_list.append(os.path.join(root, name))
            print(name)
    print(file_list)
    filenames = [filename for filename in file_list if filename.endswith(file_ending)]
    print("There are {} files with this format.".format(len(filenames)))
    if not filenames:  # pythonic for if a list is empty
        print("There are no files with this format.")


    all_pearsons = [] #make an empty list which will be filled with the einzelne series of PCCs
    for filename in filenames:
        print(filename)
        names.append(filename)
        file_path = os.path.join(root_path, filename)
        table = pd.read_csv(file_path, encoding='latin1')  # latin1 encocing needed in order to be able to read special chars like "µ"
        print(table)

        pearsons = table["pearson"]

        all_pearsons.append(pearsons)

    #create a dataframe of the list of lists of PCCs
    df = pd.DataFrame(all_pearsons)
    print(df)

    # take the values from certain columns for plotting later:
    deltaD_0 = list(df.iloc[:, 0]) # i have to cast this into a list here in order to be able to call it in the displot below.. why? no idea. # actually I had to make a new dataframe anyways, but at least that worked now!!!
    deltaD_6 = list(df.iloc[:, 6]) #at 90 nm
    deltaD_14 = list(df.iloc[:, 14]) #at 210 nm
    print(deltaD_0)

    #need to make a new dataframe out of it in order to be able to include it into the displot later!!
    df3 = pd.concat(axis=0, ignore_index=True, objs=[pd.DataFrame.from_dict({'value': deltaD_0, 'name': 'zero'}), pd.DataFrame.from_dict({'value': deltaD_6, 'name': 'six'}), pd.DataFrame.from_dict({'value': deltaD_14, 'name': 'fourteen'})])

    # calculate the median for every column (meaning at every delta d)
    medians = []
    for column in df:
        median = df[column].median()
        medians.append(median)

    print(medians)

    #make delta d series
    delta_d = [i*15 for i in range(len(medians))]
    print(delta_d)


    # create theoutput table

    data = {"delta d": delta_d,
            "PCC median": medians}

    print(data)

    df2 = pd.DataFrame(data)

    result_path = os.path.join(root_path, 'results')
    if not os.path.isdir(result_path):
        os.makedirs(result_path)
    savepath = os.path.join(result_path, "medianPCC_vs_deltaD.csv")
    df2.to_csv(savepath)

    #################### calcualte some values ###############################
    # make numpy arrays out of the lists in order to do calculations
    medians_arr = np.array(medians)
    delta_arr = np.array(delta_d)

    # calculate where the curve hits zero the first time
    hitting_zero = np.where(medians_arr <= 0)
    print("These are all the values below zero: {}".format(hitting_zero))
    first_hitting_zero = hitting_zero[0][0]  # I only want the first value of the array (and for some reason the array is a 2D array, that's why I have to do [0] twice...
    print("The curve is below zero for the first time at the {}th measurement".format(first_hitting_zero))
    the_one = medians[first_hitting_zero]
    print("This is the median PCC value where the curve is first below zero: {}".format(the_one))
    print("This is the delta d value where the curve is first below zero: {}".format(delta_arr[first_hitting_zero]))
    print("This is the delta d value on before the curve is first below zero: {}".format(delta_arr[first_hitting_zero-1]))
    the_one_before = medians[first_hitting_zero-1]
    print("This is the median value one before the curve is first below zero: {}".format(the_one_before))


    y = 0
    yp = [the_one, the_one_before]
    fp = [delta_arr[first_hitting_zero], delta_arr[first_hitting_zero-1]]

    delta_at_y0 = np.interp(y, yp, fp)

    print("This is the interpolated deltaD value at which PCC is exactly 0: {}".format(delta_at_y0))

    # plot mean at 50% between start and where PCC hits the 0
    print("This is the median of the Pearsons without rotating: {}".format(medians_arr[0]))
    PCC50 = medians_arr[0]/2
    print("This is the median of the Pearsons dropped to 50% of its original value: {}".format(PCC50))

    print(medians_arr[0:first_hitting_zero])
    print(delta_arr[0:first_hitting_zero])

    x = delta_arr[0:first_hitting_zero]
    y = medians_arr[0:first_hitting_zero]

    # y should be sorted for both of these methods
    order = y.argsort()
    y = y[order]
    x = x[order]

    delta50 = interp_x_from_y(PCC50, x, y)
    print("This is the delta d value in nm where the curve is at 50% from the original PCC: {}".format(delta50))

    # ####################### plot all the pearsons against delta D ##################
    # plot = sns.lineplot(x=delta_d[0:21], y=medians[0:21], color="#808080") # [0:21] covers the first 300nm
    #
    # # Größe des finalen Plots
    # plot.figure.set_figwidth(11.7)
    # plot.figure.set_figheight(8.27)
    #
    # # ax = plt.gca()
    # # ax.grid(which='zero', axis='both', linestyle='--')
    #
    # plot.set_ylim(-0.2, 0.5)
    # plot.set_xlim(0, 300)
    # plt.title('general spatial correlation', fontsize=24)  # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    # plt.xlabel('\u0394 d [nm]', fontsize=20) ##TODO: insert \u0394 as delta symbol
    # plt.ylabel('PCC', fontsize=20)
    # # plt.legend(fontsize=16, title_fontsize=20)
    #
    # # add 0 x line
    # plt.axhline(y=0, linewidth=0.5, color='black', linestyle='-')
    #
    # # add 0 y line
    # plt.axvline(x=delta_at_y0, color='#80c2d9', linestyle='dashed')
    #
    # # add 50% y line
    # plt.axvline(x=delta50, color='green', linestyle='dashed')
    # # # add 50% x line
    # # plt.axhline(y=medians[int(first_hitting_zero/2)], color='red', linestyle='dashed')
    #
    # # Zeigs her
    # plt.plot()
    # plt.show()

    # make histogram at specific delta Ds:
    # visualize as histogram with seaborn TODO: chose nicer colors and move the legend to the left
    sns.set_style("white")
    fig, ax = plt.subplots()
    hist = sns.displot(data=df3, x="value", hue="name", kde=True, palette=["#808080", "#90ee90", "#80c2d9"], binwidth=0.1, binrange=(-1, 1), height=8.27, aspect=11.7 / 8.27) # height=8.27, aspect=11.7/8.27 so stellt man die Größe beim displor ein, bei anderene gehts über figsize; das sind die Werte für A4 in inches
    # kde = kernel density estimation distribution aka the line over te histogram, length measures in inch!!
    plt.title('Spatial Correlation of Bax and Bak in the ring', y=0.97, fontsize=24)  # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel('Pearson Correlation Coefficients', fontsize=24)
    plt.ylabel('Count', fontsize=24)
    plt.tight_layout()  # damits keine legends abschneidet und so
    # add the vertical line for the median
    plt.axvline(x=df[0].median(), ymax=0.95, color='black', lw=2.5) # ymax makes the line not go into the title, the variable median comes from above
    plt.axvline(x=df[6].median(), ymax=0.95, color='green', lw=2.5)
    plt.axvline(x=0, ymax=0.95, color='#48a2c2', lw=2.5) #because I only have the pcc values slightly above and below zero I cheat here and set the median exactly to zero although this is not exact.
    plt.hist
    plt.show()


    # hist = sns.displot(x=all_pearsons[0], kde=True, color="#808080", binwidth=10, binrange=(0, 100), height=8.27, aspect=11.7 / 8.27)  # height=8.27, aspect=11.7/8.27 so stellt man die Größe beim displor ein, bei anderene gehts über figsize; das sind die Werte für A4 in inches
    # # kde = kernel density estimation distribution aka the line over te histogram, length measures in inch!!
    # plt.title('Bax percent in the ring', y=0.97, fontsize=24)  # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    # plt.xticks(fontsize=20)
    # plt.yticks(fontsize=20)
    # plt.xlabel('Amount of Bax [%]', fontsize=24)
    # plt.ylabel('Number of rings', fontsize=24)
    # plt.tight_layout()  # damits keine legends abschneidet und so
    # # add the vertical line for the median
    # plt.axvline(x=medians[0], ymax=0.95, color='black', lw=2.5)  # ymax makes the line not go into the title, the variable median comes from above
    # plt.hist
    # plt.show()


def interp_x_from_y(input, x, y):
    return np.interp(input, y, x)

if __name__ == '__main__':
    main()