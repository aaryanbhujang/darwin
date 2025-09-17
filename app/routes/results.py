import pandas as pd
from flask import Blueprint, jsonify, current_app
from datetime import datetime

result_bp = Blueprint("result", __name__)

def load_scan_data():
    """Load WiFi scan results from Excel file."""
    excel_path = current_app.config.get("SCAN_EXCEL", "../wifi_scan.xlsx")
    df = pd.read_excel(excel_path)

    # normalize column names (avoid case mismatches)
    df.columns = [c.strip().upper() for c in df.columns]
    print(df.columns)
    # enforce expected fields
    for col in ["ESSID", "BSSID", "Privacy", "First time seen"]:
        if col not in df.columns:
            raise ValueError(f"Missing expected column: {col}")

    return df


@result_bp.route("/stats", methods=["GET"])
def get_stats_from_excel():
    df = load_scan_data()

    # --- Pie chart ---
    pie_chart = df["Privacy"].fillna("UNKNOWN").value_counts().to_dict()

    # --- Line chart (encryption trend over time) ---
    # bucket by minute
    df["First time seen"] = pd.to_datetime(df["First time seen"], errors="coerce")
    df["BUCKET"] = df["First time seen"].dt.floor("T")
    trend = (
        df.groupby(["BUCKET", "Privacy"])
        .size()
        .reset_index(name="count")
        .pivot(index="BUCKET", columns="Privacy", values="count")
        .fillna(0)
        .reset_index()
    )
    line_chart = []
    for _, row in trend.iterrows():
        entry = {"time": row["BUCKET"].isoformat()}
        for col in trend.columns:
            if col != "BUCKET":
                entry[col if col else "UNKNOWN"] = int(row[col])
        line_chart.append(entry)

    # --- Anomalies & Findings ---
    anomalies, findings = set(), []
    vulnerable_count = 0

    for _, r in df.iterrows():
        essid = str(r.get("ESSID", "")).strip() or None
        bssid = str(r.get("BSSID", "")).strip() or None
        enc = str(r.get("Privacy", "")) if r.get("Privacy") else "UNKNOWN"

        issue = None
        if enc in ("OPEN", "UNKNOWN", ""):
            issue = "OPEN network"
        elif enc in ("WEP", "WPA"):
            issue = f"Weak encryption ({enc})"

        if issue:
            anomalies.add(f"{issue} detected: {essid or bssid}")
            findings.append({"essid": essid, "bssid": bssid, "issue": issue})
            vulnerable_count += 1

    # --- Metrics ---
    total_aps = len(df)
    risk_score = int((vulnerable_count / max(total_aps, 1)) * 100)

    metrics = {
        "total_aps": total_aps,
        "vulnerable_aps": vulnerable_count,
        "risk_score": risk_score,
    }

    return jsonify(
        {
            "line_chart": line_chart,
            "pie_chart": pie_chart,
            "anomalies": list(anomalies),
            "findings": findings,
            "metrics": metrics,
        }
    )
