import math
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys
from scipy import signal

#See http://www.phy.mtu.edu/~suits/notefreqs.html
C0 = 16.35  # Hz
A0 = 27.5   # Hz

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool that can generate an audio tone.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--freq', type=float, default=(2**5)*A0, help="Frequency")
    parser.add_argument('--dur', type=float, default=5, help="Duration of tone in seconds")
    parser.add_argument('--rate', type=int, default=16000, help="Sample rate in Hz")
    parser.add_argument('--signal', type=str, default="sin", help="Singnal shape (sin, square, sawtooth)")
    
    args = parser.parse_args()

    if args.signal != "sin" and args.signal != "square" and args.signal != "sawtooth":
        print "Signal type %s is not valid" % args.signal
        print len(args.signal)
        sys.exit(1)

    PyAudio = pyaudio.PyAudio
    
    #See http://en.wikipedia.org/wiki/Bit_rate#Audio
    bitrate = args.rate #number of frames per second/frameset.      
    frequency = args.freq #Hz, waves per second
    length = args.dur #seconds to play sound
    
    N = int(bitrate * length)
    t = np.linspace(0, length, num=N, endpoint=False)
    scale = 127
    offset = 128
    if args.signal == "sin":
        y = scale*np.sin(2*np.pi*frequency*t)+offset
    if args.signal == "square":
        y = scale*signal.square(2*np.pi*frequency*t)+offset
    if args.signal == "sawtooth":
        y = scale*signal.sawtooth(2*np.pi*frequency*t)+offset
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
