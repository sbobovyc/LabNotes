import math
import pyaudio
import numpy as np
import matplotlib.pyplot as plt

#See http://www.phy.mtu.edu/~suits/notefreqs.html
C0 = 16.35  # Hz
A0 = 27.5   # Hz

NOTE = (2**5)*A0

PyAudio = pyaudio.PyAudio

#See http://en.wikipedia.org/wiki/Bit_rate#Audio
bitrate = 16000 #number of frames per second/frameset.      

frequency = NOTE #Hz, waves per second
length = 5 #seconds to play sound

N = int(bitrate * length)
t = np.linspace(0, length, num=N, endpoint=False)
scale = 127
offset = 128
y = scale*np.sin(2*np.pi*frequency*t)+offset
y = y.astype(np.uint8)

#plt.plot(t,y)
#plt.show()

p = PyAudio()
stream = p.open(format = p.get_format_from_width(1), 
                channels = 1, 
                rate = bitrate, 
                output = True)

stream.write(y.tostring())

stream.stop_stream()
stream.close()
p.terminate()
