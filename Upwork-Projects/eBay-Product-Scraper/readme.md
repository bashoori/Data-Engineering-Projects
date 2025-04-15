# 📦 eBay Product Scraper → Google Sheets + Telegram

This project scrapes product listings from eBay, stores them in a Google Sheet, and sends you a Telegram notification.  
It supports both local development and automated GitHub Actions workflows.

---

## ✅ Features

- Web scraping with BeautifulSoup
- Google Sheets integration via service account
- Telegram bot notification
- Secrets managed securely via .env or GitHub Secrets

---

## 🛠 Local Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file:

```bash
cp .env.example .env
```

3. Fill in the values inside `.env`:
   - Your Telegram bot token
   - Your chat ID
   - Your full Google `credentials.json` content (on one line)

4. Run the script:

```bash
python ebay_to_gsheets_telegram.py
```

---

## 🚀 GitHub Actions Setup

1. Add the following secrets in your GitHub repo:

| Secret Name             | Description                             |
|--------------------------|-----------------------------------------|
| `GOOGLE_CREDENTIALS_JSON` | JSON content of your credentials file |
| `TELEGRAM_BOT_TOKEN`      | Your Telegram bot token               |
| `TELEGRAM_CHAT_ID`        | Your Telegram chat ID or group ID     |

2. Create a GitHub Actions workflow (see docs or ask me for template).

---

## 🔐 Security Notes

- `.env` is excluded via `.gitignore` to prevent secret exposure.
- `.env.example` is safe to commit as a reference.

---

## 📄 License

MIT — use freely, credit appreciated.



ebay_scraper_with_env_doc/
├── ebay_to_gsheets_telegram.py       ✅ Main script with dotenv support
├── requirements.txt                  📦 Dependencies
├── .env.example                      🔐 Env template (safe to commit)
├── .gitignore                        🚫 Hides secrets & temp files
├── README.md                         📘 Full usage guide
└── .github/
    └── workflows/
        └── scraper.yml              🕒 GitHub Actions automation