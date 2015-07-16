#/usr/bin/env python
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

import Utils
from menubar import GUI_menubar
from graph_frame import GUI_graph_frame
from Controller import Controller

class GUI_main(tk.Tk):
    '''
    classdocs
    '''
    
    def __init__(self, parent):
        '''
        Constructor
        '''
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.name = "main"   

        # if on linux, set the icon
#        if Utils.isLinux():                
#            os.path.join("..", "dcs.xbm")     
#            self.iconbitmap('@../dcs.xbm')    
        
        # instantiate the controller, register with the controller
        self.controller = Controller()
        self.controller.register(self, self.name)
        self.initialize()
        
    def initialize(self):
        # make the main window cover the entire screen
        if Utils.isLinux():
            self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
            self.geometry("%dx%d+0+0" % (self.w, self.h))
        if Utils.isWindows():
            self.wm_state('zoomed')    

        # bind exit command
        self.protocol("WM_DELETE_WINDOW", self.shutdown)
        
        #create menu
        self.menu = GUI_menubar(self, self.controller)
        self.config(menu=self.menu)
        
        
        # create frame structure
        self.big_frame = tk.Frame(self, bd=2, relief=tk.FLAT, background="grey")
        self.big_frame.pack(anchor=tk.NW, expand=tk.TRUE, fill=tk.BOTH)
        
        # display frame
        #self.graph_frame = GUI_graph_frame(self.big_frame, self.controller)
        #self.graph_frame.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)  
                
    
    def shutdown(self):
        self.destroy()
        raise SystemExit
        
if __name__ == "__main__":
    app = GUI_main(None)
    app.title('SolarViz')    
    app.mainloop()
