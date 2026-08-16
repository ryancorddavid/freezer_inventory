import sys
import gspread

# Receive arguments passed from Jenkins parameters
quantity = sys.argv[1]
item_name = sys.argv[2]

# Authenticate using Service Account JSON
gc = gspread.service_account(filename='credentials.json')

# Open your spreadsheet by ID
spreadsheet = gc.open_by_key("1saNUY--A7zdBK_PaSIAnbApaNpund2E8NvFrcz8EO3I")
worksheet = spreadsheet.sheet1

# Append row to match your columns: [QUANTITY, ITEM NAME]
worksheet.append_row([quantity, item_name], table_range='A2:B2')

print(f"Successfully added {quantity}x {item_name} to Freezer Inventory!")