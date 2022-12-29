from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class LinkNotFoundError(Exception):
    pass


class RedirectedPage(Exception):
    pass


def parse_book_page(url, book_id) -> dict:
    response = requests.get(f'{url}/b{book_id}')
    response.raise_for_status()
    try:
        check_for_redirect(response)
    except RedirectedPage:
        raise RedirectedPage from None
    try:
        soup = BeautifulSoup(response.text, 'lxml')
        parsed_txt_book = soup.find('a', text='скачать txt')['href']
    except TypeError:
        raise LinkNotFoundError from None
    txt_book_link = urljoin(url, parsed_txt_book)
    genres = soup.find('span', class_='d_book').find_all('a')
    parsed_title = soup.find('div', id='content').find('h1')
    parsed_img = soup.find('table').find('div', class_='bookimage').find('img')['src']
    img_link = urljoin(url, parsed_img)
    comments = soup.find_all(class_='texts')
    parsed_comments = []
    parsed_genres = []
    for genre in genres:
        parsed_genres.append(genre.text)
    for comment in comments:
        parsed_comments.append(comment.find(class_='black').text)
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
