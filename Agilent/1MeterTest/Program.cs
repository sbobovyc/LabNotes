
using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Threading;

using Ivi.Driver.Interop;

using Driver;
using ReplayerBoard;

namespace MultimeterTest
{
    class Program
    {
        private static bool keepRunning = true;

        #region unmanaged

        /// <summary>
        /// This function sets the handler for kill events.
        /// </summary>
        /// <param name="Handler"></param>
        /// <param name="Add"></param>
        /// <returns></returns>
        [DllImport("Kernel32")]
        public static extern bool SetConsoleCtrlHandler(HandlerRoutine Handler, bool Add);

        //delegate type to be used of the handler routine
        public delegate bool HandlerRoutine(CtrlTypes CtrlType);

        // control messages
        public enum CtrlTypes
        {
            CTRL_C_EVENT = 0,
            CTRL_BREAK_EVENT,
            CTRL_CLOSE_EVENT,
            CTRL_LOGOFF_EVENT = 5,
            CTRL_SHUTDOWN_EVENT
        }

        #endregion
        /// <summary>
        /// This method will be called if the user closes the console window or presses CTRL+C
        /// </summary>
        /// <param name="ctrlType"></param>
        /// <returns>always true</returns>
        private static bool ConsoleCtrlCheck(CtrlTypes ctrlType)
        {
            // TODO: implement exit handler routine
            Console.WriteLine("Handler");
            keepRunning = false;
            return true;
        }

        static void Main(string[] args)
        {
            HandlerRoutine hr = new HandlerRoutine(ConsoleCtrlCheck);
            // we have to keep the handler routine alive during the execution of the program,
            // because the garbage collector will destroy it after any CTRL event
            GC.KeepAlive(hr);
            SetConsoleCtrlHandler(hr, true);
            Console.WriteLine("Press any key to start measurements");
            Console.ReadKey();

            VoltageTest();

        }
        private static void VoltageTest()
        {
            System.Console.WriteLine("Connecting to instruments");
            Agilent.AgU3606x.Interop.IAgU3606x u3606a_dev1 = new Agilent.AgU3606x.Interop.AgU3606xClass();
            //Agilent.AgU3606x.Interop.IAgU3606x u3606a_dev2 = new Agilent.AgU3606x.Interop.AgU3606xClass();
            u3606a_dev1.Initialize("USBInstrument1", false, false, "");
            //u3606a_dev2.Initialize("USBInstrument2", false, false, "");


            System.Console.WriteLine("{0},{1},{2},{3}", u3606a_dev1.Identity.InstrumentManufacturer,
                                                        u3606a_dev1.Identity.InstrumentModel,
                                                        u3606a_dev1.Identity.Revision,
                                                        u3606a_dev1.Identity.InstrumentFirmwareRevision
                                                        );
           // System.Console.WriteLine("{0},{1},{2},{3}", u3606a_dev2.Identity.InstrumentManufacturer,
            //                                            u3606a_dev2.Identity.InstrumentModel,
             //                                           u3606a_dev2.Identity.Revision,
              //                                          u3606a_dev2.Identity.InstrumentFirmwareRevision
                //                                        );

            // enable output
            u3606a_dev1.Output.Enabled = true;
            System.Threading.Thread.Sleep(100);


            // 2 A range, low resolution for speed
            u3606a_dev1.Current.DC.Configure(1, Agilent.AgU3606x.Interop.AgU3606xResolutionEnum.AgU3606xResolutionLeast);
            u3606a_dev1.Measurement.SetInitiateContinuous(true);    
            
            double current = 0;
            var stopwatch = Stopwatch.StartNew();
            string time;
            string line;
            var start_time = DateTime.UtcNow;

            StreamWriter log_file = File.AppendText("multimeter_debug_log.csv");
            // write header
            log_file.WriteLine("Time, Current");
            u3606a_dev1.Measurement.Fetch();
            try
            {
                while (keepRunning)
                {

                    current = u3606a_dev1.Measurement.Fetch();

                    time = DateTime.Now.ToString("hh:mm:ss.fff tt");

                    line = string.Join(", ", new string[] { time, current.ToString() });
                    Console.WriteLine(line);
                    log_file.WriteLine(line);

                }
            }
            catch (AggregateException ae)
            {
                Console.WriteLine("Exception");
                goto exit;
            }

            exit:
            u3606a_dev1.Output.Enabled = false;
            u3606a_dev1.Close();
            //u3606a_dev2.Close();
            log_file.Close();
            Console.WriteLine("Exiting");

        }
    }
}
