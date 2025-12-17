# DARWIN — Drone for Access-Point Reconnaissance Warflying Infiltration and Neutralization

**DARWIN** is a modular wireless reconnaissance and security analysis framework that **discovers, characterizes, and prioritizes Wi-Fi vulnerabilities** based on real-world impact. It bridges automated scanning with context-aware risk scoring to help defenders focus on what matters.  
*Designed for ethical assessments, enterprise labs, and advanced security research.*

---

## 🚀 Features

### 🔍 Wireless Discovery & Monitoring
- Passive and active scanning of Wi-Fi access points and clients  
- Signal-based geolocation heuristics  
- Monitor/Scan modes supporting channel hopping and interface control

### 📊 Contextual Vulnerability Prioritization
- Distinguishes high-impact risks (critical assets, open infrastructure) from low-impact noise  
- Generates actionable summaries instead of raw packet dumps

### 🔧 Modular Design
- Independent Python modules (scan, monitor, dump, replay, crack)  
- Pluggable interfaces for custom analysis workflows

### 🧠 Ethical & Permission-Aware
- Active probing only with consent  
- Prioritizes passive data collection where required

---

## 📂 Repository Structure

/
├── app/ # Core backend logic  
├── frontend/ # UI elements (TypeScript / React?)  
├── crack.py # WPA/WPA2 attack orchestration  
├── dump.py # Packet capture and extraction  
├── monitor.py # Interface monitor mode logic  
├── replay.py # Deauthentication & replay actions  
├── scan.py # Network enumeration  
├── interface.py # Network interface management  
├── ss.py # Signal strength / telemetry utilities  
├── data/ # Example outputs (CSV, Excel)  
└── README.md  

---

## 🧰 Requirements

- Python
- Linux (Kali)  
- WiFi Adapter with packet injectiion capabilities  
- `aircrack-ng`
- Nodejs
---

## 🛠️ Installation

```sh
git clone https://github.com/aaryanbhujang/darwin.git
cd darwin
pip install -r requirements.txt
```
Use a virtual environment (venv/conda) to isolate dependencies.  


## 🧪 Usage
- python /app/main.py # Terminal 1  
- cd frontend && npm run dev # Terminal 2  
- python scan.py           # Discover networks and provides a list of a Access Points on which you can perform attack.(Terminal 3)  
[NOTE: Always run with sudo when capturing/monitoring packets.]  

## ⚖️ Ethics & Legal

DARWIN is intended only for authorized security testing.
Unauthorized scanning or cracking of networks you do not control is illegal in most jurisdictions. Ensure proper permission before use.

## 🧪 Contributing

Fork the repo  
Create feature branch: git checkout -b feature/<name>  
Commit & push  
Open a PR with a clear description  

## 📬 Contact

Maintained by:  
Aaryan G. Bhujang  
Chirag Ferwani  
Rudraksh Charhate  
