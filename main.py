import sys
import os
import json
import gspread
from google.oauth2.service_account import Credentials

quantity = sys.argv[1]
item_name = sys.argv[2]

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

if os.path.exists("credentials.json"):
    gc = gspread.service_account(filename="credentials.json")
elif "GOOGLE_CREDS_JSON" in os.environ and os.environ["GOOGLE_CREDS_JSON"].strip():
    creds_dict = json.loads(os.environ["GOOGLE_CREDS_JSON"])

    # Fix stringified newlines in private key
    if "private_key" in creds_dict:
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    gc = gspread.authorize(creds)
else:
    raise FileNotFoundError("No valid credentials found.")

spreadsheet = gc.open_by_key("1saNUY--A7zdBK_PaSIAnbApaNpund2E8NvFrcz8EO3I")
worksheet = spreadsheet.sheet1
worksheet.append_row([quantity, item_name], table_range="A2:B2")

print(f"Successfully added: {quantity}x {item_name}")