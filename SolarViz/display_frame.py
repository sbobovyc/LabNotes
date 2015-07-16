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

from matplotlib import pyplot 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

def nop(value):
        return value
    
class graph(object):
    def __init__(self, fig, ax, solar_data, sample_stride, title, xlabel, ylabel, xdata, ydata, xfunction=nop, yfunction=nop):
        self.solar_data = solar_data
        self.figure = fig
        self.ax = ax        
        self.original_sample_stride = sample_stride
        self.current_sample_stride = sample_stride 
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.xdata = xdata
        self.ydata = ydata
        self.xfunction = xfunction
        self.yfunction = yfunction
            
        self.plot()
        self.bind()
        
        self.original_delta_x = self.ax.get_xlim()[1] - self.ax.get_xlim()[0]
        print "##################"
        print self.original_delta_x 
        print self.original_sample_stride
        print self.current_sample_stride
        print "##################"
    
    def plot(self, xmin=None, xmax=None):        
        self.ax.set_title(self.title)        
        self.ax.get_xaxis().set_label_text(self.xlabel)
        self.ax.get_yaxis().set_label_text(self.ylabel)
        self.ax.grid(True)
        counter = 0
        for row in self.solar_data[::self.current_sample_stride]:              
            if self.xfunction != None:           
                xdata = self.xfunction(row[self.xdata])
            else:
                xdata = row[self.xdata]     
            if (xdata >= xmin and xdata <= xmax) or (xmin == None and xmax == None):
                self.ax.scatter( float(xdata), float(row[self.ydata]) )
                counter += 1
#                print xdata, " ", float(row[self.ydata])
#        self.ax.set_xlim(xmin, xmax)
        self.ax.autoscale_view(scalex=False,scaley=True)
        print "Plotted ", counter
        print "Sample stride ", self.current_sample_stride
        
    def bind(self):
        self.x_callback_id = self.ax.callbacks.connect('xlim_changed', self.replot) 
        self.y_callback_id = self.ax.callbacks.connect('ylim_changed', self.replot)
        
    def unbind(self):
        self.ax.callbacks.disconnect(self.x_callback_id) 
        self.ax.callbacks.disconnect(self.y_callback_id)
    
    def calc_stride(self):
        new_delta_x = self.ax.get_xlim()[1] - self.ax.get_xlim()[0]
        self.current_sample_stride = int( ( self.original_sample_stride * new_delta_x ) / self.original_delta_x )
        if self.current_sample_stride == 0:
            self.current_sample_stride = 1
    ##
    # @param ax: matplotlib axes, needed by the callback 
    def replot(self, ax):
        print self.ax.get_xlim()
#        print self.ax.get_ylim()
#        print self.ax.get_data_ratio()        
        self.calc_stride()
        self.ax.clear()                                     
        self.plot(self.ax.get_xlim()[0], self.ax.get_xlim()[1])
        self.unbind()                         
        self.bind()        
        
        
class GUI_display_frame(tk.Frame):
    
    def __init__(self, parent, controller):
        # register with controller
        self.name = "display_frame"
        self.controller = controller
        self.controller.register(self, self.name)
        
        
        tk.Frame.__init__(self, parent, bd=2, relief=tk.FLAT, background="grey")
        
        
    def plot_data(self, data, lod=False):                
        solar_data = data.get_data()        
                
        # It's much more convenient to just use pyplot's factory functions...
        self.fig = pyplot.figure(1)
        self.fig.subplots_adjust(hspace=0.8)
        self.fig.set_lod(True)
        pyplot.grid(True)        

        # plot time vs. voltage                
        self.ax1 = pyplot.subplot(311)
        time_zero = float(solar_data[0]["timestamp"]) 
        self.time_current = graph(self.fig, self.ax1, solar_data, 10, "Time vs. Voltage", "time (s)", "voltage (V)", "timestamp", "voltage", xfunction=(lambda x: float(x) - time_zero))
#                
#        # plot time vs. current
        self.ax2 = pyplot.subplot(312, sharex = self.ax1)        
        self.time_current = graph(self.fig, self.ax2, solar_data, 10, "Time vs. Current", "time (s)", "current (A)", "timestamp", "current", xfunction=(lambda x: float(x) - time_zero))


        # plot voltage vs. current
#        self.ax3 = pyplot.subplot(313)        
#        self.iv = graph(self.fig, self.ax3, solar_data, 1,"Voltage vs. Current", "voltage (V)", "current (A)", "voltage", "current")        
        
        # draw figure and control bar on canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg( self.canvas, self )
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
    

        
