import subprocess
import os
import csv
import re
from datetime import datetime

class AircrackWrapper:
    def __init__(self, cap_file, bssid, wordlists):
        """
        Initialize the automation tool.
        :param cap_file: Path to the .cap file containing the captured handshake.
        :param bssid: Target AP BSSID to scope cracking.
        :param wordlists: List of wordlist files to try.
        """
        self.cap_file = cap_file
        self.bssid = bssid
        self.wordlists = wordlists

    def validate_files(self):
        """
        Validate if the .cap file and wordlists exist.
        """
        if not os.path.exists(self.cap_file):
            print(f"[!] Capture file '{self.cap_file}' does not exist!")
            return False

        for wordlist in self.wordlists:
            if not os.path.exists(wordlist):
                print(f"[!] Wordlist file '{wordlist}' does not exist!")
                return False

        return True

    def run_aircrack(self, wordlist):
        """
        Run aircrack-ng with a single wordlist and BSSID filter.
        :param wordlist: Path to the wordlist file.
        :return: Tuple (found:bool, password:str or None)
        """
        print(f"[*] Trying wordlist: {wordlist} against BSSID: {self.bssid} ...")
        aircrack_cmd = [
            "aircrack-ng",
            "-w", wordlist,      # Specify the wordlist file
            "-b", self.bssid,    # Limit cracking to this BSSID
            self.cap_file        # Specify the .cap file
        ]

        try:
            result = subprocess.run(aircrack_cmd, text=True, capture_output=True)
            output = result.stdout + "\n" + result.stderr

            if "KEY FOUND!" in output:
                m = re.search(r"KEY FOUND!\s+\[([^\]]+)\]", output)
                password = m.group(1) if m else output.splitlines()[-1].strip()
                print("[+] Key successfully cracked!")
                print(password)
                return True, password
            else:
                print("[-] Key not found with this wordlist.")
                return False, None
        except Exception as e:
            print(f"[!] An error occurred: {e}")
            return False, None

    def run_and_save(self, wordlist):
        """
        Run aircrack with the provided wordlist and save any found key to passwords.csv.
        """
        found, password = self.run_aircrack(wordlist)
        if found and password:
            csv_file = "passwords.csv"
            header = ["timestamp", "cap_file", "bssid", "wordlist", "password"]
            row = [datetime.utcnow().isoformat(), os.path.abspath(self.cap_file), self.bssid, wordlist, password]
            write_header = not os.path.exists(csv_file)
            try:
                with open(csv_file, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    if write_header:
                        writer.writerow(header)
                    writer.writerow(row)
                print(f"[+] Saved cracked password to {csv_file}")
            except Exception as e:
                print(f"[!] Failed to write to {csv_file}: {e}")
            return True
        return False

    def start_cracking(self):
        """
        Start the cracking process, trying each wordlist in sequence.
        """
        if not self.validate_files():
            return

        for wordlist in self.wordlists:
            if self.run_aircrack(wordlist)[0]:
                print("[+] Stopping as the key has been cracked.")
                break
        else:
            print("[-] Exhausted all wordlists. No key found.")

if __name__ == "__main__":
    cap_file = input("Enter the path to the .cap file (e.g., handshake.cap): ")
    bssid = input("Enter the target BSSID (e.g., AA:BB:CC:DD:EE:FF): ").strip()
    wordlists = input("Enter paths to wordlists, separated by commas (e.g., wordlist1.txt,wordlist2.txt): ").split(",")
    wordlists = [w.strip() for w in wordlists if w.strip()]

    aircrack = AircrackWrapper(cap_file, bssid, wordlists)
    aircrack.start_cracking()
