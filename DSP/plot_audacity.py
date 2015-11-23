import numpy as np
import matplotlib.pyplot as plt
import sys

if len(sys.argv) != 2:
    sys.exit(0)

freq,db = np.genfromtxt(sys.argv[1], skip_header=1, unpack=True)
plt.plot(freq,db)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.xlim([0, max(freq)])
plt.ylim([min(db), max(db)])
plt.fill_between(freq, db, min(db))
plt.grid()
plt.show()
