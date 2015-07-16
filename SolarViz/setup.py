from distutils.core import setup
import py2exe


packages = ['numpy']
includes = ['matplotlib.numerix.random_array',
            'pytz.zoneinfo.UTC',
            'scipy.misc.info']                              

setup(
    name="SolarViz v0.1",
    version="0.1",
    description = "Solar data visualizer",
    author="Stanislav Bobovych",
    author_email="stan.bobovych@gmail.com",
    options = { 'py2exe': { "includes" : ["matplotlib.backends", "matplotlib.backends.backend_qt4agg",
"matplotlib.figure", "pylab", "numpy", "matplotlib.numerix.fft",
"matplotlib.numerix.linear_algebra", "matplotlib.numerix.random_array",
"matplotlib.backends.backend_tkagg"] }}, 

#    options = {'py2exe': {'optimize': 0, 'packages': packages,'includes': includes} },
    windows = [
        {'script': "main.py"}
          #{'icon_resources': [(0, 'dcs.ico')], 'dest_base': 'DCS', 'script': main.py}
    ],
)
