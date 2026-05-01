"""
app.py — Phase 4: Serve scraped keyboard price data as a JSON API.

Reads keyboard_prices.csv (produced by scrape_title.py) and exposes it
at GET /api/prices so any frontend or tool can consume the data.
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
