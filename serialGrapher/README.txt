############
Programs
############
getVSPdata.py - main script for recording data streaming from VSP
plotVSPdata.py - script for plotting data recorded from VSP
grapher.py - real time plotting of VSP data, is broken and should not be used, left for reference and future fixes

############
Libraries
############
SerialData.py - create a thread that reads from serial port and stores raw data in queue
VSP_format.py - parses binary VSP data format

############
Scripts
############
csv2csvMat.sh - converts all CSV files in a directory to CSV files that can be used by Matlab (basically strips out time stamp)
plot_long_walk.sh - plots some experimental data from experiments done in the hallway