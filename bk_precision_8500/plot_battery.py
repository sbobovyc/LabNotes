import matplotlib.pyplot as plt
import matplotlib.dates as md
import dateutil
import csv
import sys


if len(sys.argv) < 2:
    print "Usage: python plot_battery. file.txt"
    sys.exit()
    
datafile = sys.argv[1]

time = []
voltage = []
with open(datafile, 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    reader.next() # skip header
    for row in reader:
        time.append(dateutil.parser.parse(row[0]))
        voltage.append(row[1])

fig = plt.figure()
plt.subplots_adjust(bottom=0.2)
plt.xticks( rotation= 80 )
ax=plt.gca()
xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
ax.set_ylabel('Battery voltage (V)')
ax.set_title(datafile)

plt.plot(time,voltage, "o-")
plt.show()

