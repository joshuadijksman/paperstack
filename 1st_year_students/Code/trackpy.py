import matplotlib as mpl
import matplotlib.pyplot as plt

# change the following to %matplotlib notebook for interactive plotting
# matplotlib inline

# Optionally, tweak styles.
mpl.rc('figure',  figsize=(10, 5))
mpl.rc('image', cmap='gray')

import numpy as np
import pandas as pd
from pandas import DataFrame, Series  # for convenience

import pims
import trackpy as tp

test=pims.open('C:/Users/salad/Documents/PROJECT METINGTJE/papiermetingen/1-1-M.avi')
test


@pims.pipeline
def gray(image):
    return image[:, :, 1]  # Take just the green channel

frames = gray(pims.open('C:/Users/salad/Documents/PROJECT METINGTJE/papiermetingen/1-1-M.avi'))

plt.imshow(frames[0])

f = tp.locate(frames[0], 11, invert=True)