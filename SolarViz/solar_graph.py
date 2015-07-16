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
            if self.yfunction != None:           
                ydata = self.yfunction(row[self.ydata])
            else:
                ydata = row[self.ydata]     
            if (xdata >= xmin and xdata <= xmax) or (xmin == None and xmax == None):
                self.ax.scatter( float(xdata), float(ydata) )
                counter += 1
#                print xdata, " ", float(row[self.ydata])

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
#        print self.ax.get_xlim()
#        print self.ax.get_ylim()
#        print self.ax.get_data_ratio()        
        self.calc_stride()
        self.ax.clear()                                     
        self.plot(self.ax.get_xlim()[0], self.ax.get_xlim()[1])
        self.unbind()                         
        self.bind()        