'''
This program opens a folder with csv files.
Then retrieves the lenght of the line profile, if the series exists.
Then plots the line profiles as histogram.
Göttingen, May 2022, Sarah Vanessa Schweighofer, MPI-NAT
'''

import os
from tkinter import filedialog
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob2



def main():
    #let the user state the name of the condition
    condition = input("Please choose a name for the condition (cell type, knock down etc): ")
    # let the user choose the folder containing the images to be converted
    root_path = filedialog.askdirectory()
    root_path2 = glob2.glob(root_path)  # prompts user to choose directory. From tkinter
    # glob is needed for the wildcards to work later when walking childpaths
    print(root_path)
    result_path = os.path.join(root_path, 'results')
    if not os.path.isdir(result_path):
        os.makedirs(result_path)

    path_list = []
    for p in root_path2:
        child_paths = glob2.glob(os.path.join(p, 'IF*'))
        for child_path in child_paths:
            path_list.append(child_path)
        print(path_list)

    names = []  # empty list for all filenames, both of these are gonna be our columns in the final csv.
    lengths = []  # empty list for all lengths, both of these are gonna be our columns in the final csv.
    conditions = []  # empty list for all lengths, both of these are gonna be our columns in the final csv.

    file_format = ".csv"

    for path in path_list:
        filenames = [filename for filename in sorted(os.listdir(path)) if filename.startswith(("Plot_")) and filename.endswith(file_format)]
        # also create a subfolder where the converted images would be saved

        print(filenames)

        # now that we have all files, go through the list of files
        for filename in filenames:
            print(filename)
            file_path = os.path.join(path, filename)
            print(file_path)

            table = pd.read_csv(file_path, encoding='latin1')  #latin1 encocing needed in order to be able to read special chars like "µ"
            print(table)
            if 'µm' in table.columns:
                names.append(filename)
                length = table.at[table.index[-1], 'µm']
                lengths.append(length)
                conditions.append(condition)

        print(names)
        print(lengths)
        print(conditions)

    ##################################  create the final output table  #####################################################

    data = {"filenames": names,
             "length": lengths,
            "conditions": conditions}

    print(data)

    df = pd.DataFrame(data)

    ######################################  calculate the median  ########################################################
    median = df["length"].median()

    print(df)
    print("The length median is: {}.".format(median))

    savepath = os.path.join(result_path, "Lengths.csv")
    df.to_csv(savepath)

    ###################################  visualize as histogram with seaborn  ###########################################
    sns.set_style("white")
    hist = sns.displot(x='length', data=data, kde=True, color="#808080", binwidth=0.1, binrange=(0, 6), height=8.27, aspect=11.7/8.27) # height=8.27, aspect=11.7/8.27 so stellt man die Größe beim displor ein, bei anderene gehts über figsize; das sind die Werte für A4 in inches
    # kde = kernel density estimation distribution aka the line over te histogram, length measures in inch!!
    plt.title('Ring circumference', y=0.97, fontsize=24) # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel('Lengths [µm]', fontsize=24)
    plt.ylabel('Count', fontsize=24)
    plt.tight_layout() #damits keine legends abschneidet und so
    # add the vertical line for the median
    plt.axvline(x=median, ymax=0.95, color='black', lw=2.5) #ymax makes the line not go into the title, the variable median comes from above
    plt.hist
    savepath = os.path.join(result_path, "lengths.png")
    plt.savefig(savepath)
    plt.show()
    # plt.close()

    ###################################  write text file with median and number of analyzed rings  ###########################################
    savepath = os.path.join(result_path, "lengths.txt")
    with open(savepath, "w") as f:  # Opens file and casts as f
        f.write("The median is " + str(median) + ". I analyzed " + str(len(df)) + " rings.")  # Writing
        # File closed automatically

if __name__ == '__main__':
    main()