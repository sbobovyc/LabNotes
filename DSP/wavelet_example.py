import numpy as np
import matplotlib.pyplot as plt
import pywt
from scipy import signal

mode = pywt.Modes.smooth
mode = pywt.Modes.periodization

def plot_signal_decomp(data, w, level, title):
    """Decompose and plot a signal S.
    S = An + Dn + Dn-1 + ... + D1
    """
    a = data
    ca = []
    cd = []
    for i in range(level):
        (a, d) = pywt.dwt(a, w, mode)
        ca.append(a)
        cd.append(d)
#         print("Ca/Cd len", len(a), len(d))

    rec_a = []
    rec_d = []

    for i, coeff in enumerate(ca):
        coeff_list = [coeff, None] + [None] * i
        rec_a.append(pywt.waverec(coeff_list, w, mode))
#         print("Len a", len(rec_a[-1]))

    for i, coeff in enumerate(cd):
        coeff_list = [None, coeff] + [None] * i
        rec_d.append(pywt.waverec(coeff_list, w, mode))
#         print("Len d", len(rec_d[-1]))

    fig = plt.figure()
    ax_main = fig.add_subplot(len(rec_a) + 1, 1, 1)
    ax_main.set_title(title)
    ax_main.plot(data)
    ax_main.set_xlim(0, len(data) - 1)

    for i, y in enumerate(rec_a):
        ax = fig.add_subplot(len(rec_a) + 1, 2, 3 + i * 2)
        ax.plot(y, 'r')
        ax.set_xlim(0, len(y) - 1)
        ax.set_ylabel("A%d" % (i + 1))

    for i, y in enumerate(rec_d):
        ax = fig.add_subplot(len(rec_d) + 1, 2, 4 + i * 2)
        ax.plot(y, 'g')
        ax.set_xlim(0, len(y) - 1)
        ax.set_ylabel("D%d" % (i + 1))



fs = 100 # Sample frequency (Hz)
L = 10 # 10 seconds
N = fs*L # Number of samples
t = np.linspace(0, L, num=N, endpoint=False) 

noise = np.random.normal(scale=0.5, size=t.shape[0])
scale_noise = np.random.normal(scale=1.0, size=t.shape[0])
sig1 = 1.3*np.sin(2*np.pi*5*t) # 5 Hz
sig2 = 1.7*np.sin(2*np.pi*2*(t-10)) # 2 Hz, phase shifted
y = sig1 + sig2 + noise*scale_noise

plt.figure()
plt.title("Original signal")
plt.xlabel("Time (seconds)")
plt.plot(t, y)
plt.show()

print("Data length", len(y))
w = pywt.Wavelet('sym5')
max_level = pywt.dwt_max_level(len(y), w.dec_len)
print("Max level", max_level)
plot_signal_decomp(y, w, max_level, "DWT - Symmlets5")
plt.show()
