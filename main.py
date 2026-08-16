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

SPREADSHEET_KEY = "1saNUY--A7zdBK_PaSIAnbApaNpund2E8NvFrcz8EO3I"

def get_credentials():
    # 1. First check if Jenkins provided a Secret File path
    creds_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
    if os.path.exists(creds_file):
        return Credentials.from_service_account_file(creds_file, scopes=scopes)

    # 2. Check environment variable string fallbacks
    for env_var in ["GOOGLE_CRED_JSON", "GOOGLE_CREDS_JSON"]:
        if env_var in os.environ and os.environ[env_var].strip():
            creds_dict = json.loads(os.environ[env_var])
            if "private_key" in creds_dict:
                pk = creds_dict["private_key"]
                if "\\n" in pk:
                    pk = pk.replace("\\n", "\n")
                creds_dict["private_key"] = pk.strip()
            return Credentials.from_service_account_info(creds_dict, scopes=scopes)

    raise FileNotFoundError(
        "No valid credentials found. Ensure credentials.json exists locally or "
        "GOOGLE_APPLICATION_CREDENTIALS / GOOGLE_CRED_JSON environment variable is set."
    )

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 main.py <qty> <item_name>")
        sys.exit(1)

    qty = sys.argv[1]
    item_name = sys.argv[2]
    print(f"Processing item: {qty}x {item_name}")

    creds = get_credentials()
    gc = gspread.authorize(creds)

    # Open the sheet by its explicit URL key and target the first worksheet
    sh = gc.open_by_key(SPREADSHEET_KEY)
    worksheet = sh.sheet1

    # Append the quantity and item name as a new row
    worksheet.append_row([qty, item_name])
    print(f"Successfully added {qty}x {item_name} to sheet: {sh.title}")

if __name__ == "__main__":
    main()