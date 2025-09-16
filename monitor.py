import subprocess 
class MonitorMode:
    def __init__(self, interface):
        self.interface = interface
    def startMonitorMode(self):
        output = subprocess.run(["airmon-ng", "start", self.interface], capture_output=True, text=True)
        print(output.stdout)
        if "does not exist" in output.stdout:
            print("[!]ERROR: Interface not detected", output.stdout)
    def stopMonitorMode(self):
        output = subprocess.run(["airmon-ng", "stop", self.interface + "mon"], capture_output=True, text=True)
        print(output.stdout)
        if "does not exist" in output.stdout:
            print("[!]ERROR: Interface not detected", output.stdout)