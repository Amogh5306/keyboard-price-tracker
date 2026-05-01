import sys, io, requests
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

URL = "https://meckeys.com/shop/keyboard/75-keyboard/royal-kludge-rk-m75-charcoal/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    )
}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

for tag in soup.select("p.price, .summary .price, .woocommerce-Price-amount"):
    print(f"TAG: {tag.name} | CLASS: {tag.get('class')} | TEXT: {tag.get_text(strip=True)}")
    print(f"HTML: {tag}")
    print("---")
