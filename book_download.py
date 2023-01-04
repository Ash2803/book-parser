import os
import urllib.parse
from pathlib import Path

import requests
from pathvalidate import sanitize_filename


def download_book_comments(parsed_book: dict, book_id: int):
    """ Download books comments """
    images_dir_path = Path('comments')
    images_dir_path.mkdir(parents=True, exist_ok=True)
    comments = parsed_book['comments']
    parsed_book_name = f'{sanitize_filename(parsed_book["book_title"])}.txt'
    with open(images_dir_path / f'{book_id}. {parsed_book_name}', 'w') as file:
        for comment in comments:
            if comment:
                file.write(f'{comment}\n')


def download_book_image(parsed_book: dict, book_id: int):
    """ Download books images """
    images_dir_path = Path('images')
    images_dir_path.mkdir(parents=True, exist_ok=True)
    book_image_link = parsed_book['image_link']
    split_url = urllib.parse.urlsplit(book_image_link)
    split_domain = urllib.parse.unquote(split_url[2])
    file_format = os.path.splitext(split_domain)
    if file_format[1] != '.gif':
        response = requests.get(book_image_link)
        response.raise_for_status()
        parsed_book_name = f'{sanitize_filename(parsed_book["book_title"])}.jpg'
        with open(images_dir_path / f'{book_id}. {parsed_book_name}', 'wb') as file:
            file.write(response.content)


def download_book_txt(parsed_book: dict, book_id: int):
    """ Download books in txt format"""
    book_dir_path = Path('books')
    book_dir_path.mkdir(parents=True, exist_ok=True)
    txt_book_link = parsed_book['txt_book_link']
    response = requests.get(txt_book_link)
    response.raise_for_status()
    parsed_book_name = f'{sanitize_filename(parsed_book["book_title"])}.txt'
    with open(book_dir_path / f'{book_id}. {parsed_book_name}', 'wb') as file:
        file.write(response.content)
