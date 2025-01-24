import subprocess
import os

class AircrackWrapper:
    def __init__(self, cap_file, wordlists):
        """
        Initialize the automation tool.
        :param cap_file: Path to the .cap file containing the captured handshake.
        :param wordlists: List of wordlist files to try.
        """
        self.cap_file = cap_file
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
        Run aircrack-ng with a single wordlist.
        :param wordlist: Path to the wordlist file.
        :return: True if a key is found, False otherwise.
        """
        print(f"[*] Trying wordlist: {wordlist}...")
        aircrack_cmd = [
            "sudo", "aircrack-ng",
            "-w", wordlist,  # Specify the wordlist file
            self.cap_file    # Specify the .cap file
        ]

        try:
            # Capture output from aircrack-ng
            result = subprocess.run(
                aircrack_cmd, text=True, capture_output=True
            )
            output = result.stdout

            # Check if a key was found
            if "KEY FOUND!" in output:
                print("[+] Key successfully cracked!")
                print(output.splitlines()[-1])  # Print the cracked key
                return True
            else:
                print("[-] Key not found with this wordlist.")
                return False
        except Exception as e:
            print(f"[!] An error occurred: {e}")
            return False

    def start_cracking(self):
        """
        Start the cracking process, trying each wordlist in sequence.
        """
        if not self.validate_files():
            return

        for wordlist in self.wordlists:
            if self.run_aircrack(wordlist):
                print("[+] Stopping as the key has been cracked.")
                break
        else:
            print("[-] Exhausted all wordlists. No key found.")

if __name__ == "__main__":
    # Example usage
    cap_file = input("Enter the path to the .cap file (e.g., handshake.cap): ")
    wordlists = input("Enter paths to wordlists, separated by commas (e.g., wordlist1.txt,wordlist2.txt): ").split(",")

    aircrack = AircrackWrapper(cap_file, wordlists)
    aircrack.start_cracking()
