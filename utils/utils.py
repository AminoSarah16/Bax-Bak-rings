import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
import numpy as np
import pandas as pd
import scipy.ndimage.filters as filters
import scipy.ndimage.morphology as morphology

###### basic pandas funcionality to read a csv and make a dataframe out of it. file location is being asked via tkinter
def df_from_csv():
    file = filedialog.askopenfile()
    df = pd.read_csv(file, encoding='latin1')  # better already sort the csv manually before importing
    return df
#####################################################################################################################


###### basic pandas funcionality to read a xls and make a dataframe out of it. file location is being asked via tkinter
def df_from_xls():
    file = filedialog.askopenfile()
    df = pd.read_excel(file, encoding='latin1')  # better already sort the csv manually before importing
    return df
#####################################################################################################################


def detect_local_minima(arr):
    # https://stackoverflow.com/questions/3684484/peak-detection-in-a-2d-array/3689710#3689710
    """
    Takes an array and detects the troughs using the local maximum filter.
    Returns a boolean mask of the troughs (i.e. 1 when
    the pixel's value is the neighborhood maximum, 0 otherwise)
    """
    # define an connected neighborhood
    # http://www.scipy.org/doc/api_docs/SciPy.ndimage.morphology.html#generate_binary_structure
    neighborhood = morphology.generate_binary_structure(len(arr.shape),2)
    # apply the local minimum filter; all locations of minimum value
    # in their neighborhood are set to 1
    # http://www.scipy.org/doc/api_docs/SciPy.ndimage.filters.html#minimum_filter
    local_min = (filters.minimum_filter(arr, footprint=neighborhood)==arr)
    # local_min is a mask that contains the peaks we are
    # looking for, but also the background.
    # In order to isolate the peaks we must remove the background from the mask.
    #
    # we create the mask of the background
    background = (arr==0)
    #
    # a little technicality: we must erode the background in order to
    # successfully subtract it from local_min, otherwise a line will
    # appear along the background border (artifact of the local minimum filter)
    # http://www.scipy.org/doc/api_docs/SciPy.ndimage.morphology.html#binary_erosion
    eroded_background = morphology.binary_erosion(
        background, structure=neighborhood, border_value=1)
    #
    # we obtain the final mask, containing only peaks,
    # by removing the background from the local_min mask
    detected_minima = local_min ^ eroded_background
    return np.where(detected_minima)


def rolling_mean(window_size, starting_value, x_series, y_series, max_x_value, roll_factor):
    '''
    :param window_size: how big is the window sliding over the dataset
    :param starting_value: where does the sliding start
    :param x_series: series of pandas dataframe containing the independent x values
    :param y_series: series of pandas dataframe containing the dependent y values
    :param max_x_value: where should the while loop stop, eg 100% Bax content or maximal ring length etc
    :param roll_factor:in which increments should the window slide over the data
    :return: rollmeans: the means for each slided window and rollmean_x: the according x values
    '''
    # x is the independent, y the dependent variable
    x_slices = []
    x_slice_indices = []
    rollmeans = []
    rollmean_x = []

    # schleife mit stepsize
    i = starting_value
    while i < max_x_value:  # 100 is the maximal possible amount
        # find all the x values in a certain window of the series (= slice)
        x_slice = x_series[(x_series >= i) & (x_series < (i + window_size))].sort_values()  # find all the values between x and (x plus stepsize) and sort the list ascending
        print(i)
        print(x_slice)
        x_slices.append(x_slice)

        # find the index values of the x values in the slice
        slice_index = x_slice.index
        x_slice_indices.append(slice_index)
        print(slice_index)

        # find the according y values at the given indices
        y_values = y_series.iloc[slice_index]
        print(y_values)

        # calculate the y mean in each y slice
        mean = y_values.mean()
        rollmeans.append(mean)

        # create column with adequate window size
        rollmean_x.append(i)

        i += window_size / roll_factor  # increase i with window size durch 2 oder 4 etc um wirklich nen rolling zu haben!!!

    print(x_slices)
    print(x_slice_indices)
    print(rollmeans)
    print(len(rollmeans))
    print(len(rollmean_x))

    return rollmeans, rollmean_x
