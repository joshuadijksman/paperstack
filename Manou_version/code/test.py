import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
from scipy.stats import chi2
import math as math
from scipy.ndimage import gaussian_filter1d
from pathlib import Path
import selfmadefunctions
import importlib
importlib.reload(selfmadefunctions)

# Author: Manou Liesker, Student number: 15250946

NETWORK_FOLDER = Path(rf"Z:\Clean_Data\Data_Manou_Maria_Clean")
T3_Thicknesses = [0, 20, 40, 60, 80, 100, 140, 180, 200, 250, 300, 350, 400, 500]
V_Thicknesses = [0, 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 25, 30, 35, 40]

T_COR, T_COR_err = selfmadefunctions.calulate_COR(NETWORK_FOLDER, 'T3', T3_Thicknesses, 3, False) # (networkfolder, filebegin, thicknesslist, repetitions, Plot)
V_COR, V_COR_err = selfmadefunctions.calulate_COR(NETWORK_FOLDER, 'V', V_Thicknesses, 3, False)

plt.errorbar(T3_Thicknesses, T_COR, yerr= T_COR_err, fmt = 'o', label = "Measurements day 1")
plt.errorbar(V_Thicknesses, V_COR, yerr= V_COR_err, fmt = 'o', label = "Measurements day 2")
plt.title('The COR as a function of substrate thickness')
plt.xlabel('Thickness (paper layers)')
plt.ylabel('Coefficient of restitution')
plt.legend()
plt.show()
