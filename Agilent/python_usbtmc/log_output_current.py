import usbtmc
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import MinuteLocator
from multiprocessing import Process

data_list = []

def save_data():
    data_array = np.array(data_list)
    np.save("current_log", data_array)

instr = usbtmc.Instrument(0x0957, 0x4d18)
print(instr.ask("*IDN?"))
time.sleep(0.5)
instr.write("INIT:CONT ON")

try:
    while True:
        ts = datetime.datetime.now()
        # curr = float(instr.ask("SENS:CURR?"))
        # c = instr.ask("MEAS:CURR?")
        c = instr.ask("FETC?")
        curr = c
        print(ts,curr)
        data_list.append([ts, curr])
        if len(data_list) % 1000 == 0:
            print("Saving", len(data_list))
            Process(target=save_data).start()
        time.sleep(0.01)  # sample every 10 ms
except KeyboardInterrupt:
    print("W: interrupt received, stopping…")
    data_array = np.array(data_list)

    t = data_array[:,0]
    d = data_array[:,1]
    np.save("current_log", data_array)
    plt.ioff()
    fig, ax = plt.subplots()
    ax.plot_date(t, d, '-')
    ax.grid()

    minute = MinuteLocator()
    # format the ticks
    # ax.xaxis.set_major_locator(minute)
    # ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(minute)
    ax.autoscale_view()
    plt.show()

finally:
    # clean up
    instr.close()
