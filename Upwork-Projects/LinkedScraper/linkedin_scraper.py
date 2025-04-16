"""
📄 LinkedIn Guest API Job Scraper → Google Sheets + Telegram Notifier

This version uses LinkedIn's public HTML endpoint to fetch job listings without login or Selenium.
It pulls job cards directly for "Data Engineer" roles in Vancouver, writes them to Google Sheets,
and sends a Telegram summary.

Author: Your Name
"""

import requests
import gspread
import os
import json
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON_bita-projects")

search_term = "data engineer"
geo_id = "103366113" # Vancouver, British Columbia, Canada
RESULT_LIMIT = 200

# -----------------------------
# Build guest jobs API URL
# -----------------------------

url = (
    "https://www.linkedin.com/jobs/search/?"
    f"geoId={geo_id}&keywords={urllib.parse.quote(search_term)}"
)

print(url)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/"
}

# -----------------------------
# Send Telegram message
# -----------------------------
def send_telegram_message(text):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(telegram_url, data=payload)

# -----------------------------
# Google Sheets setup
# -----------------------------
if not CREDENTIALS_JSON:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON")

with open("credentials.json", "w") as f:
    json.dump(json.loads(CREDENTIALS_JSON), f)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

#sheet = client.open("bita-projects").sheet1
spreadsheet = client.open("bita-projects")

# Create the worksheet if it doesn't exist
try:
    sheet = spreadsheet.worksheet("linkedin")
except gspread.exceptions.WorksheetNotFound:
    print("🔧 Worksheet 'linkedin' not found. Creating it now...")
    sheet = spreadsheet.add_worksheet(title="linkedin", rows="500", cols="20")

# Clear old data and set headers
sheet.clear()
headers_row = ["Title", "Company", "Location", "Link", "Timestamp"]
sheet.append_row(headers_row)


# -----------------------------
# Fetch and parse job HTML
# -----------------------------
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Save HTML to file for debugging
with open("LinkedIn_debug.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())
print("💾 Saved raw LinkedIn HTML to LinkedIn_debug.html")

job_cards = soup.select("li")
rows_to_add = []
existing_titles = [row[0] for row in sheet.get_all_values()[1:] if row]


# -----------------------------
# Parse each job card
# -----------------------------
for job in job_cards:
    title_tag = job.find("h3")
    company_tag = job.find("h4")
    location_tag = job.find("span", class_="job-search-card__location")
    link_tag = job.find("a", href=True)

    if title_tag and company_tag and location_tag and link_tag:
        title = title_tag.get_text(strip=True)
        company = company_tag.get_text(strip=True)
        location = location_tag.get_text(strip=True)
        link = "https://www.linkedin.com" + link_tag["href"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 🔍 Title must include both 'data' and 'engineer'
        if "data" not in title.lower() or "engineer" not in title.lower():
            print(f"❌ Rejected (title): {title}")
            continue

        # 📍 Location must include 'vancouver'
        if "vancouver" not in location.lower():
            print(f"❌ Rejected (location): {title} — {location}")
            continue

        if title in existing_titles:
            print(f"⚠️ Duplicate: {title}")
            continue

        rows_to_add.append([title, company, location, link, timestamp])
        print(f"✅ Accepted: {title} at {company} — {location}")

# -----------------------------
# Append to Google Sheet
# -----------------------------
top_rows = rows_to_add[:RESULT_LIMIT]

if top_rows:
    sheet.append_rows(top_rows)

# -----------------------------
# Send summary to Telegram
# -----------------------------
message = f"✅ {len(top_rows)} LinkedIn jobs added to Google Sheets!\nSearch term: {search_term}"
send_telegram_message(message)
print(message)
