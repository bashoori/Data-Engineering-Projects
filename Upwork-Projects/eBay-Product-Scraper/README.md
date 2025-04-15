# 📦 eBay Product Scraper → Google Sheets + Telegram Bot

This is a Python automation script that:

1. Scrapes product listings from eBay based on a search term
2. Saves **unique** listings to a Google Sheet
3. Sends a summary update to Telegram

---

## ✅ Features

- **Keyword-configurable** via `.env` file
- **append_rows** batching to avoid rate limit errors
- **Deduplication**: avoids adding duplicate products
- **Timestamping**: logs when each item was added
- **Telegram bot integration**
- **Failsafe**: saves fallback HTML when no items found

---

## 🛠 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ebay-scraper.git
cd ebay-scraper
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

Copy the example:
```bash
cp .env.example .env
```

Fill in:

```env
SEARCH_TERM=wireless+mouse
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
GOOGLE_CREDENTIALS_JSON={"type": "service_account", ...}
```

### 4. Share your Google Sheet

- Name the sheet: `eBay Products`
- Share it with your **Google service account email** as an editor

---

## ▶️ Run the script

```bash
python ebay_to_gsheets_telegram.py
```

---

## 🤖 GitHub Actions

You can automate this script to run daily using the included workflow in `.github/workflows/scraper.yml`.

---

## 📂 Output Format

Each new row added to the sheet will contain:

| Title | Price | Product Link | Timestamp |
|-------|-------|--------------|-----------|

---
## 📁 Project Structure

<pre>
/your-project-folder/
├── <strong>ebay_to_gsheets_telegram.py</strong>   ← 🧠 Main script
├── <strong>.env.example</strong>                  ← 📄 Template for your environment variables
├── <strong>.gitignore</strong>                    ← 🔐 Prevents secrets from being committed
├── <strong>README.md</strong>                     ← 📘 Optional setup guide
├── <strong>LICENSE</strong>                        ← 📄 MIT License for open-source use
└── <strong>.github/</strong>
    └── <strong>workflows/</strong>
        └── <strong>scraper.yml</strong>           ← 🕒 GitHub Actions workflow for daily automation
</pre>



## 📄 License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.
