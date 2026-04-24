from fileinput import filename

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
from scipy.ndimage import gaussian_filter1d
from pathlib import Path
import cv2

# Author: Manou Liesker. Student number: 15250946

############################ General functions that should work on most files ##############################


# Fits a parabola to an isolated bounce
# Input: Frames and y-points of an isolated bounce (So that you only have a parabola), Plot (True or False), fit_report (True or False)
# Output: The top of the parabola (the bounce height). If Plot and fit_report are True, it plots the fit and prints the fit report 
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

def track_video(treshold, video_inputfolder, video_outputfolder, csv_outputfolder, filename, show, save_video, save_csv, BOTTOM_CROP):
    input_path = video_inputfolder / filename

    cap = cv2.VideoCapture(input_path)

    if save_video:
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 30

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        output_path = str(video_outputfolder / f"{Path(filename).stem}_tracked.avi")
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=True)

    x_points = []
    y_points = []
    frame_numbers = []


    threshold_value = treshold
    min_area = 5
    max_area = 100
    min_circularity = 0.4   # raise this if you want stricter circle-like blobs

    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = gray[:gray.shape[0] - BOTTOM_CROP, :]
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        frame = frame[:frame.shape[0] - BOTTOM_CROP, :]

        _, mask = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
        

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        overlay = frame.copy()
        cv2.drawContours(overlay, contours, -1, (255, 0, 0), -1)   # filled blue
        alpha = 0.8  # transparency: 0 = invisible, 1 = solid
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        valid_contours = []
        contour_scores = []

        for cnt in contours:
            area = cv2.contourArea(cnt)

            # First: size check
            if not (min_area <= area <= max_area):
                continue

            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0:
                continue

            # Second: circularity check
            circularity = 4 * np.pi * area / (perimeter ** 2)

            if circularity >= min_circularity:
                valid_contours.append(cnt)
                contour_scores.append(circularity)

        # Blue transparent fill for ONLY the contours that pass the tracking filter


        frame_numbers.append(frame_idx)

        if valid_contours:
            # Pick the most circular contour, not the biggest one
            best_idx = np.argmax(contour_scores)
            cnt = valid_contours[best_idx]

            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = M["m10"] / M["m00"]
                cy = M["m01"] / M["m00"]

                x_points.append(cx)
                y_points.append(cy)

                # Green outline of the actually selected contour
                cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
                cv2.circle(frame, (int(cx), int(cy)), 5, (0, 0, 255), -1)
            else:
                x_points.append(np.nan)
                y_points.append(np.nan)
        else:
            x_points.append(np.nan)
            y_points.append(np.nan)

        if show:
            cv2.imshow("tracking", frame)
            cv2.imshow("mask", mask)
            if cv2.waitKey(30) == 27:
                break

        if save_video:
            out.write(frame)

        frame_idx += 1

    cap.release()

    if save_video:
        out.release()
        print("Saved video to:", output_path)

    if save_csv:
        lowest_y = np.nanmax(y_points)
        new_points = []

        for y in y_points:
            new_y = lowest_y - y if not np.isnan(y) else np.nan
            new_points.append(new_y)

        cleaned_file = pd.DataFrame({
            'Frame': frame_numbers,
            'Y': new_points
        })

        csv_path = csv_outputfolder / f"{Path(filename).stem}_clean.csv"
        cleaned_file.to_csv(csv_path, index=False)
        print(f"Saved as {csv_path}")

    cv2.destroyAllWindows()

