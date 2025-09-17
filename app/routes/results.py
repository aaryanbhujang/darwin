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
    for col in ["ESSID", "BSSID", "PRIVACY", "FIRST TIME SEEN"]:
        if col not in df.columns:
            raise ValueError(f"Missing expected column: {col}")

    return df


@result_bp.route("/stats", methods=["GET"])
def get_stats_from_excel():
    df = load_scan_data()

    # --- Pie chart ---
    pie_chart = df["PRIVACY"].fillna("UNKNOWN").value_counts().to_dict()

    # --- Line chart (encryption trend over time) ---
    # choose granularity depending on your data
    df["FIRST TIME SEEN"] = pd.to_datetime(df["FIRST TIME SEEN"], errors="coerce")

    # try seconds if you want finer granularity
    df["BUCKET"] = df["FIRST TIME SEEN"].dt.floor("5S")  # 5-second intervals

    trend = (
        df.groupby(["BUCKET", "PRIVACY"])
        .size()
        .reset_index(name="count")
        .pivot(index="BUCKET", columns="PRIVACY", values="count")
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
    issue = None

    for _, r in df.iterrows():
        essid = str(r.get("ESSID", "")).strip() or None
        bssid = str(r.get("BSSID", "")).strip() or None
        enc = str(r.get("PRIVACY", "")).strip().upper() or "UNKNOWN"
        issue = None
        print(enc)
        if enc == "OPN":
            issue = "OPEN network"
            
        elif enc in ("WEP", "WPA"):
            issue = f"Weak encryption ({enc})"
        print(f"ESSID={essid}, BSSID={bssid}, PRIVACY={enc}, ISSUE={issue}")
        if issue:
            anomalies.add(f"{issue} detected: {essid or bssid}")
            vulnerable_count += 1
        findings.append({"essid": essid, "bssid": bssid, "issue": issue})
            

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
