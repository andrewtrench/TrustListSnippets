import requests
from bs4 import BeautifulSoup
'''basic snippet to extract links from page and looking for quality markers'''

def extract_urls(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tags = (soup.find_all('a', href=True))
    for a in tags:
        if "about" in a['href'] or "contact" in a['href'] or "advertise" in a['href'] or "privacy" in a['href'] or "terms" in a['href'] or "cookie" in a['href'] or "sitemap" in a['href']:
            print (a['href'])


if __name__ == "__main__":
    url = 'https://timeslive.co.za'
    extract_urls(url)