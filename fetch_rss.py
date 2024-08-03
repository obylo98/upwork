import requests
import feedparser

def fetch_rss_feed(url):
    response = requests.get(url)
    if response.status_code == 200:
        return feedparser.parse(response.content)
    else:
        print(f"Failed to retrieve RSS feed. Status code: {response.status_code}")
        return None
