from flask import Flask
from routes.results import result_bp

def create_app():
    app = Flask(__name__)
    app.config["SCAN_EXCEL"] = "/home/kali/darwin/wifi_scan.xlsx"  # update path
    app.register_blueprint(result_bp, url_prefix="/results")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
