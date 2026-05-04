# ⌨️ Keyboard Price Tracker

A full-stack data pipeline that scrapes e-commerce prices, serves them via a REST API, and visualizes trends on a live dashboard.

**[Live Dashboard](https://amogh-keyboard-tracker.vercel.app)** · **[API Endpoint](https://keyboard-price-tracker.onrender.com/api/prices)**

---

## How It Works

```
Scraper (Python) → CSV Database → Flask API → Chart.js Dashboard
```

1. **Scrape** — Python script spoofs a Chrome User-Agent, parses WooCommerce HTML with BeautifulSoup, and extracts current + original prices
2. **Store** — Cleans data with regex, appends timestamped rows to a CSV file
3. **Serve** — Flask API reads the CSV and returns structured JSON via a CORS-enabled endpoint
4. **Visualize** — Vanilla JS fetches the API and renders an interactive Chart.js line graph with a dark-mode UI

## Tech Stack

| Layer | Tech |
|-------|------|
| Scraping | Python, BeautifulSoup4, Requests |
| Backend | Flask, Flask-CORS, Gunicorn |
| Frontend | Vanilla JS, HTML5, CSS3, Chart.js |
| Deployment | Render (API), Vercel (Dashboard) |

## Quick Start

```bash
git clone https://github.com/Amogh5306/keyboard-price-tracker.git
cd keyboard-price-tracker
pip install -r requirements.txt

python scrape_title.py   # generate data
python app.py            # start API on :5000
# open index.html in browser
```

## What I Learned

- Navigating anti-bot protections and parsing nested HTML structures
- Building a minimal REST API with Flask and deploying with Gunicorn
- Connecting a frontend to a live backend across different hosting providers (Vercel ↔ Render)
