import matplotlib.pylab as plt
import numpy as np
import sys
import datetime


a = np.load(sys.argv[1])
t = a[:,0]
d = a[:,1]

try:
    type(float(d[0]))
except ValueError:
    t = a[1:,0]
    d = a[1:,1]

plt.plot_date(t, d)

plt.show()
