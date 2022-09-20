'''
This program opens a folder with subfolders with csv files.
Then calculates the Pearson correlation coefficient.
Then shifts the two correlated series one position and adds the lowest value on top, then calculates the Pearson again and so on.
Spits out a csv and curve with the Pearsons plotted in y and the deltaD plotted in x.
Göttingen, August 2022, Sarah Vanessa Schweighofer, MPI-NAT
'''


import os
from matplotlib import pyplot as plt
import seaborn as sns
from utils.utils import *


def main():
    names = []  # empty list for all filenames, both of these are gonna be our columns in the final csv.

    # let the user choose the folder containing the images to be converted
    root_path = filedialog.askdirectory()  # prompts user to choose directory. From tkinter

    # prints out the number of files in the selected folder with the .tiff file format
    file_ending = "replicate.csv"
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

    for filename in filenames:
        pearsons = []  # empty list for alle the pearson coefficients
        print(filename)
        names.append(filename)
        file_path = os.path.join(root_path, filename)
        table = pd.read_csv(file_path, encoding='latin1')  # latin1 encocing needed in order to be able to read special chars like "µ"
        print(table)

        Bax = table["Bax Intensities"]  # in order to calculate the mean of each column
        print(len(Bax))
        Bak = table["Bak Intensities"]
        lengths = table["Âµm"]

        pearson = Bax.corr(Bak, method="pearson")  # easier way to correlate two specifi series with each other!
        print(pearson)

        pearsons.append(pearson)

        pearson = Bak.corr(Bax, method="pearson")
        print(pearson)

        ################ shift the Bax series one down and fill top with last value until reached top again#########
        for i in range(len(Bax)-1): ## -1 damit der das letzte nicht macht, weil das wäre dann wieder glecih wie die Ursprunswerte
            # convert Series to numpy array and select last, which is needed to fill the series from the top:
            last = Bax.values[-1]
            print(last)
            Bax = Bax.shift(1, fill_value=last)  # shifts the series one down
            print(Bax)

            pearson = Bax.corr(Bak, method="pearson")
            print(pearson)
            pearsons.append(pearson)
        print(pearsons)
        ############################################################################################################


        ##### create and save a new csv with length and pearson ######
        data = {"delta d": lengths,
               "pearson": pearsons}
        print(data)
        df = pd.DataFrame(data)

        new_filename = filename[:-34]
        print(new_filename)
        output_file = os.path.join(root_path, new_filename + "-pearsons_delta_d.csv")
        print(output_file)
        df.to_csv(output_file)
        ################################################################################################################

        #################### calcualte some values, always correlated to their delta d an write to an extra csv ###############################
        # make numpy arrays out of the lists in order to do calculations
        pearson_arr = np.array(pearsons)
        lengths = np.array(lengths)

        #calculate the mean
        mean = pearson_arr.mean()
        print(mean)

        # calculate the maximum
        max = pearson_arr.max()
        print(max)

        # calculate the minimum
        min = pearson_arr.min()
        print(min)

        #calculate all the local minima
        local_minima_locations = detect_local_minima(pearson_arr)  ## see utils for function
        print(local_minima_locations)
        print(lengths[local_minima_locations]) ## find the same indices in the length array, which then correspond to the delta d value where this locacl minimum is hit
        first_local_mimimum = local_minima_locations[0][0]
        print(first_local_mimimum)
        print(lengths[first_local_mimimum])

        #calculate where the curve hits zero the first time
        hitting_zero = np.where(pearson_arr <= 0)
        print(hitting_zero)
        first_hitting_zero = hitting_zero[0][0] # I only want the first value of the array (and for some reason the array is a 2D array, that's why I have to do [0] twice...
        print(first_hitting_zero)
        print(pearson_arr[first_hitting_zero])
        print(lengths[first_hitting_zero])

        #################################################################################################


        ####################### plot all the pearsons against delta D ##################
        plot = sns.lineplot(x=lengths, y=pearsons, color="#808080")
        # Größe des finalen Plots
        plot.figure.set_figwidth(11.7)
        plot.figure.set_figheight(8.27)

        plot.set_ylim(-1, 1)
        plt.title('spatial correlation', fontsize=24)  # y is a relative coordinate system. 1 is at the very top, 0.9 a little below and so on
        plt.xlabel('Delta d [µm]', fontsize=20) ##TODO: insert \u0394 as delta symbol
        plt.ylabel('Pearson', fontsize=20)
        # plt.legend(fontsize=16, title_fontsize=20)


        #add mean line
        plt.axhline(y=mean, color='#80c2d9', linestyle='-')


        #### add first hitting zero point to graphic ############
        plt.scatter(lengths[first_hitting_zero], pearson_arr[first_hitting_zero], s=56, marker="o", c="green")

        #### add first local minimum to graphic ############
        plt.scatter(lengths[first_local_mimimum], pearson_arr[first_local_mimimum], s=56, marker="o", c="black")




        # Zeigs her
        plt.plot()

        savepath = os.path.join(root_path, new_filename + "_pearsons_delta_d.png")
        plt.savefig(savepath)
        # plt.show()
        plt.close()
        #####################################################################################


if __name__ == '__main__':
    main()