<<<<<<< HEAD
def track_video_2(treshold, video_inputfolder, video_outputfolder, csv_outputfolder,
                  filename, show, save_video, save_csv, BOTTOM_CROP):
    input_path = video_inputfolder / filename
    cap = cv2.VideoCapture(input_path)

    if save_video:
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 30
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) - BOTTOM_CROP
        output_path = str(video_outputfolder / f"{Path(filename).stem}_tracked.avi")
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=True)

    x_points = []
    y_points = []
    frame_numbers = []

    threshold_value = treshold
    min_area = 10
    max_area = 400
    alpha = 0.8

    prev_cx = None
    prev_cy = None
    prev_area = None
    has_locked_once = False
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = gray[:gray.shape[0] - BOTTOM_CROP, :]
        frame = frame[:frame.shape[0] - BOTTOM_CROP, :]
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        _, mask = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        candidates = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if not (min_area <= area <= max_area):
                continue

            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue

            cx = M["m10"] / M["m00"]
            cy = M["m01"] / M["m00"]

            candidates.append((cnt, cx, cy, area))

        overlay = frame.copy()
        cv2.drawContours(overlay, [c[0] for c in candidates], -1, (255, 0, 0), -1)
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        frame_numbers.append(frame_idx)

        if candidates:
            if not has_locked_once:
                cnt, cx, cy, area = min(candidates, key=lambda c: c[2])
                has_locked_once = True
            else:
                def candidate_score(c):
                    _, cx, cy, area = c

                    dist = np.hypot(cx - prev_cx, cy - prev_cy)
                    area_diff = abs(area - prev_area)

                    dist_norm = dist / 40
                    area_norm = area_diff / max(prev_area, 1)

                    return dist_norm + area_norm

                cnt, cx, cy, area = min(candidates, key=candidate_score)

            x_points.append(cx)
            y_points.append(cy)

            prev_cx = cx
            prev_cy = cy
            prev_area = area

            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
            cv2.circle(frame, (int(cx), int(cy)), 5, (0, 0, 255), -1)
        else:
            x_points.append(np.nan)
            y_points.append(np.nan)

        if show:
            cv2.imshow("tracking", frame)
            cv2.imshow("mask", mask)
            if cv2.waitKey(30) == 27:
                break

        if save_video:
            out.write(frame)

        frame_idx += 1

    cap.release()

    if save_video:
        out.release()
        print("Saved video to:", output_path)

    if save_csv:
        lowest_y = np.nanmax(y_points)
        new_points = []

        for y in y_points:
            new_y = lowest_y - y if not np.isnan(y) else np.nan
            new_points.append(new_y)

        cleaned_file = pd.DataFrame({
            'Frame': frame_numbers,
            'Y': new_points
        })

        csv_path = csv_outputfolder / f"{Path(filename).stem}_clean.csv"
        cleaned_file.to_csv(csv_path, index=False)
        print(f"Saved as {csv_path}")

    cv2.destroyAllWindows()

