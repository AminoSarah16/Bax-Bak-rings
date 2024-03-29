'''
This program opens a folder with csv files.
Then calculates the relative content of Bax vs Bak in the line profiles.

Göttingen, May 2022 Sarah Vanessa Schweighofer (https://github.com/AminoSarah16), MPI-NAT

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
    # let the user choose the folder containing the tables
    root_path = filedialog.askdirectory()  # prompts user to choose directory. From tkinter
    # prints out the number of files in the selected folder with the wanted file format and adds them to a list
    file_format = ".csv"
    filenames = [filename for filename in sorted(os.listdir(root_path)) if filename.endswith(file_format)]
    print("There are {} files with this format.".format(len(filenames)))
    if not filenames:  # pythonic for if a list is empty
        print("There are no files with this format.")

    names = [] #empty list for all filenames, both of these are gonna be our columns in the final csv.
    lengths = []  # empty list for all the lengths
    Bax_percents = [] #empty list for al
    Bak_percents = []  # empty list for al

    for filename in filenames:
        print(filename)
        names.append(filename)
        file_path = os.path.join(root_path, filename)
        table = pd.read_csv(file_path, encoding='latin1')  #latin1 encocing needed in order to be able to read special chars like "µ"
        print(table)

        ##TODO: which input table is taken? how does it normalize and get to percenatge? numpy.amax? or mean?

        higher_values = table[["Bax Intensities", "Bak Intensities"]].max(axis=1)
        print(higher_values)


        ############count all the values in the specified column which are larger than the other##################
        Bax_column = table["Bax Intensities"]
        Bak_column = table["Bak Intensities"]
        Bax_count = Bax_column[Bax_column > Bak_column].count()
        print(Bax_count)
        Bak_count = Bak_column[Bak_column > Bax_column].count()
        print(Bak_count)
        Bax_percent = Bax_count/(Bax_count + Bak_count)*100
        Bak_percent= 100-Bax_percent
        print(Bax_percent)
        print(Bak_percent)
        Bax_percents.append(Bax_percent)
        Bak_percents.append(Bak_percent)
        #########################################################################################


        ##################create list with lengths############################################
        length = table['Âµm'].iloc[-1]
        lengths.append(length)
        print(lengths)
        ##########################################################################################

        ##############################create the final output table and save it######################################

        data = {"filename": names,
                "length": lengths,
                "Percent Bax": Bax_percents,
                "Percent Bak": Bak_percents}

        print(data)

        df = pd.DataFrame(data)
        print(df)

    savepath = os.path.join(root_path, "Percents.csv")
    df.to_csv(savepath)

    ##TODO: plot Bax-percentage as histogram

    #### plot the whole story #######################################################################################
    # my_color_palette = {"WT": "#0EB30E", "siCtrl": "#808080", "Mic60 KD": "#D10FD1", "Bax-Bak DKO": "k"}
    # # I am defining my own color plaette for the different samples that are in my dataset, I could also just use one of the pre-defined palettes from seaborn or make my own colorpalette independent from samples, like below:
    # # my_color_palette = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
    plot = sns.scatterplot(x="length", y="Percent Bax", data=df, color="#808080")
    ## #if one would want a second axis:
    # sns.scatterplot(x="length", y="Percent Bak", data=df, color="m", ax=plot.axes.twinx())
    # hue heißt die Farbgebung bezieht sich auf die sample-type, style ist die Art von Linie (strichliert etc) bezieht sich auf die treatment bedingung
    # data=df1 würde auch gehen, dann plottets alle 25 Zeitpunkte, hier hab ich aber halt nur 18 ausgewählt
    # plot.set_xticks(range(25))  # you could also set anintervall here!
    # # set size of the tickmark labels
    # plot.set_xticklabels(plot.get_xticks(), size=16)
    # plot.set_yticklabels(plot.get_yticks(), size=16)
    # plot.set_xlim(4, 24)  # adjusts, where the x axis meets the y axes
    # plt.title('Live/dead curves',
    #           fontsize=24)  # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    # plt.xlabel('Time [h]', fontsize=20)
    # plt.ylabel('Dead cells [%]', fontsize=20)
    # plt.legend(fontsize=16, title_fontsize=20)
    # # Größe des finalen Plots
    # plot.figure.set_figwidth(11.7)
    # plot.figure.set_figheight(8.27)
    # # Zeigs her
    plt.plot()
    plt.show()
    ##############################################################################################################



if __name__ == '__main__':
    main()