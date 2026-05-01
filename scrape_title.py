import sys, io, csv, os, re, requests
from datetime import datetime
from bs4 import BeautifulSoup

# Fix Windows terminal encoding for the ₹ symbol
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Config ───────────────────────────────────────────────────────────
URL = "https://meckeys.com/shop/keyboard/75-keyboard/royal-kludge-rk-m75-charcoal/"
CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keyboard_prices.csv")
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    )
}


def clean_price(raw: str) -> str:
    """Strip ₹, commas, whitespace, and any trailing text to get a plain number."""
    if not raw:
        return ""
    cleaned = re.sub(r"[₹,\s]", "", raw)   # remove ₹ , and whitespace
    # keep only the numeric portion (digits + decimal point)
    match = re.search(r"[\d.]+", cleaned)
    return match.group() if match else cleaned


def fetch_product_data(url: str) -> dict:
    """Fetch the page and return title + price info as a dict."""
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise ConnectionError(f"Request failed with status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Product title
    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else "N/A"

    # Price extraction
    price_tag = soup.select_one("p.price")
    if price_tag:
        sale = price_tag.select_one("ins .woocommerce-Price-amount")
        original = price_tag.select_one("del .woocommerce-Price-amount")
        current_price = (
            sale.get_text(strip=True) if sale
            else price_tag.select_one(".woocommerce-Price-amount").get_text(strip=True)
        )
        original_price = original.get_text(strip=True) if original else None
    else:
        current_price = "N/A"
        original_price = None

    return {
        "title": title,
        "mrp_raw": original_price or current_price,
        "price_raw": current_price,
    }


def log_to_csv(data: dict) -> None:
    """Append a row to the CSV, creating the file + header if needed."""
    file_exists = os.path.isfile(CSV_FILE)
    header = ["Timestamp", "Product", "MRP", "Current Price"]

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data["title"],
            clean_price(data["mrp_raw"]),
            clean_price(data["price_raw"]),
        ])


# ── Main ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    product = fetch_product_data(URL)

    # Terminal output (human-friendly, with symbols)
    print(f"Product : {product['title']}")
    if product["mrp_raw"] and product["mrp_raw"] != product["price_raw"]:
        print(f"MRP     : {product['mrp_raw']}  (original)")
    print(f"Price   : {product['price_raw']}")

    # CSV logging (clean numbers, no symbols)
    log_to_csv(product)
    print(f"\nData successfully logged to CSV.")
