from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class LinkNotFoundError(Exception):
    pass


class RedirectedPage(Exception):
    pass


def get_book_page(url, book_id):
    try:
        response = requests.get(f'{url}/b{book_id}')
        response.raise_for_status()
        check_for_redirect(response)
        return response
    except RedirectedPage:
        raise RedirectedPage from None


def parse_book_page(response) -> dict:
    try:
        soup = BeautifulSoup(response.text, 'lxml')
        relative_book_path = soup.find('a', text='скачать txt')['href']
    except TypeError:
        raise LinkNotFoundError from None

    page_url_parse = urlparse(response.url)
    page_base_url = page_url_parse._replace(path='').geturl()
    txt_book_link = urljoin(page_base_url, relative_book_path)

    genres = soup.find('span', class_='d_book').find_all('a')
    parsed_title = soup.find('div', id='content').find('h1')
    parsed_img = soup.find('table').find('div', class_='bookimage').find('img')['src']
    img_link = urljoin(page_base_url, parsed_img)
    comments = soup.find_all(class_='texts')
    parsed_comments = [comment.find(class_='black').text for comment in comments]
    parsed_genres = [genre.text for genre in genres]
    return {
        'txt_book_link': txt_book_link,
        'image_link': img_link,
        'book_title': parsed_title.text.split('::')[0].strip(),
        'author': parsed_title.text.split('::')[1].strip(),
        'comments': parsed_comments,
        'genres': parsed_genres
    }


def check_for_redirect(response):
    if not response.history:
        raise RedirectedPage from None
