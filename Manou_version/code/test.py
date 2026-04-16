import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
import math as math
from scipy.ndimage import gaussian_filter1d

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

        ax_main.set_xlabel('Time (frames)')
        ax_main.set_ylabel('Height (pixels)')
        ax_main.set_title('Data and fit')
        ax_main.legend()

        plt.tight_layout()
        plt.show()
    return bounce_height

def COR_calculator_general(inputfolder, variable_type, variable_value, filename, Find_Plot, Fit_Plot, Fit_Report):
    # tweak these

    leniency = 5
    y_err = 1

    # maybe tweak these for better results
    sigma = 2
    
    # dont tweak these

    delete_first_elements = 1
    laagtepunt_1 = 0
    laagtepunt_2 = 0

    file_path = inputfolder / f"{filename}.csv"
    data_current =  pd.read_csv(file_path)

    y_points = data_current.iloc[:, 1] 
    frames = data_current.iloc[:, 0]

    nan_mask = np.isnan(y_points)
    not_nan = ~nan_mask

    y_points[nan_mask] = np.interp(np.flatnonzero(nan_mask),np.flatnonzero(not_nan),y_points[not_nan])

    
    while abs(y_points[delete_first_elements] - y_points[delete_first_elements - 1]) < leniency:
            delete_first_elements += 1

    delete_first_elements -= 30 # dertig frames terugspoelen, tot voor hij viel.
    drop_height = y_points[delete_first_elements]
    
    afgeknipt_y = y_points[delete_first_elements:].to_numpy(dtype=float)
    afgeknipt_frame = frames[delete_first_elements:].to_numpy(dtype=float)

    mask = ~np.isnan(afgeknipt_y)
    afgeknipt_y = afgeknipt_y[mask]
    afgeknipt_frame = afgeknipt_frame[mask]

    smoothed = gaussian_filter1d(afgeknipt_y, sigma=sigma)



    for i in range(len(smoothed) - 1):
        if smoothed[i] < smoothed[i + 1] and smoothed[i] < smoothed[i-1]:      # van deze data de eerste twee minimums vinden en het frame hiervan onthouden
            if laagtepunt_1 == 0:
                laagtepunt_1 = i + 1
            else:
                laagtepunt_2 = i - 2
                break
        
    
    y = [0, drop_height]
    x1 = [laagtepunt_1 + delete_first_elements, laagtepunt_1 + delete_first_elements]
    x2 = [laagtepunt_2 + delete_first_elements, laagtepunt_2 + delete_first_elements]

    frame_bounce = afgeknipt_frame[laagtepunt_1:laagtepunt_2]
    y_bounce = afgeknipt_y[laagtepunt_1:laagtepunt_2]

    if Find_Plot:
        fig, ax = plt.subplots(1, 3, figsize=(18, 5))
        
        print(f'{variable_type} = {variable_value}')
        print(f"The first {delete_first_elements} frames are deleted, after that the ball drops.")
        print(f'The ball is released at y = {drop_height} pixels.')
        print(f'The minima are located at {laagtepunt_1} frames and {laagtepunt_2} frames.')

        # Grafiek 1
        ax[0].errorbar(frames, y_points, yerr=y_err)
        ax[0].plot(
            [delete_first_elements - 200, delete_first_elements + 200],
            [drop_height, drop_height],
            'b--'
        )
        ax[0].plot(
            [delete_first_elements, delete_first_elements],
            [drop_height + 100, 0],
            'r--'
        )
        ax[0].set_xlabel('Time (frames)')
        ax[0].set_ylabel('Height [pixels]')
        ax[0].set_title('Beginning Data')

        # Grafiek 2
        ax[1].errorbar(afgeknipt_frame, afgeknipt_y, yerr=y_err)
        ax[1].plot(x1, y, 'r--')
        ax[1].plot(x2, y, 'r--')
        ax[1].set_xlabel('Time (frames)')
        ax[1].set_ylabel('Height (pixels)')
        ax[1].set_title('Data from moment of release')

        # Grafiek 3
        ax[2].errorbar(
            frame_bounce,
            y_bounce,
            yerr=y_err,
            markersize=2,
            fmt='o'
        )
        ax[2].set_xlabel('Time (frames)')
        ax[2].set_ylabel('Height (pixels)')
        ax[2].set_title('Isolated first Bounce')

        fig.suptitle(f'Measurement on {variable_type} {variable_value}, filename = {filename}')
        plt.tight_layout()
        plt.show()

        bounce_height = parabola_fit(frame_bounce, y_bounce, Fit_Plot, Fit_Report)
        COR = np.sqrt(bounce_height/drop_height)

        return COR