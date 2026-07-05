from pathlib import Path  
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
from lmfit import Model




inputfolder = Path(r"Z:\Clean_Data\Data_Manou_Thesis_Clean\Force_measurements\test_and_0")
filename = "80dpaper_13_43mm"

file_path = inputfolder / f"{filename}.csv"
data_current = pd.read_csv(file_path)

time = data_current.iloc[:, 0].to_list()
voltage = data_current.iloc[:, 1].to_list()


plt.plot(time, voltage)
plt.title(filename)
plt.yscale('log')
plt.xlabel('time (s)')
plt.ylabel('voltage (V)')
plt.ylabel('')
plt.show()