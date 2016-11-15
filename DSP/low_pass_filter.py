import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import fft
from scipy.io import wavfile

def fftnoise(f):
    f = np.array(f, dtype='complex')
    Np = (len(f) - 1) // 2
    phases = np.random.rand(Np) * 2 * np.pi
    phases = np.cos(phases) + 1j * np.sin(phases)
    f[1:Np+1] *= phases
    f[-1:-1-Np:-1] = np.conj(f[1:Np+1])
    return np.fft.ifft(f).real

def band_limited_noise(min_freq, max_freq, samples=1024, samplerate=1):
    freqs = np.abs(np.fft.fftfreq(samples, 1.0/samplerate))
    f = np.zeros(samples)
    idx = np.where(np.logical_and(freqs>=min_freq, freqs<=max_freq))[0]
    f[idx] = 1
    return fftnoise(f)


fs = 44100 # Sample frequency (Hz)
L = 10 # 10 seconds
N = fs*L # Number of samples
t = np.linspace(0, L, num=N, endpoint=False) 

sig1 = 150.0*np.sin(2*np.pi*100*t) # 100 Hz

noise = band_limited_noise(500, 2000, N, fs)
noise = np.int16(noise * (2 ** 15 - 1))

y = sig1 + noise

ax1 = plt.subplot(311)
plt.plot(t, sig1)
plt.plot(t, y)
plt.xlabel("Time (s)")
plt.grid()

plt.subplot(312, sharex=ax1, sharey=ax1)
plt.plot(t, noise)

plt.grid()

plt.subplot(313)
#yf = fft(sig1)
yf = fft(y)
xf = np.linspace(0.0, fs/2, num=N/2)
plt.title("FFT, 100 Hz + Band limited noise")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.plot(xf, 20*np.log10(np.abs(yf[0:N/2])))


plt.show()


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y


# Filter requirements.
order = 6
cutoff = 200  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# Plot the frequency response.
w, h = signal.freqz(b, a, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()


y_filt = butter_lowpass_filter(y, cutoff, fs, order)

plt.subplot(2, 1, 2)
plt.plot(t, y, 'b-', label='data')
plt.plot(t, y_filt, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)

plt.show()

wavfile.write("orig.wav", 44100, sig1)
wavfile.write("noise.wav", 44100, noise)
wavfile.write("final.wav", 44100, y)
wavfile.write("filtered.wav", 44100, y_filt)
