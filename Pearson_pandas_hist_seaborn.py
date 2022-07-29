'''
This program opens a folder with csv files.
Then calculates the Pearson correlation coefficient.
Göttingen, March 2022, Sarah Vanessa Schweighofer, MPI-NAT
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
    pearsons = [] #empty list for alle the pearson coefficients

    for filename in filenames:
        print(filename)
        names.append(filename)
        file_path = os.path.join(root_path, filename)
        table = pd.read_csv(file_path, encoding='latin1', usecols=["Bax Intensities", "Bak Intensities"])  #latin1 encocing needed in order to be able to read special chars like "µ"
        print(table)

        pearson = table.corr(method="pearson")

        pearson = pearson.iat[0, 1] #as it spits out a correlation matrix between all columns in a dataframe, again as datafram itself, I need to pick the value out of the datafram, then correlates the two columns with each other
        print(pearson)

        pearsons.append(pearson)

    print(names)
    print(pearsons)

    #create the final output table

    data = {"filenames": filenames,
             "pearson coefficient": pearsons}

    print(data)

    df = pd.DataFrame(data)

    # calculate the median
    median = df["pearson coefficient"].median()

    print(df)
    print("The median is: {}.".format(median))

    savepath = os.path.join(root_path, "Pearsons.csv")
    df.to_csv(savepath)

    # # visualize as histogram with pandas
    # hist = df.hist(column='pearson coefficient', bins=10)
    # plt.hist
    # plt.show()

    # visualize as histogram with seaborn
    sns.set_style("white")
    hist = sns.displot(x='pearson coefficient', data=data, kde=True, color="#808080", binwidth=0.1, binrange=(-1, 1), height=8.27, aspect=11.7/8.27) # height=8.27, aspect=11.7/8.27 so stellt man die Größe beim displor ein, bei anderene gehts über figsize; das sind die Werte für A4 in inches
    # kde = kernel density estimation distribution aka the line over te histogram, length measures in inch!!
    plt.title('Spatial Correlation of Bax and Bak in the ring', y=0.97, fontsize=24) # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel('Pearson Correlation Coefficients', fontsize=24)
    plt.ylabel('Count', fontsize=24)
    plt.tight_layout() #damits keine legends abschneidet und so
    # add the vertical line for the median
    plt.axvline(x=median, ymax=0.95, color='black', lw=2.5) #ymax makes the line not go into the title, the variable median comes from above
    plt.hist
    plt.show()



if __name__ == '__main__':
    main()