import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

fs = 1000 # Sample frequency (Hz)
N = fs*1 # Number of samples
t = np.linspace(0, 1, num=N, endpoint=False) # 1 sec sample
mu, sigma = 0, 0.1 # mean and standard deviation
y = np.random.normal(mu, sigma, N)

plt.figure(1)
plt.subplots_adjust(hspace=0.8)
plt.subplot(411)
plt.title("Clean signal")
plt.xlabel("Time (sec)")
plt.ylabel("Magnitude")
plt.plot(t,y)

yf = fft(y)
xf = np.linspace(0.0, fs/2, num=N/2)
plt.subplot(412)
plt.title("FFT, Clean signal")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.plot(xf, 20*np.log10(np.abs(yf[0:N/2]))) # Plot 0 to fs/2, in dB

plt.subplot(413)
noise = 0.2*np.sin(2*np.pi*60*t) # 60 Hz noise
y = y+noise
plt.title("Signal with 60 Hz noise")
plt.xlabel("Time (sec)")
plt.ylabel("Magnitude")
plt.plot(t, y)

yf = fft(y)
xf = np.linspace(0.0, fs/2, num=N/2)
plt.subplot(414)
plt.title("FFT, Signal with 60 Hz noise")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.plot(xf, 20*np.log10(np.abs(yf[0:N/2])))

plt.show()
