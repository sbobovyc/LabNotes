"""
Created on September 14, 2011

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

import os
import sys

def isLinux():
    if os.sys.platform == "linux2":
        return True
    else:
        return False
    
def isWindows():
    if os.sys.platform == "win32":
        return True
    else:
        return False

def import_file(full_path_to_module):
    try:        
        module_dir, module_file = os.path.split(full_path_to_module)
        package_name = os.path.basename(module_dir)
        module_name, module_ext = os.path.splitext(module_file)        
        save_cwd = os.getcwd()
        os.chdir(module_dir)
        print module_name
        __import__(package_name + "." + module_name)
        module = sys.modules[package_name + "." + module_name]
        os.chdir(save_cwd)
        return module
    except:
        raise ImportError
    
def dir(path):
    file_list = []
    dirList=os.listdir(path)
    for fname in dirList:
        if fname.endswith(".py") and fname != "__init__.py":
            file_list.append(os.path.join(path, fname))
    return file_list
