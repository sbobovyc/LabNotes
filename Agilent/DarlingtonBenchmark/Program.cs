//#define VERBOSE
#define BENCHMARK_SWEEP

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

            DarlingtonTest();
            
        }
        private static void DarlingtonTest()
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
            
            U1272A meter = new U1272A("COM10");
            Replayer board = new Replayer("COM1");

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
            System.Console.WriteLine(meter.Identification());
            System.Console.WriteLine(board.getVersion());


            // max 5V, low resolution for speed
            u3606a_dev1.Voltage.DC.Configure(5, Agilent.AgU3606x.Interop.AgU3606xResolutionEnum.AgU3606xResolutionLeast);
            u3606a_dev1.Measurement.SetInitiateContinuous(true);

            // 1 A range, low resolution for speed
            u3606a_dev2.Current.DC.Configure(1, Agilent.AgU3606x.Interop.AgU3606xResolutionEnum.AgU3606xResolutionLeast);
            u3606a_dev2.Measurement.SetInitiateContinuous(true);

            // max 15V, low resolution for speed
            u3606a_dev3.Voltage.DC.Configure(15, Agilent.AgU3606x.Interop.AgU3606xResolutionEnum.AgU3606xResolutionLeast);
            u3606a_dev3.Measurement.SetInitiateContinuous(true);

            // max 15V, low resolution for speed
            u3606a_dev4.Voltage.DC.Configure(15, Agilent.AgU3606x.Interop.AgU3606xResolutionEnum.AgU3606xResolutionLeast);
            u3606a_dev4.Measurement.SetInitiateContinuous(true);

            float Ve_board;
            float Ve_max;
            float Ve_min;
            float Ve_delta;
            float Vb_board;
            float Vbe_on;
            float Vbe_sat;
            float Vb_delta;
            bool low_power = false;
            double voltage = 0;
            double current = 0;
            double Vb = 0;
            double Ve = 0;
            double temperature = 0;
            var stopwatch = Stopwatch.StartNew();
            string time;
            string line;
            
            //board.setVE(Ve_board);
            //board.setVB(Vb_board);

            // set amp gain to lowest
            board.setGain(AD8253.GAIN_1);

            StreamWriter log_file = File.AppendText("multimeter_log.csv");
            // write header
            if (new FileInfo("multimeter_log.csv").Length == 0)
            {
                log_file.WriteLine("Time, Voltage, Current, Vb, Ve, Vbe, R_equiv, Temp(C)");
            }
            // set parameters
            if (low_power)
            {
                Ve_max = 6.5F;
                Ve_min = 6.0F;
                Ve_delta = 0.5F;
                Vbe_on = 0.6F;
                Vbe_sat = 1.3F;
                Vb_delta = 0.003F;
            }
            else
            {
                Ve_max = 10.0F;
                Ve_min = 9.5F;
                Ve_delta = 0.5F;
                Vbe_on = 1.2F;
                Vbe_sat = 1.3F;
                Vb_delta = 0.0005F;
            }
            try
            {
#if BENCHMARK_SWEEP
                for (Ve_board = Ve_max; Ve_board > Ve_min; Ve_board -= Ve_delta)
                {
                    board.setVE(Ve_board);
                    for (Vb_board = Ve_board - Vbe_on; Vb_board > Ve_board - Vbe_sat; Vb_board -= Vb_delta)
                    {
                        for (int i = 0; i < 1; i++)
                        {
                            board.setVB(Vb_board);
                            System.Console.WriteLine("Ve: {0}, Vb: {1}", Ve_board, Vb_board);
                            Thread.Sleep(3000);

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
                                temperature = Convert.ToDouble(meter.Fetch());
                            });
                            #endregion

                            //time = DateTime.Now.ToLongTimeString();
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

                            line = string.Join(", ", new string[] { time, voltage.ToString(), current.ToString(), Vb.ToString(), Ve.ToString(), (Vb - Ve).ToString(), (voltage / current).ToString(), temperature.ToString() });
                            Console.WriteLine(line);
                            log_file.WriteLine(line);                            

                            if (!keepRunning)
                                goto Exit;
                        }
                    }
                }

#endif
            }
            catch (AggregateException ae)
            {
                Console.WriteLine("Exception");
            }

            Exit:
            // put in cutoff
            board.setVE(4.0F);
            board.setVB(4.0F);


            u3606a_dev1.Close();
            u3606a_dev2.Close();
            u3606a_dev3.Close();
            u3606a_dev4.Close();
            log_file.Close();
            Console.WriteLine("Exiting");

        }
    }
}
