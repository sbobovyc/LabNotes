""" Listen to serial, return most recent numeric values Lots of help
from here:
http://stackoverflow.com/questions/1093598/pyserial-how-to-read-last-line-sent-from-serial-device
https://github.com/jonleung/AccelPlot/blob/master/plot/Archive/Arduino_Monitorz.py
"""
from threading import Thread
import time
import datetime
import serial
import random
import struct
import binascii
import Queue
import sys

log_info = "SerialData: "

class SerialData(object):
    def __init__(self, port="COM6", baud=9600, timestamp_format='%Y-%m-%d %H:%M:%S', verbose=False):
        self.Running = True
        self.thread = None
        self.ser = None
        self.queue = Queue.Queue()
        self.timestamp_format = timestamp_format
        self.verbose = verbose
        
        try:
            self.ser = ser = serial.Serial(
                port, baud, timeout=2, parity=serial.PARITY_NONE,
                        bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE,
                        rtscts=1
            )
        except serial.serialutil.SerialException:
            print log_info + "No serial port"
            sys.exit(0)
        self.thread = Thread(target=self.receiving, name="_SerialRecieve_", args=(self.ser,))
        self.thread.start()

    def receiving(self, ser):
        if self.ser != None:
            while self.Running:
                    raw_data = ser.read(ser.inWaiting())
                    if len(raw_data) != 0:
                        timestamp = datetime.datetime.now().strftime(self.timestamp_format)
                        self.queue.put_nowait((raw_data, timestamp))
                        if self.verbose:
                            print log_info + "Raw", binascii.hexlify(raw_data), timestamp
                            print log_info + "Queue size", self.queue.qsize()
        else:
                while self.Running:
                        self.queue.put(random.randint(0, 100), block=False, timeout=None)
                        
    def next(self):
        if self.queue.empty() != True:
            data = self.queue.get_nowait()
            if len(data) > 0:                
                #print log_info + "Getting data, queue size", self.queue.qsize()
                pass
            return data
        else:
            return None

    def queueEmpty(self):
        return self.queue.empty()
        
    def quit(self):
        print "Exiting SerialData"
        while self.queue.empty()==False:
            self.queue.get_nowait() #empty queue quickly         
        self.Running = False
        self.thread.join()
        if self.ser != None:
            self.ser.close()
        sys.exit() 

    def get_port_info(self):
        if self.ser != None:
            return (self.ser.port, self.ser.baudrate)
        else:
            return None
        
    def __del__(self):
        if self.ser:
            print log_info + "Closing serial port"
            self.ser.close()

if __name__ == '__main__':    
        s = SerialData(port="COM6")
        token = '$$$'
        len_packet = 52 # in bytes
        raw_data = ""
        try:     
                while True:                        
                        new_data = s.next()                        
                        if new_data != None and len(new_data) > 0:
                            raw_data += new_data
                            index = raw_data.find(token)
                            if index != -1:
                                #print "Found at ", index
                                substring = raw_data[index+len(token):]
                                #print "Length of string", len(substring)
                                if len(substring) >= len_packet:
                                    #print binascii.hexlify(substring[0:len_packet])
                                    print "Integers", struct.unpack(">26H", substring[0:len_packet])
                                    raw_data = substring[len_packet+1:]

        except KeyboardInterrupt:
                print "Ctrl-C detected, exiting"
                s.quit()
                s.Running = False
                s.thread.join()
                sys.exit() 
