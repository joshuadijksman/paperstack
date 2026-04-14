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


A4_Thickness, A4_COR, A4_COR_err = selfmadefunctions.read_saladin_data("A4_sanitized_data.csv", True, 1)
A5B_Thickness, A5B_COR, A5B_COR_err = selfmadefunctions.read_saladin_data("A5_B_sanitized_data.csv", True, 1)
A5O_Thickness, A5O_COR, A5O_COR_err = selfmadefunctions.read_saladin_data("A5_O_sanitized_data.csv", True, 1)

plt.errorbar(A4_Thickness, A4_COR, yerr = A4_COR_err, fmt = 'o', label = 'A4 Sheets')
plt.errorbar(A5B_Thickness, A5B_COR, yerr = A5B_COR_err, fmt = 'o', label = 'A5_B Sheets')
plt.errorbar(A5O_Thickness, A5O_COR, yerr = A5O_COR_err, fmt = 'o', label = 'A5_O Sheets')
plt.title("Saladin's Data combined")
plt.xlabel("Thickness (Paper sheets)")
plt.ylabel("Coefficient of Restitution")
plt.legend()
plt.show()

