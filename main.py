import os
import sys
import json
import gspread
from google.oauth2.service_account import Credentials

# Define required scopes
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_credentials():
    # 1. First check if Jenkins provided a Secret File path
    creds_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
    if os.path.exists(creds_file):
        return Credentials.from_service_account_file(creds_file, scopes=scopes)

    # 2. Fallback to reading JSON string from environment variable (with robust newline handling)
    if "GOOGLE_CREDS_JSON" in os.environ and os.environ["GOOGLE_CREDS_JSON"].strip():
        creds_dict = json.loads(os.environ["GOOGLE_CREDS_JSON"])
        if "private_key" in creds_dict:
            pk = creds_dict["private_key"]
            if "\\n" in pk:
                pk = pk.replace("\\n", "\n")
            creds_dict["private_key"] = pk.strip()
        return Credentials.from_service_account_info(creds_dict, scopes=scopes)

    raise FileNotFoundError(
        "No valid credentials found. Ensure credentials.json exists locally or "
        "GOOGLE_APPLICATION_CREDENTIALS / GOOGLE_CREDS_JSON environment variable is set."
    )

def main():
    creds = get_credentials()
    gc = gspread.authorize(creds)

    # Example positional args handling: python3 main.py <qty> <item_name>
    if len(sys.argv) > 2:
        qty = sys.argv[1]
        item_name = sys.argv[2]
        print(f"Processing item: {qty}x {item_name}")

    # Add your spreadsheet interaction logic below
    # sheet = gc.open("Freezer Inventory").sheet1
    # ...

if __name__ == "__main__":
    main()