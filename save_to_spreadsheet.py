import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

def save_to_spreadsheet(data, sheet_name):
    # Google Sheets authentication
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/service_account_key.json', scope)
    client = gspread.authorize(creds)
    
    # Open the Google Sheet
    sheet = client.open(sheet_name).sheet1

    # Load existing data
    existing_data = sheet.get_all_records()
    existing_titles = set([entry['Title'] for entry in existing_data])

    # Filter out duplicates
    new_entries = [entry for entry in data if entry['Title'] not in existing_titles]

    # Add timestamp to each entry
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for entry in new_entries:
        entry['Timestamp'] = timestamp

    # Convert new entries to DataFrame
    new_df = pd.DataFrame(new_entries)

    if new_entries:
        # Append new data to the sheet
        sheet.insert_rows(new_df.values.tolist(), row=len(existing_data) + 2)
    else:
        print("No new entries to add.")
