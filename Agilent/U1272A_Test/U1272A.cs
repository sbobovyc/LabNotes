using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO.Ports;
using System.Threading;

namespace Driver
{
    class U1272A
    {
        static SerialPort serial;

        public U1272A(string portName) 
        {
            serial = new SerialPort(portName, 9600, Parity.None, 8, StopBits.One);
            serial.Open();
        }


        public string Identification() 
        {
            serial.Write("*IDN?\n");
            Thread.Sleep(50);
            return serial.ReadLine();
        }

        public string Configuration()
        {
            serial.Write("CONF?\n");
            Thread.Sleep(50);
            return serial.ReadLine();
        }

        public string Fetch()
        {
            serial.Write("FETC?\n");
            Thread.Sleep(50);
            return serial.ReadLine();
        }

        ~U1272A()
        {
            serial.Close();
        }
    }
}
