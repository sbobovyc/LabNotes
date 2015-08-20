import bluetooth
import sys
from Tkinter import *

device_dict = {}

def connect(addr):
    services = bluetooth.find_service(address=addr)
    if len(services) > 0:
        print("found %d services" % len(services))
        print()
    else:
        print("no services found")

    for svc in services:
        print("Service Name: %s"    % svc["name"])
        print("    Host:        %s" % svc["host"])
        print("    Description: %s" % svc["description"])
        print("    Provided By: %s" % svc["provider"])
        print("    Protocol:    %s" % svc["protocol"])
        print("    channel/PSM: %s" % svc["port"])
        print("    svc classes: %s "% svc["service-classes"])
        print("    profiles:    %s "% svc["profiles"])
        print("    service id:  %s "% svc["service-id"])
        print()

        host = svc["host"]
        port = svc["port"]
        import binascii
        print binascii.hexlify(svc["name"])
        if svc["protocol"] == "RFCOMM" and svc["name"] == "AMP-SPP\x00":
            print("Trying to connect")
            sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
            sock.connect((host, port))
            total_size = 0
            while True:
                data = sock.recv(1024)
                total_size += len(data)
                print "received [%s], size %i" % (data, total_size)
            sock.close()

        
def connectClick():
    connect(device_dict[var.get()])
    master.destroy()
    sys.exit(0)


if __name__ ==  "__main__":
    print("performing inquiry...")

    nearby_devices = bluetooth.discover_devices(lookup_names = True)

    print("found %d devices" % len(nearby_devices))
    print(nearby_devices)

    for addr, name in nearby_devices:
        print("  %s - %s" % (addr, name))
        device_dict[name] = addr

    master = Tk()

    var = StringVar(master)
    options=[dev[1] for dev in nearby_devices]
    var.set(options[0]) # default value
    w = OptionMenu(master, var, *options)
    w.pack()


    button = Button(master, text="Connect", command=connectClick)
    button.pack()

mainloop()


