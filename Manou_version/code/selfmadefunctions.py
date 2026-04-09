import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
from scipy.stats import chi2
import math as math
from scipy.ndimage import gaussian_filter1d
from pathlib import Path

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

def databewerken(networkfolder, filename, thickness, Plot):
  
    # tweak these
    N_points = 60
    leniency = 5
    y_err = 1

    # maybe tweak these for better results
    sigma = 2
    
    # dont tweak these
    Total_first_N_points = 0
    delete_first_elements = 0
    laagtepunt_1 = 0
    laagtepunt_2 = 0
    

    file_path = networkfolder / f"{filename}.csv"
    data_current =  pd.read_csv(file_path)

    y_points = data_current.iloc[:, 1] #Camera hangt scheef, dus omdraaien en lezen van de x-coordinaten.
    frames = data_current.iloc[:, 0]

    # ervoor zorgen dat eerste rechte data wordt afgeknipt
    for i in range(N_points):           # gemiddelde nemen van eerste N punten
        Total_first_N_points += y_points[i]
    average_first_N_points = Total_first_N_points / N_points # wordt genomen als "drop height"
    
    while abs(y_points[delete_first_elements] - average_first_N_points) < leniency:        # wachten tot een punt te ver van het gemiddelde van de eerste N af zit. AKA wanneer valt het?
        delete_first_elements += 1

    afgeknipt_y = y_points[delete_first_elements:]     # Deze punten afknippen
    afgeknipt_frame = frames[delete_first_elements:]   # Deze punten afknippen
    smoothed = gaussian_filter1d(afgeknipt_y, sigma = sigma)     # hier een gaussisch filter overheen halen, zodat alle punten mooi zijn

    for i in range(len(smoothed) - 1):
        if smoothed[i] < smoothed[i + 1] and smoothed[i] < smoothed[i-1]:      # van deze data de eerste twee minimums vinden en het frame hiervan onthouden
            if laagtepunt_1 == 0:
                laagtepunt_1 = i + 2
            else:
                laagtepunt_2 = i - 2
                break
    
    y = [0, average_first_N_points]
    x1 = [laagtepunt_1 + delete_first_elements, laagtepunt_1 + delete_first_elements]
    x2 = [laagtepunt_2 + delete_first_elements, laagtepunt_2 + delete_first_elements]

    frame_bounce = afgeknipt_frame[laagtepunt_1:laagtepunt_2]
    y_bounce = afgeknipt_y[laagtepunt_1:laagtepunt_2]

    if Plot:
        fig, ax = plt.subplots(1, 3, figsize=(18, 5))
        
        print(f'Thickness = {thickness}')
        print(f"The first {delete_first_elements} frames are deleted, after that the ball drops.")
        print(f'The ball is released at y = {average_first_N_points} pixels.')
        print(f'The minima are located at {laagtepunt_1} frames and {laagtepunt_2} frames.')

        # Grafiek 1
        ax[0].errorbar(frames, y_points, yerr=y_err)
        ax[0].plot(
            [delete_first_elements - 200, delete_first_elements + 200],
            [average_first_N_points, average_first_N_points],
            'b--'
        )
        ax[0].plot(
            [delete_first_elements, delete_first_elements],
            [average_first_N_points + 100, 0],
            'r--'
        )
        ax[0].set_xlabel('Time [frames]')
        ax[0].set_ylabel('Height [pixels]')
        ax[0].set_title('Beginning Data')

        # Grafiek 2
        ax[1].errorbar(afgeknipt_frame, afgeknipt_y, yerr=y_err)
        ax[1].plot(x1, y, 'r--')
        ax[1].plot(x2, y, 'r--')
        ax[1].set_xlabel('Time [frames]')
        ax[1].set_ylabel('Height [pixels]')
        ax[1].set_title('Data from moment of release')

        # Grafiek 3
        ax[2].errorbar(
            frame_bounce,
            y_bounce,
            yerr=y_err,
            markersize=2,
            fmt='o'
        )
        ax[2].set_xlabel('Time [frames]')
        ax[2].set_ylabel('Height [pixels]')
        ax[2].set_title('Isolated first Bounce')

        fig.suptitle(f'Measurement on thickness {thickness}, filename = {filename}')
        plt.tight_layout()
        plt.show()

    return average_first_N_points, frame_bounce, y_bounce  #Returns the drop height en the trajectory of the relevant bounce.

def parabola_fit(frames, y_points, Plot, fit_report):

    def fit_function(t, a, t_0, b):
        return a * (t - t_0)**2 + b

    calibration_model = Model(fit_function)
    fit_result = calibration_model.fit(y_points, t=frames, a=20, t_0=70, b=200, weights=1)
    bounce_height = fit_result.params['b'].value

    if fit_report:
        print(fit_result.fit_report())

    if Plot:
        fit_y = fit_result.best_fit
        residuals = y_points - fit_y
        rmse = np.sqrt(np.mean(residuals**2))

        fig, (ax_res, ax_main) = plt.subplots(
            2, 1, figsize=(5, 4), sharex=True,
            gridspec_kw={'height_ratios': [1, 3]}
        )

        print(f'bounce height = {bounce_height} pixels')
        print(f'RMSE = {rmse:.2f} pixels')

        # residual plot
        ax_res.axhline(0, linestyle='--')
        ax_res.errorbar(frames, residuals, yerr = 1, fmt = 'o', markersize=3)
        ax_res.set_ylabel('Residual')
        ax_res.set_title(f'Fit quality (RMSE = {rmse:.2f} px)')

        # main plot
        ax_main.errorbar(frames, y_points, label='Data', yerr=1, fmt='None', markersize=1, zorder=2)
        ax_main.plot(frames, fit_y, label='Fit', zorder=1)
        ax_main.plot([min(frames), max(frames)], [bounce_height, bounce_height],
                     label='Bounce height', linestyle='--')

        ax_main.set_xlabel('Frames (t)')
        ax_main.set_ylabel('y')
        ax_main.set_title('Data and fit')
        ax_main.legend()

        plt.tight_layout()
        plt.show()

    return bounce_height