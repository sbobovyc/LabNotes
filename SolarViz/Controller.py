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
    
from data import Data
from matplotlib import pyplot 
import imp
import os

import Utils
from graph_frame import GUI_graph_frame

class Controller(object):
    
    def __init__(self):
        self.object_map = {} 
        self.path = None  #current image_path
        self.data = None
    
    ##
    # @param object: a tkinter gui object
    # @param name: a string that represent the name of the object
    def register(self, object, name):        
        self.object_map[name] = object
    
    def open_data(self, path):        
        self.path = path
        #print path          
        self.data = Data()
        self.data.load(path)
        
        plugin_list = Utils.dir("plugins")
        print plugin_list
        for plugin_path in plugin_list:
            plugin = Utils.import_file(plugin_path)
            print "Loading ", plugin
            solar_data, sample_stride, title, xlabel, ylabel, xdata, ydata, xfunction, yfunction = plugin.plot(self.data)
            graph_frame = GUI_graph_frame(self.object_map["main"].big_frame, self)
            graph_frame.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH) 
            graph_frame.plot_data(solar_data, sample_stride, title, xlabel, ylabel, xdata, ydata, xfunction, yfunction)
        # plot time vs. voltage                     
        #time_zero = float(self.data.get_data()[0]["timestamp"]) 
        #self.object_map["main"].graph_frame.plot_data(self.data.get_data(), 10, "Time vs. Voltage", "time (s)", "voltage (V)", "timestamp", "voltage", xfunction=(lambda x: float(x) - time_zero))
        
           
        

        
