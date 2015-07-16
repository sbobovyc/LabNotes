using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.IO.Ports;

namespace ReplayerBoard
{
    public enum ReplayerMessages
    {
        SET_VB = 0x00000001,
        SET_VE = 0x00000002,
        SET_GAIN = 0x00000003,
        DONE = 0x0000000F,
    }

    public enum AD8253
    {
        GAIN_1 = 1,       /// Amplifier gain 1
        GAIN_10 = 10,      /// Amplifier gain 10
        GAIN_100 = 100,     /// Amplifier gain 100
        GAIN_1000 = 1000,    /// Amplifier gain 1000
    }

    public class DebugData
    {
        public float xmin;
        public float xmax;
        public float Vpred;
        public float Ipred;
        public float m_meas;
        public float error;
        public float delta;
        public float Vout;
        public float current;
        public Int16 gain;
        public float operating_point_vout;

        public DebugData(byte[] data)
        {
            xmin = BitConverter.ToSingle(data, 0);
            xmax = BitConverter.ToSingle(data, 4);
            Vpred = BitConverter.ToSingle(data, 8);
            Ipred = BitConverter.ToSingle(data, 12);
            m_meas = BitConverter.ToSingle(data, 16);
            error = BitConverter.ToSingle(data, 20);
            delta = BitConverter.ToSingle(data, 24);
            Vout = BitConverter.ToSingle(data, 28);
            current = BitConverter.ToSingle(data, 32);
            gain = BitConverter.ToInt16(data, 36);
            operating_point_vout = BitConverter.ToSingle(data, 38);
        }
    }


    public class Replayer
    {
        static SerialPort serial;

        public Replayer(string portName)
        {
            serial = new SerialPort(portName, 9600, Parity.None, 8, StopBits.One);
            serial.Open();
        }

        private void send(byte[] data)
        {
            serial.Write(data, 0, 8);
            Thread.Sleep(20);
            serial.Read(new byte[8], 0, 8);
        }

        public void setVB(float voltage)
        {
            byte[] message = BitConverter.GetBytes((Int32)ReplayerMessages.SET_VB);
            byte[] value = BitConverter.GetBytes(voltage);
            byte[] data = message.Concat(value).ToArray();
            //System.Console.WriteLine(data.Length);
            //System.Console.WriteLine(BitConverter.ToString(data));
            this.send(data);
        }

        public void setVE(float voltage)
        {
            byte[] message = BitConverter.GetBytes((Int32)ReplayerMessages.SET_VE);
            byte[] value = BitConverter.GetBytes(voltage);
            byte[] data = message.Concat(value).ToArray();
            //System.Console.WriteLine(data.Length);
            //System.Console.WriteLine(BitConverter.ToString(data));
            this.send(data);
        }

        public void setGain(AD8253 gain)
        {
            byte[] message = BitConverter.GetBytes((Int32)ReplayerMessages.SET_GAIN);
            byte[] value = BitConverter.GetBytes((Int32)gain);
            byte[] data = message.Concat(value).ToArray();
            this.send(data);
        }

        public void cutOff()
        {
            this.setVE(10.0F);
            this.setVB(10.0F);
        }

        public string getVersion()
        {
            //TODO
            return "Replayer version here";
        }

        public DebugData getDebugData()
        {
            byte[] buffer = new byte[48];
            //System.Console.WriteLine(serial.BytesToRead);
            for (int i = 0; i < 48; i++)
            {
                buffer[i] = (byte)serial.ReadByte();
            }            
            System.Console.WriteLine(BitConverter.ToString(buffer));
            return new DebugData(buffer);
        }

        ~Replayer()
        {
            serial.Close();
        }
    }
}
