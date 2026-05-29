import time
import nidaqmx
from nidaqmx.constants import AcquisitionType, TerminalConfiguration
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import traceback
from threading import Thread, Lock
from tkinter import filedialog as fd

# =================== USER PARAMETERS ===================
SAMPLERATE = 400000.0         # Sampling rate in Hz
DURATION_SEC = 4            # Total acquisition duration in seconds
CHANNEL_NAME = "Dev1/ai0"     # Analog input channel
TRIGGER_LINE = "Dev1/PFI0"    # Digital line used as trigger
ENABLE_TRIGGER = False        # Toggle hardware trigger ON/OFF

# =================== SYSTEM CONSTANTS ===================
NUM_SAMPLES = int(SAMPLERATE * DURATION_SEC)
DATA_BUFFER_SIZE = int(SAMPLERATE * 2)  # Buffer for continuous streaming
MAXPOINTS_TO_SHOW = 5000                # Reduced number of points to keep display responsive
AMOUNTPOINTS = 40000                    # Samples per callback
GRAPHINTERVAL = 100                     # Graph update interval in ms

# =================== SHARED VARIABLES ===================
data = []
x = []
y = []
slotje = Lock()
endtask = False
start_time = None
anim = None  # persist animation object

def update(frame):
    global graph, x, y, ax, slotje, endtask, start_time

    try:
        slotje.acquire()
        try:
            if len(y) > 0:
                xstep = 1 / SAMPLERATE
                x_full = np.linspace(0, len(y) * xstep, len(y))

                if len(y) >= NUM_SAMPLES:
                    endtask = True

                # Plot all points collected so far, with x-axis capped at duration
                graph.set_xdata(x_full)
                graph.set_ydata(y)
                ax.set_xlim(0, DURATION_SEC)

                ymin = y.min() - abs(0.05 * y.min())
                ymax = y.max() * 1.05
                ax.set_ylim(ymin, ymax)
        finally:
            slotje.release()
    except Exception:
        traceback.print_exc()

def measurement(task):
    global y, slotje, endtask, start_time

    def callback(task_handle, every_n_samples_event_type, number_of_samples, callback_data):
        nonlocal task
        global y, endtask

        if endtask:
            task.stop()
            return 0

        samples = task.read(number_of_samples_per_channel=number_of_samples)
        slotje.acquire()
        try:
            y = np.append(y, samples)
        finally:
            slotje.release()

        if len(y) >= NUM_SAMPLES:
            endtask = True

        return 0

    try:
        task.ai_channels.add_ai_voltage_chan(CHANNEL_NAME, terminal_config=TerminalConfiguration.RSE)
        task.timing.cfg_samp_clk_timing(SAMPLERATE, sample_mode=AcquisitionType.CONTINUOUS)
        task.in_stream.input_buf_size = DATA_BUFFER_SIZE

        if ENABLE_TRIGGER:
            try:
                task.triggers.start_trigger.cfg_dig_edge_start_trig(TRIGGER_LINE)
            except nidaqmx.errors.DaqError as e:
                print("[Warning] Trigger configuration failed, falling back to no trigger.")
                print(f"\n[DAQmx Error] {e}\n")
                print("Continuing without external trigger.\n")

        task.register_every_n_samples_acquired_into_buffer_event(AMOUNTPOINTS, callback)

        start_time = time.time()
        task.start()

        while not endtask:
            time.sleep(0.05)

        task.stop()

    except Exception:
        traceback.print_exc()
    finally:
        try:
            task.close()
        except:
            pass

def main():
    global graph, ax, y, slotje, endtask, anim

    filename = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not filename:
        print("No file selected. Exiting.")
        return
    print(f"File will be saved as: {filename}")

    endtask = False
    slotje = Lock()
    y = np.array([])

    fig, ax = plt.subplots()
    graph, = ax.plot([], [], color='g')
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (V)")
    ax.set_title("Live Acquisition")
    ax.grid(True)
    ax.set_xlim(0, DURATION_SEC)

    anim = FuncAnimation(fig, update, interval=GRAPHINTERVAL, cache_frame_data=False)

    task = nidaqmx.Task()
    mt = Thread(target=measurement, args=(task,))
    mt.start()

    plt.show()  # Blocks until user closes

    print("\nWaiting for acquisition thread to complete...")
    mt.join()

    print(f"Writing {len(y)} samples to file...")
    with open(filename, 'w') as f:
        f.write("time,voltage\n")
        x_vals = np.arange(0, len(y)) / SAMPLERATE
        for t, v in zip(x_vals, y):
            f.write(f"{t:.7f},{v}\n")

    print("Data saved. Done!")

if __name__ == "__main__":
    main()
