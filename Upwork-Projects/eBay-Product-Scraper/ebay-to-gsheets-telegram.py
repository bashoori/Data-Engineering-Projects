"""
eBay Product Scraper → Google Sheets + Telegram Notifier
---------------------------------------------------------
This script scrapes product data from eBay search results,
cleans the prices, saves the data into a Google Sheet,
and sends a summary notification to Telegram.

Tools Used:
- BeautifulSoup for scraping
- gspread + oauth2client for Google Sheets integration
- Telegram Bot API for notification

Author: Your Name
License: MIT
"""

import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import re
import json


# ---------------------------------------------------
# 🔐 Recreate credentials.json from GitHub Secrets
# This allows secure use in GitHub Actions or Codespaces
# ---------------------------------------------------
if os.getenv("GOOGLE_CREDENTIALS_JSON"):
    with open("credentials.json", "w") as f:
        f.write(os.getenv("GOOGLE_CREDENTIALS_JSON"))


# -------------------------
# 📬 Telegram Bot Setup
# -------------------------
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    """Send a message to your Telegram chat via Bot API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=payload)

# -------------------------
# 📄 Setup Google Sheets Client
# -------------------------
# Requires a credentials.json file from Google Cloud Console with Sheets API enabled
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open("eBay Products").sheet1

# -------------------------
# 💰 Price Cleaning Utility
# -------------------------
def clean_price(price_str):
    """Remove currency symbols and convert price string to float."""
    price = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(price)
    except ValueError:
        return None

# -------------------------
# 🔍 Scrape eBay for Products
# -------------------------
search_term = "laptop"
url = f"https://www.ebay.com/sch/i.html?_nkw={search_term}"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
items = soup.select(".s-item")

# -------------------------
# 🧹 Extract and Process Data
# -------------------------
count = 0
for item in items:
    title_tag = item.select_one(".s-item__title")
    price_tag = item.select_one(".s-item__price")
    link_tag = item.select_one(".s-item__link")

    if title_tag and price_tag and link_tag:
        title = title_tag.get_text()
        price = price_tag.get_text()
        link = link_tag["href"]

        clean_price_value = clean_price(price)
        if clean_price_value:
            sheet.append_row([title, price, link])
            count += 1

# -------------------------
# ✅ Send Summary via Telegram
# -------------------------
message = f"✅ {count} products from eBay added to Google Sheets!\nSearch term: {search_term}"
send_telegram_message(message)
print(message)
