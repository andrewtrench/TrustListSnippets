import requests
from bs4 import BeautifulSoup


def extract_text_from_page(url):
    '''Extracts text from a web page using BeautifulSoup'''
    # send a GET request to the URL
    response = requests.get(url)

    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # find all the text elements and join them together
    text = ' '.join([elem.text.strip() for elem in soup.find_all(text=True)])

    return text

if __name__ == "__main__":
    url = 'https://celebrealitygossip.com/'
    text = extract_text_from_page(url)
    print(text)