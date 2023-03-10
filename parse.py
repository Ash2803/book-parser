from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class RedirectedPage(Exception):
    pass


def get_page(url):
    response = requests.get(f'{url}')
    response.raise_for_status()
    return response


def parse_book_page(response) -> dict:
    soup = BeautifulSoup(response.text, 'lxml')
    relative_book_path = soup.select_one('.d_book a:nth-child(2)')['href']
    page_url_parse = urlparse(response.url)
    page_base_url = page_url_parse._replace(path='').geturl()
    txt_book_link = urljoin(page_base_url, relative_book_path)
    genres = soup.select('span.d_book a')
    parsed_title = soup.select_one('div#content h1')
    parsed_img = soup.select_one('.bookimage img')['src']
    img_link = urljoin(page_base_url, parsed_img)
    comments = soup.select('.texts .black')
    parsed_comments = [comment.text for comment in comments]
    parsed_genres = [genre.text for genre in genres]
    return {
        'txt_book_link': txt_book_link,
        'image_link': img_link,
        'book_title': parsed_title.text.split('::')[0].strip(),
        'author': parsed_title.text.split('::')[1].strip(),
        'comments': parsed_comments,
        'genres': parsed_genres
    }


def parse_collection_page(response) -> list:
    """Returns books links"""
    soup = BeautifulSoup(response.text, 'lxml')
    relative_book_path = soup.select('table .bookimage a')
    page_url_parse = urlparse(response.url)
    page_base_url = page_url_parse._replace(path='').geturl()
    books_links = [urljoin(page_base_url, book_id['href']) for book_id in relative_book_path]
    return books_links


def get_collection_last_page_number(response):
    soup = BeautifulSoup(response.text, 'lxml')
    count_of_pages = soup.select_one('.center .npage:nth-child(7)').text
    return int(count_of_pages)


def check_for_redirect(response):
    if response.history:
        raise RedirectedPage
