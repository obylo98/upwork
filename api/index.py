import gspread
from oauth2client.service_account import ServiceAccountCredentials
from fetch_rss import fetch_rss_feed
from parse_rss import parse_feed_entries
from save_to_spreadsheet import save_to_spreadsheet
import schedule
import time
from datetime import datetime

def read_rss_urls_from_google_sheet(sheet_name):
    # Google Sheets authentication
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/service_account_key.json', scope)
    client = gspread.authorize(creds)
    
    # Open the Google Sheet
    sheet = client.open(sheet_name).sheet1
    
    # Read RSS feed URLs
    urls = sheet.col_values(1)  # Assuming URLs are in the first column
    return urls[1:]  # Skip the header row

def fetch_and_save_rss_entries():
    print(f"Running RSS fetch and save at {datetime.now()}")
    rss_urls = read_rss_urls_from_google_sheet('RSS Feeds')  # Replace with your sheet name
    all_entries = []

    for url in rss_urls:
        feed = fetch_rss_feed(url)
        if feed:
            entries = parse_feed_entries(feed)
            all_entries.extend(entries)

    if all_entries:
        save_to_spreadsheet(all_entries, 'RSS Feed Results')  # Replace with your destination sheet name
    else:
        print("No entries to save.")

# Schedule the job every 2 hours
schedule.every(2).hours.do(fetch_and_save_rss_entries)

if __name__ == '__main__':
    # Initial run
    fetch_and_save_rss_entries()
    while True:
        schedule.run_pending()
        time.sleep(1)
