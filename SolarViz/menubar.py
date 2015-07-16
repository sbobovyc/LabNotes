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
import tkFileDialog
import os


class GUI_menubar(tk.Menu):
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.name = "menubar"
        self.controller = controller
        self.controller.register(self, self.name)
        # file types
        self.file_types = [('', '.csv'), ('all files', '.*')]
        
        # create a menu
        tk.Menu.__init__(self, parent)
                
        filemenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=filemenu)
#        filemenu.add_command(label="New Project", command=self.callback())
#        filemenu.add_command(label="Open Project", command=self.callback())
        filemenu.add_command(label="Open ...", command=self.file_open)
#        filemenu.add_command(label="Save", command=self.callback())
        filemenu.add_command(label="Save as", command=None)        
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_callback)
        
        helpmenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=None)
        
    def callback(self):
        print "called the callback!"
    
    def file_open(self):                
        path = tkFileDialog.askopenfilename(filetypes=self.file_types)
        self.controller.open_data(path) 
        
    def exit_callback(self):
        self.parent.quit()
        
        

        