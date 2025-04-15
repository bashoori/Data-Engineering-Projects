"""
📦 eBay Product Scraper → Google Sheets + Telegram Notifier
------------------------------------------------------------

This Python script automates the process of:
1. Scraping product listings from eBay based on a configurable search keyword
2. Storing unique product info (title, price, link, timestamp) in a Google Sheet
3. Sending a summary notification to Telegram after the update

✨ Key Features:
- append_rows(): Uses batch write for better speed & quota efficiency
- Deduplication: Prevents adding the same product multiple times
- Timestamping: Each row is labeled with when it was added
- Configuration: Set search term and secrets via .env file

🔐 Required:
- Google Service Account with Sheets + Drive API enabled
- Telegram Bot Token + Chat ID from @BotFather
- Google Sheet titled "eBay Products" shared with your service account

Author: Bita
License: MIT
"""

import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import re
import json
from dotenv import load_dotenv
from datetime import datetime

# -----------------------------
# Load environment config
# 🔧 Environment Variables (set in .env or GitHub Secrets)
# -----------------------------
load_dotenv()
SEARCH_TERM = os.getenv("SEARCH_TERM", "laptop")       # set custom eBay keyword
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")

# -----------------------------
# Telegram Notification
# -----------------------------
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=payload)

# -----------------------------
# Google Sheets Authentication
# -----------------------------
if not CREDENTIALS_JSON:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON")

with open("credentials.json", "w") as f:
    json.dump(json.loads(CREDENTIALS_JSON), f)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("eBay Products").sheet1

# -----------------------------
# Utility: clean price string
# -----------------------------
def clean_price(price_str):
    price = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(price)
    except ValueError:
        return None

# -----------------------------
# Scrape eBay
# -----------------------------
print(f"🔍 Searching eBay for: {SEARCH_TERM}")
url = f"https://www.ebay.com/sch/i.html?_nkw={SEARCH_TERM}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
items = soup.select(".s-item")

# Save fallback HTML for manual inspection if empty
if not items:
    with open("ebay_debug.html", "w") as f:
        f.write(soup.prettify())
    print("⚠️ No items found. HTML saved to ebay_debug.html.")

# -----------------------------
# Deduplicate based on existing titles
# -----------------------------
existing_titles = [row[0] for row in sheet.get_all_values()[1:] if row]  # skip header row
rows_to_add = []

# -----------------------------
# Parse and collect product data
# -----------------------------
for item in items:
    title_tag = item.select_one(".s-item__title") or item.select_one("h3")
    price_tag = item.select_one(".s-item__price") or item.select_one(".s-item__detail")
    link_tag = item.select_one(".s-item__link") or item.find("a", href=True)

    if title_tag and price_tag and link_tag:
        title = title_tag.get_text(strip=True)
        price = price_tag.get_text(strip=True)
        link = link_tag["href"]

        if title in existing_titles:
            continue  # Skip duplicates

        clean_price_value = clean_price(price)
        if clean_price_value:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            rows_to_add.append([title, price, link, timestamp])
            print(f"✅ New: {title} — {price}")

######## Options to add data to sheet:
# -----------------------------
# Batch append to Google Sheet
# -----------------------------
#if rows_to_add:
#    sheet.append_rows(rows_to_add)

# -----------------------------
# Append top 10 results only
# -----------------------------
top_10_rows = rows_to_add[:10]  # Only keep top 10

if top_10_rows:
    sheet.append_rows(top_10_rows)
######## End of Options

# -----------------------------
# Telegram Summary Notification
# -----------------------------
message = f"✅ {len(rows_to_add)} new products from eBay added to Google Sheets!\nSearch term: {SEARCH_TERM}"
send_telegram_message(message)
print(message)
