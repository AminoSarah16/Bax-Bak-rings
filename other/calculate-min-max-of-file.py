'''

Opens .obf files and saves min and max values as csv.

The OBF file format originates from the Department of NanoBiophotonics
of the Max Planck Institute for Biophysical Chemistry in Göttingen, Germany. A specification can be found at
https://github.com/AbberiorInstruments/ImspectorDocs/blob/master/docs/fileformat.rst

Opening and converting to numpy array is done via the obf support package by Jan Keller-Findeisen (https://github.com/jkfindeisen)
https://github.com/jkfindeisen/python-mix/tree/main/obf
[Pure Python read only support for OBF files.  This implementation is similar to the File and Stack API of specpy
(https://pypi.org/project/specpy/). Can also read MSR files (the OBF part of it).]

Include Jan's obf_support.py in your project and import it into the code with "import obf_support".

Sarah Schweighofer, August 2022, Göttingen, Max Planck Institute for Multidisciplinary sciences.
'''

from utils import obf_support
from tkinter import filedialog
import os
import numpy
import pandas as pd


def main():
    # let the user choose the folder containing the images to be converted
    root_path = filedialog.askdirectory()  # prompts user to choose directory. From tkinter

    # prints out the number of files in the selected folder with the .obf file format
    file_format = ".obf"
    filenames = [filename for filename in sorted(os.listdir(root_path)) if filename.endswith(file_format)]
    print("There are {} files with this format.".format(len(filenames)))
    if not filenames:  # pythonic for if a list is empty
        print("There are no files with this format.")

    # ask user which what part in the name we are looking for:
    # namepart = input("Please enter the namepart you are looking for - case-sensitive (eg STED, Confocal..). If all stacks are wanted press enter: ")
    namepart = ""
    # create a subfolder where the converted images would be saved
    result_path = os.path.join(root_path, 'results')
    if not os.path.isdir(result_path):
        os.makedirs(result_path)


    Bax_maxes = []  # empty list for all mins and maxes, all of these are gonna be our columns in the final csv.
    Bak_maxes = []
    Bax_mins = []
    Bak_mins = []

    # go through the list of files
    for filename in filenames:
        print(filename)
        file_path = os.path.join(root_path, filename)
        current_obf_file = obf_support.File(file_path)  # this is where Jan does the magic of opening

        # extract the stacks according o the defined name part
        wanted_stacks = [stack for stack in current_obf_file.stacks if namepart in stack.name]
        print('The measurement contains {} {} channels.'.format(len(wanted_stacks), namepart))

        # now load all the wanted stacks, turn them into numpy arrays and get the exact name.
        for stack in wanted_stacks:
            array = stack.data  # this is where Jan does the magic of converting obf to numpy
            array = numpy.transpose(array)  # need to transpose to have in the original orientation
            stackname = stack.name

            # calculate and save the min/max values
            if "Bax" in stackname:
                Bax_max = numpy.amax(array)
                Bax_min = numpy.amin(array)

                Bax_maxes.append(Bax_max)
                Bax_mins.append(Bax_min)

            if "Bak" in stackname:
                Bak_max = numpy.amax(array)
                Bak_min = numpy.amin(array)

                Bak_maxes.append(Bak_max)
                Bak_mins.append(Bak_min)

        # create the min/max output table

    data = {"filenames": filenames,
            "Bax max": Bax_maxes,
            "Bak max": Bak_maxes,
            "Bax min": Bax_mins,
            "Bak min": Bak_mins}

    print(data)

    df = pd.DataFrame(data)

    savepath = os.path.join(result_path, "mins_maxes_from-obf.csv")
    df.to_csv(savepath)


if __name__ == '__main__':
    main()

