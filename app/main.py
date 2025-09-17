from flask import Flask, jsonify
from routes.results import result_bp
from flask_cors import CORS  # enable CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})  # allow React frontend to fetch data from Flask

    app.config["SCAN_EXCEL"] = "/home/chirag/Code/Repositories/darwin/wifi_scan.xlsx"
    app.register_blueprint(result_bp, url_prefix="/results")

    @app.route("/")
    def home():
        return jsonify({"message": "Backend running! Visit /results/stats for WiFi data."})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
