from monitor import MonitorMode
from interface import Interface
from dump import Dump
import subprocess

ifs = Interface()
#select interfaces
ifaces = ifs.getInterfaces()
if len(ifaces) == 0:
    exit(0)

while True:    
    for i in range (len(ifaces)):
        print(i+1, ". ", ifaces[i])
    active_iface_no = int(input("[?]Interface no. : "))
    if active_iface_no <= len(ifaces) and active_iface_no >= 1:
        break
    else:
        active_iface_no = None
        
active_interface = ifs.selectInterface(active_iface_no - 1)

#start monitor mode
mon = MonitorMode(active_interface)
mon.startMonitorMode()
active_interface = ifs.selectInterface()
print(ifs.getInterfaces())

#Get APs and Clients
d = Dump()
d.enumAPs(interface = active_interface)

#stop monitor mode
mon.stopMonitorMode()
active_interface = ifs.selectInterface()
print(ifs.getInterfaces())
