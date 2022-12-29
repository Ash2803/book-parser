import os
import urllib.parse
from pathlib import Path

import requests
from pathvalidate import sanitize_filename

from parse import parse_book_page, LinkNotFoundError, RedirectedPage


def download_book_comments(url: str, genre: str, start_id: int, end_id: int):
    """ Download books comments """
    images_dir_path = Path('comments')
    images_dir_path.mkdir(parents=True, exist_ok=True)
    for book_id in range(start_id, end_id):
        try:
            book = parse_book_page(url, book_id)
            if genre in book['genres']:
                comments = book['comments']
                parsed_book_name = f'{sanitize_filename(book["book_title"])}.txt'
                with open(images_dir_path / f'{book_id}. {parsed_book_name}', 'w') as file:
                    for comment in comments:
                        if comment:
                            file.write(f'{comment}\n')
        except LinkNotFoundError:
            continue
        except RedirectedPage:
            continue


def download_book_image(url: str, genre: str, start_id: int, end_id: int):
    """ Download books images """
    images_dir_path = Path('images')
    images_dir_path.mkdir(parents=True, exist_ok=True)
    for book_id in range(start_id, end_id):
        try:
            book_page = parse_book_page(url, book_id)
            if genre in book_page['genres']:
                book_image_link = book_page['image_link']
                split_url = urllib.parse.urlsplit(book_image_link)
                split_domain = urllib.parse.unquote(split_url[2])
                file_format = os.path.splitext(split_domain)
                if file_format[1] != '.gif':
                    response = requests.get(book_image_link)
                    response.raise_for_status()
                    parsed_book_name = f'{sanitize_filename(book_page["book_title"])}.jpg'
                    with open(images_dir_path / f'{book_id}. {parsed_book_name}', 'wb') as file:
                        file.write(response.content)
        except LinkNotFoundError:
            continue
        except RedirectedPage:
            continue


def download_book_txt(url: str, genre: str, start_id: int, end_id: int):
    """ Download books in txt format"""
    book_dir_path = Path('books')
    book_dir_path.mkdir(parents=True, exist_ok=True)
    for book_id in range(start_id, end_id):
        try:
            book_page = parse_book_page(url, book_id)
            if genre in book_page['genres']:
                txt_book_link = book_page['txt_book_link']
                response = requests.get(txt_book_link)
                response.raise_for_status()
                parsed_book_name = f'{sanitize_filename(book_page["book_title"])}.txt'
                with open(book_dir_path / f'{book_id}. {parsed_book_name}', 'wb') as file:
                    file.write(response.content)
                print(f'Название: {book_page["book_title"]}\nАвтор: {book_page["author"]}')
        except LinkNotFoundError:
            continue
        except RedirectedPage:
            continue
