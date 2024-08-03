from bs4 import BeautifulSoup

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.get_text()

def parse_feed_entries(feed):
    entries = []
    for entry in feed.entries:
        cleaned_description = clean_html(entry.description)
        entries.append({
            'Title': entry.title,
            'Link': entry.link,
            'Published': entry.published,
            'Description': cleaned_description
        })
    return entries
