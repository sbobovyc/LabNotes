using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO.Ports;
using System.Threading;
using Driver;

namespace U1272A_Test
{
    class Program
    {
        static SerialPort serial;

        static void Main(string[] args)
        {
            U1272A meter = new U1272A("COM8");
            Console.WriteLine(meter.Identification());
            Console.WriteLine(meter.Configuration());
            Console.WriteLine(meter.Fetch());
        }
    }
}
