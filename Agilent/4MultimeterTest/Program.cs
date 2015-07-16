//#define VERBOSE
#define WITH_TEMP
//#define WITH_SIMDEBUG
//#define WITH_AUTO_STOP


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
        public const int STOP_TIME = 45; // seconds

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
            u3606a_dev1.Initialize("USBInstrument1", false, false, "");
            Agilent.AgU3606x.Interop.IAgU3606x u3606a_dev2 = new Agilent.AgU3606x.Interop.AgU3606xClass();
            u3606a_dev2.Initialize("USBInstrument2", false, false, "");
            Agilent.AgU3606x.Interop.IAgU3606x u3606a_dev3 = new Agilent.AgU3606x.Interop.AgU3606xClass();
            u3606a_dev3.Initialize("USBInstrument3", false, false, "");
            Agilent.AgU3606x.Interop.IAgU3606x u3606a_dev4 = new Agilent.AgU3606x.Interop.AgU3606xClass();
            u3606a_dev4.Initialize("USBInstrument4", false, false, "");

#if WITH_TEMP
            U1272A meter = new U1272A("COM10");
#endif
#if WITH_SIMDEBUG
            Replayer board = new Replayer("COM1");
#endif

            System.Console.WriteLine("{0},{1},{2},{3}", u3606a_dev1.Identity.InstrumentManufacturer, 
                                                        u3606a_dev1.Identity.InstrumentModel,
                                                        u3606a_dev1.Identity.Revision, 
                                                        u3606a_dev1.Identity.InstrumentFirmwareRevision
                                                        );
            System.Console.WriteLine("{0},{1},{2},{3}", u3606a_dev2.Identity.InstrumentManufacturer,
                                                        u3606a_dev2.Identity.InstrumentModel,
                                                        u3606a_dev2.Identity.Revision,
                                                        u3606a_dev2.Identity.InstrumentFirmwareRevision
                                                        );
            System.Console.WriteLine("{0},{1},{2},{3}", u3606a_dev3.Identity.InstrumentManufacturer,
                                                        u3606a_dev3.Identity.InstrumentModel,
                                                        u3606a_dev3.Identity.Revision,
                                                        u3606a_dev3.Identity.InstrumentFirmwareRevision
                                                        );
            System.Console.WriteLine("{0},{1},{2},{3}", u3606a_dev4.Identity.InstrumentManufacturer,
                                                        u3606a_dev4.Identity.InstrumentModel,
                                                        u3606a_dev4.Identity.Revision,
                                                        u3606a_dev4.Identity.InstrumentFirmwareRevision
                                                        );
#if WITH_TEMP
            System.Console.WriteLine(meter.Identification());
#endif
#if WITH_SIMDEBUG
            System.Console.WriteLine(board.getVersion());
#endif


            // max 5V, low resolution for speed
            u3606a_dev1.Voltage.DC.Configure(5, Agilent.AgU3606x.Interop.AgU3606xResolutionEnum.AgU3606xResolutionLeast);
            u3606a_dev1.Measurement.SetInitiateContinuous(true);

            // 2 A range, low resolution for speed
            u3606a_dev2.Current.DC.Configure(2, Agilent.AgU3606x.Interop.AgU3606xResolutionEnum.AgU3606xResolutionLeast);
            u3606a_dev2.Measurement.SetInitiateContinuous(true);

            // max 15V, low resolution for speed
            u3606a_dev3.Voltage.DC.Configure(15, Agilent.AgU3606x.Interop.AgU3606xResolutionEnum.AgU3606xResolutionLeast);
            u3606a_dev3.Measurement.SetInitiateContinuous(true);

            // max 15V, low resolution for speed
            u3606a_dev4.Voltage.DC.Configure(15, Agilent.AgU3606x.Interop.AgU3606xResolutionEnum.AgU3606xResolutionLeast);
            u3606a_dev4.Measurement.SetInitiateContinuous(true);

            // enable output
            u3606a_dev2.Output.Enabled = true;
            u3606a_dev3.Output.Enabled = true;
            u3606a_dev4.Output.Enabled = true;
           
            double voltage = 0;
            double current = 0;
            double Vb = 0;
            double Ve = 0;
            double temperature = 0;
            var stopwatch = Stopwatch.StartNew();
            string time;
            string line;
            var start_time = DateTime.UtcNow;

            StreamWriter log_file = File.AppendText("multimeter_debug_log.csv");
            // write header
