import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model


# Author: Manou Liesker. Student number: 15250946

############################ General functions that should work on most files ##############################


# Fits a parabola to an isolated bounce
# Input: Frames and y-points of an isolated bounce (So that you only have a parabola), Plot (True or False), fit_report (True or False)
# Output: The top of the parabola (the bounce height). If Plot and fit_report are True, it plots the fit and prints the fit report 
def linear_fit(x_points, y_points, error):

    def fit_function(x, a, b):
        return a * x + b

    calibration_model = Model(fit_function)   
    calibration_model.set_param_hint('a', min= 0, max = 1)
    calibration_model.set_param_hint('b', min=-0.1, max = 0.1)

    fit_result = calibration_model.fit(y_points, x=x_points, a=0.1, b=y_points[0], weights=1/error)
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
    ax_main.errorbar(x_points, y_points, label='Data', yerr=error, fmt='None', markersize=1, zorder=2)
    ax_main.plot(x_points, fit_y, label='Fit', zorder=1)


    ax_main.set_xlabel('Amount of paper layers')
    ax_main.set_ylabel('Stack height (mm)')
    ax_main.set_title('Data and fit')
    ax_main.legend()

    plt.tight_layout()
    plt.show()

    return a, b



layers = []
measured_mm = [0.01, 0.58, 1.16, 1.74, 2.32, 2.92, 3.46, 4.04, 4.62, 5.16, 5.72, 6.30, 6.88, 7.43, 8.00, 8.54, 9.16, 9.69, 10.25, 10.81, 11.41]
papermm = []

for i in range(0,105, 5):
    layers.append(i)

for l in layers:
    papermm.append(0.1 * l)


linear_fit(layers, measured_mm, 0.02)




plt.errorbar(layers, measured_mm, fmt = 'o', label = 'Measured thickness')
plt.errorbar(layers, papermm, fmt = 'o', label = 'paper thickness * paper layers')
plt.legend()
plt.xlabel("Amount of paper layers")
plt.ylabel("Stack height (mm)")
plt.show()


