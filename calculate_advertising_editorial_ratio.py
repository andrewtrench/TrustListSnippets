import requests
from bs4 import BeautifulSoup
import math
import re

'''Calculate the ratio of ad links to content on a web page.'''

# adhostenames from https://pgl.yoyo.org/adservers/serverlist.php?hostformat=nohtml
# https://pgl.yoyo.org/adservers/index.php
#
def get_page_content(url):
    '''Get the content of a web page.'''
    response = requests.get(url)
    content = response.text
    # Remove HTML comments - to accommodate for Clemence's point about tags being commented out
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    soup = BeautifulSoup(content, 'html.parser')
    return soup



def read_ad_hostnames(file_path):
    '''Read a list of ad hostnames from a file.'''
    with open(file_path, 'r') as f:
        return f.read().splitlines()




def contains_ad_keywords(tag):
    '''Check if a tag contains any of the keywords.'''
    for attribute in tag.attrs:
        if attribute in to_check:
            attr_value = str(tag.get(attribute)).lower()
            if any(keyword.lower() in attr_value for keyword in all_keywords):
                #print("found match")
                #print("tag: ", attribute, tag.get(attribute))
                return tag

    return None


def calculate_ad_to_content_ratio(url):
    '''Calculate the ratio of ad links to content on a web page.'''
    soup = get_page_content(url)
    ad_count = 0
    content_count = 0

    for tag in soup.descendants:
        if tag.name is not None:
            matched_tag = contains_ad_keywords(tag)
            if matched_tag:
                ad_count += 1
                # print(matched_tag)
            elif tag.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'pre', 'blockquote']:
                content_count += 1

    if content_count == 0:
        return "Not enough content to calculate ratio."
    print(ad_count)
    print(content_count)
    ad_to_content_ratio = ad_count / content_count
    ad_to_content_percentage = ad_to_content_ratio * 100
    return ad_to_content_percentage

if __name__ == "__main__":
    adhostnames = read_ad_hostnames('adhostnames.txt')

    keywords = [
        'ads', 'adzone', 'adblock', 'advertiser', 'ad-banner', 'banner', 'sponsored', 'nofollow sponsored',
        'syndication', 'advertising', 'advert', 'advertorial', 'advertisement', 'ins', 'advertisement',
        'advertisements', 'advertisers', 'googlesyndication', 'googleadservices', 'adclick', 'doubleclick'
    ]

    all_keywords = set(keywords + adhostnames)

    to_check = ['class', 'id', 'rel', 'href']

    url = 'https://citizen.co.za'  # Replace with the URL of the web page you want to analyze
    ratio = calculate_ad_to_content_ratio(url)
    print(f'Adlink-to-contentlink ratio: {round(ratio, 2)}%')

