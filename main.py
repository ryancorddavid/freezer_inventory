import sys
import os
import json
import gspread
from google.oauth2.service_account import Credentials

# 1. Grab parameters passed from Jenkins/GitHub Actions
quantity = sys.argv[1]
item_name = sys.argv[2]

# 2. Authenticate using credentials stored in environment
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Check if JSON string exists in ENV (ideal for CI/CD secrets)
if "GOOGLE_CREDS_JSON" in os.environ:
    creds_dict = json.loads(os.environ["GOOGLE_CREDS_JSON"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    gc = gspread.authorize(creds)
else:
    # Fallback to local file if testing locally
    gc = gspread.service_account(filename="credentials.json")

# 3. Open spreadsheet by ID
spreadsheet = gc.open_by_key("1saNUY--A7zdBK_PaSIAnbApaNpund2E8NvFrcz8EO3I")
worksheet = spreadsheet.sheet1

# 4. Append row matching template [QUANTITY, ITEM NAME]
worksheet.append_row([quantity, item_name], table_range="A2:B2")

print(f"Successfully added: {quantity}x {item_name}")