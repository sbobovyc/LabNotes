import numpy as np
import matplotlib.pyplot as plt

start = 0
stop = 2*np.pi
samples = 100
x = np.linspace(start, stop, samples)
y = np.sin(x)
plt.plot(x,y, '.')
plt.show()