=======
>>>>>>> parent of 6472d89 (Added new video tracking software)
def COR_calculator_general(inputfolder, variable_type, variable_value, filename, Find_Plot, Fit_Plot, Fit_Report):
    # tweak these
    leniency = 5
    y_err = 1

    # maybe tweak these for better results
    nan_run_limit = 20
    outlier_limit = 80

    # dont tweak these
    delete_first_elements = 1
    laagtepunt_1 = 0
    laagtepunt_2 = 0

    file_path = inputfolder / f"{filename}.csv"
    data_current = pd.read_csv(file_path)

    y_points = data_current.iloc[:, 1].to_numpy(dtype=float).copy()
    frames = data_current.iloc[:, 0].to_numpy(dtype=float).copy()
    # ---- 0) First turn outliers into NaN ----
    if len(y_points) >= 3:
        extra_outlier_mask = np.zeros(len(y_points), dtype=bool)

        for i in range(1, len(y_points) - 1):
            if np.isnan(y_points[i - 1]) or np.isnan(y_points[i]) or np.isnan(y_points[i + 1]):
                continue

            if (
                abs(y_points[i] - y_points[i - 1]) >= outlier_limit
                and abs(y_points[i] - y_points[i + 1]) >= outlier_limit
            ):
                extra_outlier_mask[i] = True

        y_points[extra_outlier_mask] = np.nan

    # Save where values were originally NaN (including outliers turned into NaN)
    original_nan_mask = np.isnan(y_points)
    original_valid_mask = ~original_nan_mask

    # ---- 1) If there is a run of original NaNs, delete everything from there on ----
    nan_int = original_nan_mask.astype(int)
    kernel = np.ones(nan_run_limit, dtype=int)
    run_sums = np.convolve(nan_int, kernel, mode="valid")

    if np.any(run_sums == nan_run_limit):
        first_nan_run_start = np.flatnonzero(run_sums == nan_run_limit)[0]
        y_points = y_points[:first_nan_run_start]
        frames = frames[:first_nan_run_start]
        original_nan_mask = original_nan_mask[:first_nan_run_start]
        original_valid_mask = original_valid_mask[:first_nan_run_start]

    # Safety check
    if np.sum(original_valid_mask) < 2:
        print(f"Warning: not enough valid points in {filename}.")
        return np.nan

    # Interpolate NaNs
    y_points[original_nan_mask] = np.interp(
        np.flatnonzero(original_nan_mask),
        np.flatnonzero(original_valid_mask),
        y_points[original_valid_mask]
    )

    while (
        delete_first_elements < len(y_points)
        and abs(y_points[delete_first_elements] - y_points[delete_first_elements - 1]) < leniency
    ):
        delete_first_elements += 1

    delete_first_elements = max(0, delete_first_elements - 30)  # rewind 30 frames
    drop_height = y_points[delete_first_elements]

    afgeknipt_y = y_points[delete_first_elements:].copy()
    afgeknipt_frame = frames[delete_first_elements:].copy()
    afgeknipt_original_valid = original_valid_mask[delete_first_elements:]

    # Keep only up to the last originally valid datapoint
    if np.any(afgeknipt_original_valid):
        last_valid_idx = np.flatnonzero(afgeknipt_original_valid)[-1] + 1
        afgeknipt_y = afgeknipt_y[:last_valid_idx]
        afgeknipt_frame = afgeknipt_frame[:last_valid_idx]
        afgeknipt_original_valid = afgeknipt_original_valid[:last_valid_idx]
    else:
        print(f"Warning: no valid cropped points in {filename}.")
        return np.nan

    # Remove points that were originally NaN inside the cropped array
    afgeknipt_y = afgeknipt_y[afgeknipt_original_valid]
    afgeknipt_frame = afgeknipt_frame[afgeknipt_original_valid]

    if len(afgeknipt_y) < 5:
        print(f"Warning: too few points left after cleaning in {filename}.")
        return np.nan


    for i in range(2, len(afgeknipt_y) - 2):
        if afgeknipt_y[i] < drop_height / 2:
            if afgeknipt_y[i - 2] >= afgeknipt_y[i - 1] >= afgeknipt_y[i] <= afgeknipt_y[i + 1] <= afgeknipt_y[i + 2]:
                if laagtepunt_1 == 0:
                        laagtepunt_1 = i
                else:
                    if i - laagtepunt_1 > 5:
                        laagtepunt_2 = i
                        break

    if laagtepunt_2 == 0:
        laagtepunt_2 = len(afgeknipt_y) - 1
        print("Warning: only one minimum found, using last point as second minimum. This may cause errors in the COR calculation.")
    
    if laagtepunt_2 - laagtepunt_1 < 3: #Sometime happens when the frame is too short
        laagtepunt_1 -= 3
        print(f"Mask {filename}, tracking went wrong.")

    y = [0, drop_height]
    x1 = [afgeknipt_frame[laagtepunt_1], afgeknipt_frame[laagtepunt_1]]
    x2 = [afgeknipt_frame[laagtepunt_2], afgeknipt_frame[laagtepunt_2]]

    frame_bounce = afgeknipt_frame[laagtepunt_1:laagtepunt_2]
    y_bounce = afgeknipt_y[laagtepunt_1:laagtepunt_2]




    if Find_Plot:
        fig, ax = plt.subplots(1, 3, figsize=(18, 5))

        print(f'{variable_type} = {variable_value}')
        print(f"The first {delete_first_elements} frames are deleted, after that the ball drops.")
        print(f'The ball is released at y = {drop_height} pixels.')
        print(f'The minima are located at {laagtepunt_1} frames and {laagtepunt_2} frames.')

        ax[0].errorbar(frames, y_points, yerr=y_err, fmt='o', markersize=1)
        ax[0].plot(
            [delete_first_elements + frames[0] - 20, delete_first_elements + frames[0] + 20],
            [drop_height, drop_height],
            'b--'
        )
        ax[0].plot(
            [delete_first_elements + frames[0], delete_first_elements + frames[0]],
            [drop_height + 100, 0],
            'r--'
        )
        ax[0].set_xlabel('Time (frames)')
        ax[0].set_ylabel('Height [pixels]')
        ax[0].set_title('Beginning Data')

        ax[1].errorbar(afgeknipt_frame, afgeknipt_y, yerr=y_err, fmt='o', markersize=1)
        ax[1].plot(x1, y, 'r--')
        ax[1].plot(x2, y, 'r--')
        ax[1].set_xlabel('Time (frames)')
        ax[1].set_ylabel('Height (pixels)')
        ax[1].set_title('Data from moment of release')

        ax[2].errorbar(frame_bounce, y_bounce, yerr=y_err, markersize=2, fmt='o')
        ax[2].set_xlabel('Time (frames)')
        ax[2].set_ylabel('Height (pixels)')
        ax[2].set_title('Isolated first Bounce')

        fig.suptitle(f'Measurement on {variable_type} {variable_value}, filename = {filename}')
        plt.tight_layout()
        plt.show()

    bounce_height = parabola_fit(frame_bounce, y_bounce, Fit_Plot, Fit_Report) - afgeknipt_y[laagtepunt_1]
    drop_height = drop_height - afgeknipt_y[laagtepunt_1]
    COR = np.sqrt(bounce_height / drop_height)

    return COR




def get_avg_err(x, y):
    x =  np.array(x, dtype = float)
    y =  np.array(y, dtype = float)

    mask = ~ np.isnan(y)

    y_clean = y[mask]
    x_clean = x[mask]

    x_unique = np.unique(x)

    avg_y = []
    err_y = []

    for val in x_unique:
        y_group = y_clean[x_clean == val]
        avg_y.append(np.mean(y_group))
        err_y.append(np.std(y_group, ddof = 1)/len(y_group))

    return x_clean, y_clean, err_y, avg_y, x_unique
