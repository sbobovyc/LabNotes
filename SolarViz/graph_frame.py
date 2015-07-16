"""
Created on September 20, 2011

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

import solar_graph
from matplotlib import pyplot 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

class GUI_graph_frame(tk.Frame):
    
    def __init__(self, parent, controller):
        # register with controller
        self.name = "graph_frame"
        self.controller = controller
        self.controller.register(self, self.name)                
        tk.Frame.__init__(self, parent, bd=2, relief=tk.FLAT, background="grey")
        
        # create pyplot figure
        self.fig = pyplot.figure()
        self.fig.subplots_adjust(hspace=0.8)
        
        # draw figure and control bar on canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg( self.canvas, self )
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
    def plot_data(self, solar_data, sample_stride, title, xlabel, ylabel, xdata, ydata, xfunction=solar_graph.nop, yfunction=solar_graph.nop):                
        self.ax = pyplot.subplot(111)   
        self.solar_graph = solar_graph.graph(self.fig, self.ax, solar_data, sample_stride, title, xlabel, ylabel, xdata, ydata, xfunction, yfunction)          
        self.canvas.show()
