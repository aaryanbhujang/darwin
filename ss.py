import subprocess
output = subprocess.run(["airmon-ng", "start", "wlan0"], capture_output=True, text=True)
if "does not exist" in output.stdout:
    print("[!]ERROR:", output.stdout)