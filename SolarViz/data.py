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
import csv

class Data(object):
    def __init__(self):
        self.data = [] # a list of dictionaries {"timestamp", "voltage", "current"}        
        
    def load(self, path):
        ifile  = open(path, "rb")
        reader = csv.reader(ifile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    
        for row in reader:
            self.data.append( {"timestamp" : row[0], "voltage" : row[1], "current" : row[2]} )
            
    def save(self, path):
        ofile  = open(path, "wb")
        writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        for row in self.data:
            writer.writerow( (row["timestamp"], row["voltage"], row["current"]) )
    
    def get_data(self):
        return self.data
    
    def make_rand(self):
        import random
        import os
        import time
        
        timestamp = time.time()
        for i in range(1000):
            voltage = random.uniform(2.5, 3.5)
            resistance = random.randrange(50, 100)  # 50 to 100 ohms
            # apply ohm's law
            current = voltage / resistance            
            self.data.append( {"timestamp" : timestamp, "voltage" : voltage, "current" : current} )
            timestamp += 10
            
        for each in self.data:
            print each
            
if __name__ == "__main__":
    data = Data()
    data.make_rand()
    data.save("file.csv")
    

        