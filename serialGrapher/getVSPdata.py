import argparse
import csv
import datetime
import time
import binascii
import VSP_format
from SerialData import SerialData

class FileData(object):
    def __init__(self, filepath, len_packet):
        self.f = open(filepath, 'rb')
        self.size = len_packet

    def next(self):
        data = self.f.read(self.size+3)        
        return (data, None)

    def quit(self):
        self.f.close()
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool to get data from VSP using the serial port.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--port', nargs='?', default="COM38", help='Serial port')
    parser.add_argument('--baud', nargs='?', default=115200, help='Baud rate')
    parser.add_argument('--chan', nargs='?', default=6, type=int, help='Number of channels')
    parser.add_argument('-s', '--stream', default=False, action='store_true', help='Stream data to stdout instead of saving to file.')
    parser.add_argument('-f', '--file', default=None, help='Parse binary file instead of stream from serial port.')
    parser.add_argument('-w', '--work', default=False, action='store_true', help='Name output file #plate_work.csv instead of name with timestamp.')
    args = parser.parse_args()

    packet_size = args.chan*4
    formatter = VSP_format.Formatter(packet_size, ">" + "I"*args.chan)
    
    if args.file == None:
        s = SerialData(port=args.port, baud=args.baud, timestamp_format="%H:%M:%S.%f")
    else:
        s = FileData(args.file, packet_size)
        
    if not args.stream:
        name = "work"
        if not args.work:
            name = datetime.datetime.now().strftime("%m-%d-%y_%H-%M-%S")
        csvfile = open("%iplate_%s.csv" % (args.chan, name), "wb")
        writer = csv.writer(csvfile)
    count = 0
    try:
        while True:
            new_data = s.next()
            data = formatter.parse(new_data)
            if data == None and len(formatter.raw_data) != 0:
                data = formatter.parse(None, True)
            if data != None:
                print count,data                
                count += 1
                if not args.stream:
                    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")
                    writer.writerow([timestamp] + list(data))
    except KeyboardInterrupt:
        print "Ctrl-C detected, exiting"
        if not args.stream:
            csvfile.close()
        s.quit()  
