import json, os
from dotenv import load_dotenv

load_dotenv()
creds = json.loads(os.getenv("GOOGLE_CREDENTIALS_JSON_bita-projects"))
print("📧 Your service account email is:", creds["client_email"])
