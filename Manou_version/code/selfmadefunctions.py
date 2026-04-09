import math
import numpy as np
from pathlib import Path
import pandas as pd
import csv

# The camera from the measurements of Maria and Manou was turned 90 degrees, 
# making positive movement in X equal negative vertical movement. 
# This function creates a new csv file that's easier to work with. 
#(positive Y movement = positive vertical movement and y=0 is the point at wich the ball touches the floor.)
#This also turns the data from mqa into a csv file, like the other ones.

def coordinate_swap(filename, folder):    # folder = metingen_0_40 of metingen_0_500
 
    NETWORK_FOLDER = Path(rf"Z:\Data_Manou_Maria\{folder}")

    file_path = NETWORK_FOLDER / f"{filename}.mqa"
    data_current =  pd.read_csv(file_path, sep='\t')

    omgedraaid_y_current = data_current.iloc[:, 2] #Camera hangt scheef, dus omdraaien en lezen van de x-coordinaten.
    frame_current = data_current.iloc[:, 0]
    laagste_y_current = max(omgedraaid_y_current)
    
    y_current = []
    for oy in omgedraaid_y_current:
        y = laagste_y_current - oy
        y_current.append(y)

    cleaned_file = pd.DataFrame(
    {'Frame': frame_current,
     'Y': y_current,
    })

    cleaned_file.to_csv(f"{filename}_clean.csv", index = False)


coordinate_swap("V_d0_1", "metingen_0_40")

