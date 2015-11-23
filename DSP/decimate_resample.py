import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

start = 0
stop = 2*np.pi
samples = 100
x = np.linspace(start, stop, samples)
y = np.sin(x)
plt.plot(x,y, color="blue", linestyle="-", label="original")
new_samples = 20
rate = samples/new_samples
x_decimated = scipy.signal.decimate(x, rate)
y_decimated = scipy.signal.decimate(y, rate)

plt.figure(1)
plt.plot(x_decimated,y_decimated, color="red", linestyle="_", marker=".", label="decimated")
plt.legend()

plt.figure(2)
plt.plot(x,y, color="blue", linestyle="-", label="original")

resampled_signal = scipy.signal.resample(y, new_samples, x)
y_resampled = resampled_signal[0]
x_resampled = resampled_signal[1]
plt.plot(x_resampled,y_resampled, color="darkgreen", linestyle="_", marker=".", label="resampled")
plt.legend()

plt.show()
