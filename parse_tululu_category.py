from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from parse import RedirectedPage


def get_collection(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def parse_category(response) -> list:
    soup = BeautifulSoup(response.text, 'lxml')
    relative_book_path = soup.select('table .bookimage a')
    page_url_parse = urlparse(response.url)
    page_base_url = page_url_parse._replace(path='').geturl()
    books_links = [urljoin(page_base_url, book_id['href']) for book_id in relative_book_path]
    return books_links


def check_for_redirect(response):
    if response.history:
        raise RedirectedPage
