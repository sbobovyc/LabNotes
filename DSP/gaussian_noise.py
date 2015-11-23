import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import fft

fs = 100 # Sample frequency (Hz)
L = 10 # 10 seconds
N = fs*L # Number of samples
t = np.linspace(0, L, num=N, endpoint=False) 

noise = np.random.normal(scale=0.5, size=t.shape[0])
sig1 = 1.3*np.sin(2*np.pi*15*t) # 15 Hz
sig2 = 1.7*np.sin(2*np.pi*40*(t-2)) # 40 Hz, phase shifted
y = sig1 + sig2 + noise

plt.subplot(311)
plt.title("15 Hz + 40 Hz")
plt.xlabel("Time (seconds)")
plt.plot(t, sig1+sig2)

plt.subplot(312)
plt.title("15 Hz + 40 Hz + Gaussian noise")
plt.xlabel("Time (seconds)")
plt.plot(t,y)

plt.subplot(313)
yf = fft(y)
plt.title("FFT, 15 Hz + 40 Hz + Gaussian noise")
xf = np.linspace(0.0, fs/2, num=N/2)
plt.plot(xf, np.abs(yf[0:N/2]))
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (absolute value)")

plt.tight_layout()
plt.show()
