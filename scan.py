from monitor import Monitor
from dump import Dump
import subprocess
class PayloadDriver:
    def __init__(self):
        self.interfaces = []
        self.active_interface = None
    def getInterfaces(self):
        iface_info = subprocess.run(["iwconfig"], capture_output=True, text=True)
        split_iface_info = str(iface_info.stdout).splitlines()
        for line in split_iface_info:
            if not line.strip():
                continue
        
            if "IEEE" in line:
                curr_iface = line.split()
                self.interfaces.append(curr_iface[0])

    def selectInterface(self):
        if len(self.interfaces) == 0:
            print("[!]No interfaces detected")
            return
        for i in range(len(self.interfaces)):
            print(i, ". ", self.interfaces[i])
        while True:
            self.active_interface = input("[?]Interface:")
            if self.active_interface not in self.interfaces:
                self.active_interface = None
            else:
                break
        
main = PayloadDriver()
main.getInterfaces()
main.selectInterface()

