#!/usr/bin/env python
from matplotlib import pyplot as plt

def callback(ax):
    """ prints mode of toolbar after limits changed

          e.g.
           mode : >zoom rect<
           mode : >pan/zoom<
    """
    print " mode : >%s<" % (plt.get_current_fig_manager().toolbar.mode) 
    print ax.get_xaxis().get_view_interval()
    print ax.get_yaxis().get_view_interval()
            
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click to build line segments')
ax.plot([0], [0])  # empty line
ax.callbacks.connect('xlim_changed', callback) 
ax.callbacks.connect('ylim_changed', callback) 

plt.show()