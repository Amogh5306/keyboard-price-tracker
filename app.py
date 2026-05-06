"""
Flask API — Phase 4: Serve scraped keyboard price data as a JSON API.

This script reads keyboard_prices.csv (produced by scrape_title.py) and exposes it
at GET /api/prices. This allows frontends or analytics tools to consume real-time
pricing data for visualized tracking.

===============================================================================
ARCHITECTURE OVERVIEW
===============================================================================
The backend is intentionally kept lightweight and monolithic for simplicity.
It serves a single purpose: exposing the scraped CSV dataset via a RESTful
endpoint. 

Features:
- CORS is globally enabled to allow seamless cross-origin requests from the 
  Vercel-hosted frontend dashboard.
- Uses Python's built-in `csv.DictReader` to automatically map header rows 
  to dictionary keys, ensuring robust JSON serialization.
- Provides built-in error handling (HTTP 404) if the CSV dataset is missing,
  preventing catastrophic crashes on the frontend.

Data Format:
The API returns a JSON array of objects. Example response:
[
  {
    "Timestamp": "2026-05-06 10:00:00",
    "Product": "Royal Kludge RK M75",
    "MRP": "7999",
    "Current Price": "5499"
  }
]

Deployment:
This API is designed to be deployed via WSGI servers like Gunicorn. 
Example start command: `gunicorn app:app`
===============================================================================
"""

import csv
import os
from flask import Flask, jsonify
from flask_cors import CORS

# ── Flask app instance ───────────────────────────────────────────────
app = Flask(__name__)
# Enable CORS for all routes so our local index.html can fetch data
CORS(app)

# Path to the CSV file (sits next to this script)
CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keyboard_prices.csv")


@app.route("/api/prices", methods=["GET"])
def get_prices():
    """
    GET /api/prices

    1. Open keyboard_prices.csv.
    2. Use csv.DictReader to turn each row into a dictionary
       whose keys come from the header row automatically:
       { "Timestamp": "...", "Product": "...", "MRP": "...", "Current Price": "..." }
    3. Collect every row-dict into a list.
    4. Return the list as a JSON response.
    """

    # If the CSV hasn't been created yet, return a helpful message
    if not os.path.isfile(CSV_FILE):
        return jsonify({
            "error": "keyboard_prices.csv not found. Run scrape_title.py first."
        }), 404

    # Read every row from the CSV into a list of dicts
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        # DictReader uses the first row as keys, so each subsequent
        # row becomes {"Timestamp": "...", "Product": "...", ...}
        reader = csv.DictReader(f)
        rows = list(reader)  # materialise the iterator into a list

    # jsonify() converts the Python list → a proper JSON HTTP response
    # with Content-Type: application/json set automatically.
    return jsonify(rows)


# ── Run the dev server ───────────────────────────────────────────────
if __name__ == "__main__":
    # debug=True gives auto-reload on code changes + detailed error pages
    app.run(debug=True, port=5000)
