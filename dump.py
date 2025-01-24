import subprocess
import os
import time
import re
class Dump:
    def __init__(self):
        
        self.wifis = []
        self.temp = []

    def enumAPs(self, interface):
        cmd = [
             "airodump-ng", interface
            ]
        ansi_escape = re.compile(r'\x1b\[[0-9;]*[A-Za-z]')
        print("[*]Starting A.P recon...")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(2)   
        start_time = time.time()
        while True:
            print("[-]Progress: ",int(time.time() - start_time),"s" )
            output = process.stdout.readline()
            clean_line = ansi_escape.sub('', output.strip())
            if "Elapsed" in output:
                self.wifis = self.temp
                self.temp = []

            self.temp.append(clean_line.strip().split())
            print(output.strip())
            if time.time() - start_time > 15:
                print("[!]Recon complete")
                break
        self.stop_airodump(process)
        os.system("clear")
        counter = 0
        drop_list = ['BSSID', 'STATION', 'PWR', 'Rate', 'Lost', 'Frames', 'Notes', 'Probes', '']
        for i in self.wifis:
            i = i[:10] + [' '.join(i[10:])]
            if i == drop_list:
                self.wifis = self.wifis[:counter]
                break
            counter += 1
        final_list = self.wifis[2:-1]
        print(i for i in final_list)
        


    def captureHandshake(self, interface, bssid, channel):
        """
        Start the airodump-ng process and monitor for handshake.
        """
        print(f"[*] Starting airodump-ng on channel {self.channel} for BSSID {self.bssid}...")
        cmd = [
             "airodump-ng",
            "-w", output_prefix,
            "-c", str(channel),
            "--bssid", bssid,
            interface
        ]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(2)
        print("[*] Airodump-ng started. Waiting for handshake...")
        start_time = time.time()
        
        print("Output Printed")
        while True:
            output = process.stdout.readline()
            if output:
                print(output)
                if "WPA handshake:" in output:
                    print("[*]Handshake captured!")
                    break
            if time.time() - start_time > 30:
                print("[!]Timeout")
                break
        self.stop_airodump(process)
            
      

    def stop_airodump(self, process):
        # Stop the airodump-ng process.
        if process:
            print("[*] Stopping airodump-ng...")
            process.terminate()
            process.wait()
            process = None
            print("[*] Airodump-ng stopped.")

# Example Usage
if __name__ == "__main__":
        d = Dump()
        d.enumAPs("wlan0mon")