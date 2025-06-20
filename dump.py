import subprocess
import time
import os
import csv
import glob
from openpyxl import Workbook

class Dump:
    def __init__(self):
        self.wifis = []

    def enumAPs(self, interface="wlan0mon", duration=15, output_prefix="scan_output"):
        print(f"[*] Starting airodump-ng on {interface} for {duration} seconds...")

        # Clean up old CSVs
        for f in glob.glob(f"{output_prefix}-01.csv"):
            os.remove(f)

        cmd = [
            "airodump-ng",
            "--write", output_prefix,
            "--write-interval", "1",
            "--output-format", "csv",
            interface
        ]

        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        try:
            time.sleep(duration)
            self.stop_airodump(process)
        except KeyboardInterrupt:
            self.stop_airodump(process)

        print("[*] Recon complete. Parsing CSV...")

        csv_file = f"{output_prefix}-01.csv"
        if os.path.exists(csv_file):
            self.export_to_excel(csv_file)
        else:
            print("[!] No CSV output found. Did airodump-ng run properly?")

    def stop_airodump(self, process):
        if process:
            print("[*] Stopping airodump-ng...")
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
            print("[*] Airodump-ng stopped.")

    def export_to_excel(self, csv_file, output_excel="wifi_scan.xlsx"):
        with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            rows = [row for row in reader if any(cell.strip() for cell in row)]

        ap_data = []
        client_data = []
        reading_clients = False

        for row in rows:
            if row and "Station MAC" in row[0]:
                reading_clients = True
                continue
            if not reading_clients:
                ap_data.append(row)
            else:
                client_data.append(row)

        wb = Workbook()

        # Write Access Points
        ws_ap = wb.active
        ws_ap.title = "Access_Points"
        for row in ap_data:
            ws_ap.append(row)

        # Write Clients
        ws_clients = wb.create_sheet(title="Clients")
        for row in client_data:
            ws_clients.append(row)

        wb.save(output_excel)
        print(f"[+] Data saved to Excel file: {output_excel}")

# Example usage
if __name__ == "__main__":
    d = Dump()
    d.enumAPs()
