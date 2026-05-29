from pathlib import Path  
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
from lmfit import Model


def sine_fit(x_points, y_points, error):

    def fit_function(x, a, b, c, phase):
        return a*np.sin(2*np.pi*x/b - phase) + c

    calibration_model = Model(fit_function)   
    calibration_model.set_param_hint('a', min = 0.01, max = 0.03)
    calibration_model.set_param_hint('b', min = 0.01, max = 0.03)
    calibration_model.set_param_hint('c', min = 0.5, max = 0.54)
    calibration_model.set_param_hint('phase')

    fit_result = calibration_model.fit(y_points, x=x_points, a=0.01, b=0.02, c=0.53, phase = 0, weights=1/error)
    a = fit_result.params['a'].value
    b = fit_result.params['b'].value



    print(fit_result.fit_report())


    fit_y = fit_result.best_fit
    residuals = y_points - fit_y
    rmse = np.sqrt(np.mean(residuals**2))

    fig, (ax_res, ax_main) = plt.subplots(
        2, 1, figsize=(5, 4), sharex=True,
        gridspec_kw={'height_ratios': [1, 3]}
    )

    print(f'bounce height = {b} pixels')
    print(f'RMSE = {rmse:.2f} pixels')

    # residual plot
    ax_res.axhline(0, linestyle='--')
    ax_res.errorbar(x_points, residuals, yerr = error, fmt = 'o', markersize=3)
    ax_res.set_ylabel('Residual')
    ax_res.set_title(f'Fit quality (RMSE = {rmse:.2f} px)')

    # main plot
    ax_main.plot(x_points, y_points, label='Data', markersize=1, zorder=1)
    ax_main.plot(x_points, fit_y, label='Fit', zorder=2)


    ax_main.set_xlabel('Amount of paper layers')
    ax_main.set_ylabel('Stack height (mm)')
    ax_main.set_title('Data and fit')
    ax_main.legend()

    plt.tight_layout()
    plt.show()

    return fit_y



inputfolder = Path(r"Z:\Clean_Data\Data_Manou_Thesis_Clean\Force_measurements\test_and_0")
filename = "80dpaper_13_15mm"

file_path = inputfolder / f"{filename}.csv"
data_current = pd.read_csv(file_path)

time = data_current.iloc[:, 0].to_list()
voltage = data_current.iloc[:, 1].to_list()


# Find the index where x = 35
stop_index = time.index(1)

# Keep data up to (but not including) the stop_index
time_trimmed = time[:stop_index]
voltage_trimmed = voltage[:stop_index]



sine_fit(time_trimmed, voltage_trimmed, 0.00001)




plt.plot(time, voltage)
plt.yscale('log')
plt.show()