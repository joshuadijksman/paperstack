from pathlib import Path  
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np

inputfolder = Path(r"Z:")
filename = "80dpaper_8_72mm"

file_path = inputfolder / f"{filename}.csv"
data_current = pd.read_csv(file_path)

time = data_current.iloc[:, 0].to_numpy(dtype=float).copy()
voltage = data_current.iloc[:, 1].to_numpy(dtype=float).copy()

plt.plot(time, voltage)
plt.yscale('log')
plt.show()