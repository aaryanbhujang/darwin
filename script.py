from flask import Flask, render_template, redirect, url_for, jsonify, request
import subprocess
import re
from collections import Counter

app = Flask(__name__)

# in-memory store (start with some demo data)
wifi_networks = [
    {"id": 1, "ssid": "HomeNet", "wifi_name": "Home Router", "encryption": "WPA2", "channel": "6",  "speed": "150 Mb/s", "cipher": "CCMP", "power": "-45 dBm"},
    {"id": 2, "ssid": "OfficeNet", "wifi_name": "Office AP",  "encryption": "WPA3", "channel": "36", "speed": "300 Mb/s", "cipher": "GCMP", "power": "-60 dBm"},
    {"id": 3, "ssid": "CafeFree", "wifi_name": "Cafe AP",    "encryption": "Open", "channel": "11", "speed": "54 Mb/s",  "cipher": "-",     "power": "-78 dBm"},
]

def parse_iwlist_output(output):
    """Parse iwlist scan output to a list of network dicts (best-effort)."""
    networks = []
    cells = output.split("Cell ")
    for idx, cell in enumerate(cells[1:], start=1):
        ssid = re.search(r'ESSID:"([^"]+)"', cell)
        ssid = ssid.group(1) if ssid else "Unknown"

        enc = "Open"
        if re.search(r'Encryption key:on', cell) or re.search(r'IE: WPA', cell) or re.search(r'WPA2', cell, re.I):
            # try to provide a friendly label
            if re.search(r'WPA2|WPA-2|IEEE 802.11i', cell, re.I):
                enc = "WPA2"
            elif re.search(r'WPA3', cell, re.I):
                enc = "WPA3"
            else:
                enc = "WPA"

        channel = (re.search(r'Channel:(\d+)', cell).group(1) if re.search(r'Channel:(\d+)', cell) else "-")
        speed = (re.search(r'Bit Rates:(.+)', cell).group(1).strip() if re.search(r'Bit Rates:(.+)', cell) else "-")
        cipher = (re.search(r'Group Cipher\s*: (.+)', cell) or re.search(r'Pairwise Ciphers \(.*\):\s*(.+)', cell))
        cipher = cipher.group(1).strip() if cipher else "-"
        signal = (re.search(r'Signal level=(-?\d+)', cell) or re.search(r'Signal level=(-?\d+) dBm', cell))
        power = (signal.group(1) + " dBm") if signal else "-"

        networks.append({
            "id": idx,
            "ssid": ssid,
            "wifi_name": ssid,
            "encryption": enc,
            "channel": channel,
            "speed": speed,
            "cipher": cipher,
            "power": power
        })
    return networks

def do_scan(interface="wlan0"):
    """
    Attempt to scan using iwlist. If it fails (no permission or interface),
    return demo/fallback data.
    """
    try:
        # Note: iwlist needs root privileges; if you run as non-root, this may raise
        raw = subprocess.check_output(["sudo", "iwlist", interface, "scan"], stderr=subprocess.STDOUT, text=True, timeout=12)
        parsed = parse_iwlist_output(raw)
        if parsed:
            return parsed
    except Exception as e:
        app.logger.debug("iwlist scan failed: %s", e)

    # fallback: return sample data (or preserve existing wifi_networks)
    return [
        {"id": 1, "ssid": "DemoNet1", "wifi_name": "Demo Router 1", "encryption": "WPA2", "channel": "1",  "speed": "150 Mb/s", "cipher": "CCMP", "power": "-43 dBm"},
        {"id": 2, "ssid": "DemoNet2", "wifi_name": "Demo Router 2", "encryption": "WPA2", "channel": "6",  "speed": "300 Mb/s", "cipher": "GCMP", "power": "-62 dBm"},
        {"id": 3, "ssid": "DemoOpen", "wifi_name": "Coffee Shop",   "encryption": "Open", "channel": "11", "speed": "54 Mb/s",  "cipher": "-",     "power": "-78 dBm"},
    ]

@app.route("/")
def dashboard():
    # ensure wifi_networks referenced is the in-memory store
    global wifi_networks
    total_networks = len(wifi_networks)

    # Build encryption distribution
    enc_list = [net.get("encryption", "Unknown") for net in wifi_networks]
    enc_counter = Counter(enc_list)
    encryption_labels = list(enc_counter.keys())
    encryption_data = list(enc_counter.values())

    return render_template(
        "index.html",
        total_networks=total_networks,
        networks=wifi_networks,
        encryption_labels=encryption_labels,
        encryption_data=encryption_data
    )

@app.route("/scan_wifi", methods=["POST"])
def scan_wifi_route():
    global wifi_networks
    wifi_networks = do_scan(interface="wlan0")  # change interface if needed
    return redirect(url_for("dashboard"))

@app.route("/show_wifi", methods=["POST"])
def show_wifi_route():
    # For now it just redirects back to dashboard (placeholder)
    return redirect(url_for("dashboard"))

@app.route("/api/wifi")
def api_wifi():
    return jsonify(wifi_networks)

if __name__ == "__main__":
    app.run(debug=True)
