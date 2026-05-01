# Keyboard Price Tracker ⌨️

A full-stack, automated web scraping pipeline and real-time dashboard built to track the pricing volatility of the Royal Kludge RK M75 keyboard on e-commerce platforms.

![Dashboard Preview](https://via.placeholder.com/1000x500.png?text=Premium+Dark+Mode+Chart.js+Dashboard) <!-- Replace with actual screenshot later! -->

## 🚀 Overview

This project was built to demonstrate end-to-end data engineering and full-stack deployment skills. It features a robust Python scraping script that navigates complex HTML structures, a Flask REST API to serve the extracted data, and a responsive, premium dark-mode frontend to visualize pricing trends using Chart.js.

### Architecture

1. **Data Extraction**: A Python script utilizing `requests` and `BeautifulSoup` to scrape e-commerce product pages. It intelligently parses standard WooCommerce HTML structures, handling complex nested tags (`<ins>`, `<del>`) and character encoding issues (e.g., Unicode currency symbols).
2. **Data Storage**: Data is cleaned using Regex and stored in a local, lightweight CSV "database" appended with precise timestamps.
3. **Backend API**: A Python `Flask` application acting as the middleware, reading the CSV data and exposing it as a structured JSON API via a CORS-enabled endpoint.
4. **Frontend Visualization**: A modern, dependency-free HTML5/CSS/Vanilla JS frontend. It fetches the JSON data asynchronously and renders an interactive line chart using `Chart.js`.

---

## 🛠️ Tech Stack

* **Backend**: Python, Flask, Gunicorn (WSGI Server)
* **Data Engineering**: BeautifulSoup4, Requests, Regex, CSV
* **Frontend**: Vanilla JavaScript, HTML5, CSS3, Chart.js
* **Deployment**: Render (Backend API), Vercel (Static Frontend)

---

## 💻 How It Works

### 1. The Scraper (`scrape_title.py`)
Spoofs a standard Chrome User-Agent to bypass basic bot-protection, requests the HTML, and parses the DOM. It extracts both the *Current Price* and the *Original MRP*, strips away all symbols and whitespace using Regular Expressions, and logs the raw numeric values into `keyboard_prices.csv`.

### 2. The API (`app.py`)
A minimal Flask server equipped with `flask-cors`. It exposes the `/api/prices` GET endpoint, safely parsing the CSV using Python's `csv.DictReader` and serializing the rows into a JSON array for web consumption.

### 3. The Dashboard (`index.html`)
Fetches the JSON payload from the backend API. It maps the timestamps to the X-axis and the prices to the Y-axis. The UI is designed with a premium dark-theme aesthetic featuring neon-cyan accents and subtle glowing hover states for maximum visual impact.

---

## ⚙️ Local Setup

If you want to run this project locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Amogh5306/keyboard-price-tracker.git
   cd keyboard-price-tracker
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the scraper (to generate initial data):**
   ```bash
   python scrape_title.py
   ```

4. **Start the Flask API:**
   ```bash
   python app.py
   ```

5. **View the dashboard:**
   Simply double-click `index.html` to open it in your browser. The chart will automatically fetch data from `http://localhost:5000`.

---

## ☁️ Production Deployment

* The **Frontend** is deployed as a static site on **Vercel**, enabling lightning-fast global CDN delivery.
* The **Backend** is deployed as a Web Service on **Render.com**, utilizing `gunicorn` as a production-grade WSGI server to handle concurrent requests securely and efficiently.