############################## Specific functions for specific files ###############################3

def databewerken(networkfolder, filename, thickness, Plot):
    # tweak these
    N_points = 5
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

    y_points = data_current.iloc[:, 1] 
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
        
    
    y = [0, average_first_N_points]
    x1 = [laagtepunt_1 + delete_first_elements, laagtepunt_1 + delete_first_elements]
    x2 = [laagtepunt_2 + delete_first_elements, laagtepunt_2 + delete_first_elements]

    frame_bounce = afgeknipt_frame[laagtepunt_1:laagtepunt_2]
    y_bounce = afgeknipt_y[laagtepunt_1:laagtepunt_2]

    if Plot:
        fig, ax = plt.subplots(1, 3, figsize=(18, 5))
        
        print(f'thickness = {thickness}')
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

        fig.suptitle(f'Measurement on thickness {thickness}, filename = {filename}')
        plt.tight_layout()
        plt.show()
    return average_first_N_points, frame_bounce, y_bounce

# Calculates all the COR's of a given file and plots them
# Input: Networkfolder adress, how the file begins (example: T3), list of thickness, the amount of repetitions at each thickness, Plot (True or False)
# Output: List of COR and the calculated error on the COR (based on how far apart the 3 measurements are).
def calulate_COR(networkfolder, filebegin, thicknesslist, repetitions, Plot):
    COR = []
    COR_err = []

    for thickness in thicknesslist:
        temp_COR = []

        for i in range(repetitions):
            filename = f"{filebegin}_d{thickness}_{i+1}_clean"
            drop_height, frames, y_points = databewerken(networkfolder, filename, thickness, False)
            bounce_height = parabola_fit(frames, y_points, False, False)
            temp_COR.append(np.sqrt(bounce_height/drop_height))
        COR.append(sum(temp_COR)/3) 
        COR_err.append(np.std(temp_COR, ddof = 1)/np.sqrt(3))

    if Plot:
        plt.errorbar(thicknesslist, COR, yerr= COR_err, fmt = 'o')
        plt.title('The COR as a function of substrate thickness')
        plt.xlabel('Thickness (paper layers)')
        plt.ylabel('Coefficient of restitution')
        plt.show()
    return COR, COR_err

# Reads out saladins data and plots it if Plot == True.
def read_saladin_data(filename, Plot, datacolumn):

    NETWORK_FOLDER = Path(rf"Z:\Results\Results_Firstyears")
    filepath = f"{NETWORK_FOLDER}\\{filename}"

    data_current = pd.read_csv(filepath)
    pulled_Thickness = data_current.iloc[:, 0] 
    pulled_COR = data_current.iloc[:, datacolumn]

    COR = []
    COR_err = []
    Thickness = []

    for a in range(int(len(pulled_COR)/3)):
        temp_COR = []

        for b in range(3):
            temp_COR.append(pulled_COR[3*a+b])
        COR.append(sum(temp_COR)/3)
        COR_err.append(np.std(temp_COR, ddof = 1)/np.sqrt(3))

    for a in range(int(len(pulled_Thickness)/3)):
        Thickness.append(pulled_Thickness[3*a])

    if Plot:
        plt.errorbar(Thickness, COR, yerr = COR_err, fmt = 'o')
        plt.title(f"File: {filename}")
        plt.xlabel("Thickness (paper sheets)")
        plt.ylabel("Coefficient of restitution")
        plt.show()

    return Thickness, COR, COR_err

# Normalizes y-data from the pressure readings. Made specifically to handle the naming format used.
def normalize_y(filename):
    NETWORK_FOLDER = Path(rf"Z:\Clean_Data\Data_Pressure_HalfClean")

    file_path = NETWORK_FOLDER / f"{filename}.csv"
    data_current =  pd.read_csv(file_path)

    old_y = pd.to_numeric(data_current.iloc[:, 2], errors='coerce')
    frames = pd.to_numeric(data_current.iloc[:, 0], errors='coerce')

    lowest_y = old_y.max()

    y_points = []
    for y in old_y:
        new_y = lowest_y - y
        y_points.append(new_y)

    cleaned_file = pd.DataFrame(
    {'Frame': frames,
     'Y': y_points,
    })

    cleaned_file.to_csv(f"{filename}_clean.csv", index = False)
    print(f"Saved as {filename}_clean.csv")

# Same thing: specific version for the pressure readings.
def calculate_COR_Vacuum(networkfolder, filename, value):
    drop_height, frames, y_points = databewerken(networkfolder, filename, value, False)
    bounce_height = parabola_fit(frames, y_points, False, False)
    COR = np.sqrt(bounce_height/drop_height)
    COR_err = 0 # not actual error, but couldnt calculate one.
    return COR, COR_err


print("Selfmadefuntions imported/reloaded")