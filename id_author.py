import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urlparse, urljoin

'''Code below indtifies authors in source code of a webpage after selecting some random articles from the home page.'''


def find_authors(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Common tags and attributes for author names
    author_selectors = [
        {'tag': 'span', 'attr': 'class', 'value': 'author'},
        {'tag': 'span', 'attr': 'itemprop', 'value': 'name'},
        {'tag': 'span', 'attr': 'class', 'value': 'byline'},
        {'tag': 'span', 'attr': 'class', 'value': 'post-author'},
        {'tag': 'a', 'attr': 'class', 'value': 'author-url'},
        {'tag': 'div', 'attr': 'class', 'value': 'author-name'},
        {'tag': 'div', 'attr': 'class', 'value': 'entry-author'},
        {'tag': 'meta', 'attr': 'name', 'value': 'author'},
        {'tag': 'a', 'attr': 'rel', 'value': 'author'},
        {'tag': 'span', 'attr': 'class', 'value': 'name', 'parent_class': 'author'},
        {'tag': 'div', 'attr': 'id', 'value': 'author-info'},
        {'tag': 'span', 'attr': 'class', 'value': 'author vcard'},
        {'tag': 'div', 'attr': 'class', 'value': 'post-meta-author'},
        {'tag': 'div', 'attr': 'class', 'value': 'post-byline'},
        {'tag': 'span', 'attr': 'class', 'value': 'fn'},
    ]

    authors = []
    # Check for elements with specific tag, attribute and value
    for selector in author_selectors:
        elements = soup.find_all(selector['tag'], attrs={selector['attr']: selector['value']})
        for element in elements:
            author_name = element.text.strip() if element.name != 'meta' else element['content'].strip()
            if author_name and author_name not in authors:
                authors.append(author_name)

    # Check for elements with attribute values containing "author" or "byline"
    for element in soup.find_all(True):
        for attr_name, attr_value in element.attrs.items():
            if isinstance(attr_value, str) and ('author' in attr_value.lower() or 'byline' in attr_value.lower()):
                author_name = element.text.strip()
                if author_name and author_name not in authors:
                    authors.append(author_name)
            elif isinstance(attr_value, list):
                for value in attr_value:
                    if isinstance(value, str) and ('author' in value.lower() or 'byline' in value.lower()):
                        author_name = element.text.strip()
                        if author_name and author_name not in authors:
                            authors.append(author_name)

    return authors


def select_random_articles_from_home_page(url):
    '''Selects 5 random articles from the home page of the given URL'''
    articles = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all('a', href=True)

    base_url = urlparse(url).scheme + "://" + urlparse(url).hostname

    for a in tags:
        href = a['href']
        if href.startswith('/') or base_url in href:
            articles.append(href)

    selected = random.sample(articles, min(5, len(articles)))
    selected = [urljoin(base_url, s) for s in selected]
    return selected

if __name__ == "__main__":

    url = 'https://notablevoice.co.za'  # Replace this with the actual article URL

    articles = select_random_articles_from_home_page(url)
    for article in articles:
        print(article)
        authors = find_authors(article)

        if authors:
            print('Authors found:')
            for author in authors:
                print(author)
        else:
            print('No authors found.')
