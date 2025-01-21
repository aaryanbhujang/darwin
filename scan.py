from monitor import Monitor
from interface import Interface
#from dump import Dump
import subprocess

ifs = Interface()
#select interfaces
ifaces = ifs.getInterfaces()
if len(ifaces) == 0:
    print("[!]No interfaces detected. Exiting")
    exit(0)

while True:    
    for i in range (len(ifaces)):
        print(i+1, ". ", ifaces[i])
    active_iface_no = int(input("[?]Interface no.:"))
    if active_iface_no < len(ifaces) and active_iface_no >= 0:
        break
    else:
        active_iface_no = None
active_interface = ifs.selectInterface(active_iface_no)
#start monitor mode
mon = Monitor()
mon.startMonitorMode(active_interface)
active_interface = ifs.selectInterface()
print(ifs.getInterfaces())

#stop monitor mode
mon.stopMonitorMode(active_interface)
active_interface = ifs.selectInterface()
print(ifs.getInterfaces())
