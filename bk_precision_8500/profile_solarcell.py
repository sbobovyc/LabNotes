'''
Open Source Initiative OSI - The MIT License:Licensing
Tue, 2006-10-31 04:56 nelson

The MIT License

Copyright (c) 2009 BK Precision

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

This script talks to the DC load in two ways:
    1.  Using a DCLoad object (you'd use this method when you write a
        python application that talks to the DC load.

    2.  Using the COM interface.  This shows how python code uses the
        COM interface.  Other programming environments (e.g., Visual
        Basic and Visual C++) would use very similar techniques to
        talk to the DC load via COM.

Note that the DCLoad object and the COM server interface functions
always return strings.

$RCSfile: client.py $ 
$Revision: 1.0 $
$Date: 2008/05/16 21:02:50 $
$Author: Don Peterson $
'''

import sys, dcload
import time
try:
    from win32com.client import Dispatch
except:
    pass
err = sys.stderr.write

def TalkToLoad(load, port, baudrate):
    '''load is either a COM object or a DCLoad object.  They have the 
    same interface, so this code works with either.
 
    port is the COM port on your PC that is connected to the DC load.
    baudrate is a supported baud rate of the DC load.
    '''
    def test(cmd, results):
        if results:
            print cmd, "failed:"
            print "  ", results
            exit(1)
        else:
            print cmd
    load.Initialize(port, baudrate) # Open a serial connection
    print "Time from DC Load =", load.TimeNow()
    test("Set to remote control", load.SetRemoteControl())
    test("Set max current to 1 A", load.SetMaxCurrent(1))
    test("Set CC current to 0.0 A", load.SetCCCurrent(0.0))    
    print "Settings:"
    print "  Mode                =", load.GetMode()
    print "  Max voltage         =", load.GetMaxVoltage()
    print "  Max current         =", load.GetMaxCurrent()
    print "  Max power           =", load.GetMaxPower()
    print "  CC current          =", load.GetCCCurrent()
    print "  CV voltage          =", load.GetCVVoltage()
    print "  CW power            =", load.GetCWPower()
    print "  CR resistance       =", load.GetCRResistance()
    print "  Load on timer time  =", load.GetLoadOnTimer()
    print "  Load on timer state =", load.GetLoadOnTimerState()
    print "  Trigger source      =", load.GetTriggerSource()
    print "  Function            =", load.GetFunction()

    print
    f = open("output.txt", 'w')
    f.write("V\tA\tW\n")    
    test("Turn on load", load.TurnLoadOn())         
    i = 0.0
    while i < 0.21:
        test("Set CC current to %f A" % i, load.SetCCCurrent(i))       
        i += 0.005
        time.sleep(0.2)
        values = load.GetInputValues()
        
        
        for value in values.split("\t"):
            print "    ", value
            f.write(value.split(" ")[0])
            f.write('\t')
        f.write("\n")
    f.close()
    test("Turn off load", load.TurnLoadOff())            
    test("Set to local control", load.SetLocalControl())

def Usage():
    name = sys.argv[0]
    msg = '''Usage:  %(name)s {com|obj} port baudrate
Demonstration python script to talk to a B&K DC load either via the COM
(component object model) interface or via a DCLoad object (in dcload.py).
port is the COM port number on your PC that the load is connected to.  
baudrate is the baud rate setting of the DC load.
''' % locals()
    print msg
    exit(1)

def main():
    if len(sys.argv) != 4: 
        Usage()
    access_type = sys.argv[1]
    port        = int(sys.argv[2])
    baudrate    = int(sys.argv[3])
    if access_type == "com":
        load = Dispatch('BKServers.DCLoad85xx')
    elif access_type == "obj":
        load = dcload.DCLoad()
    else:
        Usage()
    TalkToLoad(load, port, baudrate)
    return 0

main()
