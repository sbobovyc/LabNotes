import os
import sys

#plugin = __import__("plugins", fromlist=["test"])
#print plugin.test.plot()

#name = "plugins.test"
#__import__(name)
#plug = sys.modules[name]
#print plug
#plug.plot()


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
    
plugin = import_file(os.path.abspath(".\plugins\\test.py"))
plugin.plot()
