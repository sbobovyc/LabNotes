"""
Created on September 12, 2011

@author: sbobovyc
"""
"""   
    Copyright (C) 2011 Stanislav Bobovych

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

from matplotlib.pylab import plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
    
class TimeVoltage(object):
    
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data 
        
    def plot_data(self):
        solar_data = self.data.get_data()
        
        # plot time vs. voltage        
        # It's much more convenient to just use pyplot's factory functions...
        fig, ax = plt.subplots()
        ax.set_title("Time vs. Voltage")
        ax.get_xaxis().set_label_text("time (s)")
        ax.get_yaxis().set_label_text("voltage (V)")
        
        time_zero = float(solar_data[0]["timestamp"])
        for row in solar_data:            
            time_delta = float(row["timestamp"]) - time_zero             
            ax.scatter( time_delta, float(row["voltage"]) )

        # set x axis limit
        ax.set_xlim( [0, time_delta] )
        
        self.canvas = FigureCanvasTkAgg(fig, master=self.parent)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg( self.canvas, self.parent )
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)