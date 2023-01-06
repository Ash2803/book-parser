from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


class RedirectedPage(Exception):
    pass


def get_collection(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def parse_category(response) -> list:
    soup = BeautifulSoup(response.text, 'lxml')
    relative_book_path = soup.find_all(['table', 'div'], class_='bookimage')
    page_url_parse = urlparse(response.url)
    page_base_url = page_url_parse._replace(path='').geturl()
    books_links = []
    for book_id in relative_book_path:
        book_link = urljoin(page_base_url, book_id.find('a')['href'])
        books_links.append(book_link)
    return books_links


def check_for_redirect(response):
    if response.history:
        raise RedirectedPage


