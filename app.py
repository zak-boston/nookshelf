"""
NookShelf — backend
====================
Endpoints:
  GET  /api/data          →  load services and sections
  POST /api/data          →  save services and sections
  GET  /api/status?url=   →  server-side reachability check (avoids CORS)

Requirements:
  pip install flask requests

Run directly:  python app.py
Run in Docker: docker compose up -d
"""

import json
import os
import requests as req_lib
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static")

PORT          = 5001
DATA_FILE     = "/data/nookshelf.json"
DEFAULT_SECTIONS = ["Media", "Tools", "Diagnostics"]
STATUS_TIMEOUT   = 2  # seconds


# ── Frontend ──────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("static", "index.html")


# ── Data ──────────────────────────────────────────────────────────

@app.route("/api/data", methods=["GET"])
def get_data():
    try:
        if not os.path.exists(DATA_FILE):
            return jsonify({"services": [], "sections": DEFAULT_SECTIONS})
        with open(DATA_FILE, "r") as f:
            return jsonify(json.load(f))
    except Exception as e:
        app.logger.error(f"Failed to load data: {e}")
        return jsonify({"services": [], "sections": DEFAULT_SECTIONS})


@app.route("/api/data", methods=["POST"])
def save_data():
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        data = request.get_json()
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return jsonify({"ok": True})
    except Exception as e:
        app.logger.error(f"Failed to save data: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# ── Status check ──────────────────────────────────────────────────

@app.route("/api/status")
def api_status():
    """
    Server-side reachability check — avoids browser CORS issues.
    The browser can't directly fetch http://192.168.1.x:8096 from a
    different origin, but Flask running on the same network can.

    GET /api/status?url=http://192.168.1.x:8096
    Returns: { "up": true, "ms": 142 } or { "up": false, "ms": null }
    """
    url = request.args.get("url", "").strip()
    if not url:
        return jsonify({"up": False, "ms": None, "error": "No URL provided"}), 400

    import time
    start = time.time()
    try:
        r = req_lib.get(url, timeout=STATUS_TIMEOUT, allow_redirects=True)
        ms = int((time.time() - start) * 1000)
        # Any HTTP response (even 401/403) means the service is up
        return jsonify({"up": True, "ms": ms})
    except Exception:
        return jsonify({"up": False, "ms": None})


# ── Start ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print()
    print("🛖  NookShelf is running!")
    print(f"   Open http://localhost:{PORT} in your browser")
    print()
    app.run(host="0.0.0.0", port=PORT, debug=False)
