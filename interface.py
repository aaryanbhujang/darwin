import subprocess
class Interface:
    def __init__(self):
        self.interfaces = []
        self.active_interface = None
        self.default_choice = None
    def getInterfaces(self):
        self.interfaces = []
        iface_info = subprocess.run(["iwconfig"], capture_output=True, text=True)
        split_iface_info = str(iface_info.stdout).splitlines()
        for line in split_iface_info:
            if not line.strip():
                continue
        
            if "IEEE" in line:
                curr_iface = line.split()
                self.interfaces.append(curr_iface[0])
            return self.interfaces

    def selectInterface(self, serial = None):
        if len(self.interfaces) == 0:
            print("[!]No interfaces detected")
            return None
        if serial is not None:
            self.default_choice = serial

        serial = serial if serial is not None else self.default_choice
        self.active_interface = self.getInterfaces()[serial]
        return self.active_interface