#if WITH_SIMDEBUG
            log_file.WriteLine("Time, Voltage, Current, Vb, Ve, Vbe, R_equiv, Temp(C), xmin, xmax, Vpred, Ipred, m_meas, error, delta, Vout, Iout, Gain, OP Vout");
#else
            log_file.WriteLine("Time, Voltage, Current, Vb, Ve, Vbe, R_equiv, Temp(C)");
#endif
            u3606a_dev1.Measurement.Fetch();
            u3606a_dev2.Measurement.Fetch();
            u3606a_dev3.Measurement.Fetch();
            u3606a_dev4.Measurement.Fetch();
            try
            {
                while (keepRunning)
                {

#if VERBOSE
                    stopwatch = Stopwatch.StartNew();
#endif
                    #region ParallelTasks
                    Parallel.Invoke(() =>
                    {
                        voltage = u3606a_dev1.Measurement.Fetch();
                    },
                    () =>
                    {
                        current = u3606a_dev2.Measurement.Fetch();
                    },
                    () =>
                    {
                        Vb = u3606a_dev3.Measurement.Fetch();
                    },

                    () =>
                    {
                        Ve = u3606a_dev4.Measurement.Fetch();
                    },


                    () =>
                    {
#if WITH_TEMP
                        temperature = Convert.ToDouble(meter.Fetch());   
#endif
                    });
                    #endregion                    

                    time = DateTime.Now.ToString("hh:mm:ss.fff tt");


#if VERBOSE
                stopwatch.Stop(); 
                Console.WriteLine(stopwatch.ElapsedMilliseconds);
                Console.WriteLine(time);
                Console.WriteLine("V: {0:0.0000}", voltage);
                Console.WriteLine("I: {0:0.0000}", current);
                Console.WriteLine("Vb: {0:0.0000}", Vb);
                Console.WriteLine("Temp (C): {0:0.0000}", temperature);
#endif

#if WITH_SIMDEBUG
                    ReplayerBoard.DebugData db = board.getDebugData();                    
                    line = string.Join(", ", new string[] { time, voltage.ToString(), current.ToString(), Vb.ToString(), Ve.ToString(), (Vb-Ve).ToString(), (voltage/current).ToString(), temperature.ToString(), db.xmin.ToString(), db.xmax.ToString(), db.Vpred.ToString(), db.Ipred.ToString(), db.m_meas.ToString(), db.error.ToString(), db.delta.ToString(), db.Vout.ToString(), db.current.ToString(), db.gain.ToString(), db.operating_point_vout.ToString() });
#else
                    line = string.Join(", ", new string[] { time, voltage.ToString(), current.ToString(), Vb.ToString(), Ve.ToString(), (Vb-Ve).ToString(), (voltage/current).ToString(), temperature.ToString() });
#endif
                    Console.WriteLine(line);
                    log_file.WriteLine(line);

#if WITH_AUTO_STOP
                    if ((DateTime.UtcNow - start_time) > TimeSpan.FromSeconds(STOP_TIME))
                    {
                        keepRunning = false;
                        // disable output                        
                        u3606a_dev3.Output.Enabled = false;
                    }                            
#endif
                }
            }
            catch (AggregateException ae)
            {
                Console.WriteLine("Exception");
            }

#if WITH_AUTO_STOP
            u3606a_dev3.Output.Enabled = false;
#endif
            u3606a_dev1.Close();
            u3606a_dev2.Close();
            u3606a_dev3.Close();
            u3606a_dev4.Close();
            log_file.Close();
            Console.WriteLine("Exiting");

        }
    }
}
