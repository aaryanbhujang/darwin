from flask import Blueprint, request, jsonify, current_app
import pandas as pd
import os
from datetime import datetime

# your modules
from monitor import MonitorMode
from interface import Interface
from dump import Dump

scanner_bp = Blueprint("scanner", __name__)

@scanner_bp.route("/submit", methods=["POST"])
def submit_scan():
    """
    Trigger WiFi scan using the custom Monitor/Interface/Dump modules.
    Saves results to Excel and returns basic summary JSON.
    """
    try:
        ifs = Interface()
        ifaces = ifs.getInterfaces()
        if not ifaces:
            return jsonify({"error": "No interfaces detected"}), 400

        # pick interface (for MVP: first one, or configurable)
        active_iface = ifs.selectInterface(0)

        # start monitor mode
        mon = MonitorMode(active_iface)
        mon.startMonitorMode()
        active_iface = ifs.selectInterface()

        # run dump
        d = Dump()
        results = d.enumAPs(interface=active_iface)  # assume this returns list[dict]

        # stop monitor mode
        mon.stopMonitorMode()
        active_iface = ifs.selectInterface()

        # save results to Excel for the /results/stats endpoint
        out_dir = current_app.config.get("SCAN_OUTPUT_DIR", "scans")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")

        df = pd.DataFrame(results)
        df.to_excel(out_path, index=False)

        # also update "latest" pointer
        current_app.config["SCAN_EXCEL"] = out_path

        return jsonify({
            "status": "success",
            "message": "Scan completed",
            "results_file": out_path,
            "summary": {
                "total_aps": len(df),
                "columns": list(df.columns),
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
