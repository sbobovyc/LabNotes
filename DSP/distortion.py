#############
# Distortion due to clipping
#############

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

def norm(sig):
    """Normalisze signal."""
    sig_max = np.float(np.max(np.abs(sig)))
    return sig / sig_max


Fs = 500    # Sampling frequency
T = 1.0/Fs  # Sampling period
L = 1       # Length of signal
N = Fs*L
t = np.linspace(0, L, num=N, endpoint=False) # 10 sec sample

plt.figure(1)
plt.subplot(311)
y = np.sin(t*2*np.pi*25)*2 # 25 Hz
y_clipped = np.clip(y, -1, 1)
plt.title("25 Hz sin")
plt.plot(t,y, label="original")
plt.plot(t,y_clipped, linewidth=2, label="clipped")
plt.legend()

yf = fft(y)
xf = Fs*np.fft.fftfreq(yf.size)[0:N/2]
plt.subplot(312)
plt.title("FFT, 25 Hz sin")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (absolute)")
plt.plot(xf, 2.0/N * np.abs(yf[0:N/2]))

yf_clipped = fft(y_clipped)
plt.subplot(313)
plt.title("FFT, 25 Hz sin (clipped -1 to 1)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (absolute)")
plt.plot(xf, 2.0/N * np.abs(yf_clipped[0:N/2]))

plt.figure(2)
plt.subplot(311)
y_clipped_upper = np.clip(y, -2, 1)
plt.title("25 Hz sin")
plt.plot(t,y, label="original")
plt.plot(t, y_clipped_upper, linewidth=2, label="clipped")

plt.subplot(312)
plt.title("FFT, 25 Hz sin (clipped -1 to 1)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (absolute)")
plt.plot(xf, 2.0/N * np.abs(yf_clipped[0:N/2]))

yf_clipped_upper = fft(y_clipped_upper)
plt.subplot(313)
plt.title("FFT, 25 Hz sin (clipped -2 to 1)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (absolute)")
plt.plot(xf, 2.0/N * np.abs(yf_clipped_upper[0:N/2]))

plt.tight_layout()
plt.show()
