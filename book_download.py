import os
import traceback
from pathlib import Path

import requests
from pathvalidate import sanitize_filename
import urllib.parse
from parse import parse_book


def download_book_comments(url):
    images_dir_path = Path('comments')
    images_dir_path.mkdir(parents=True, exist_ok=True)
    for book_id in range(4, 11):
        try:
            comments = parse_book(url, book_id)['comments']
            parsed_book_name = f'{sanitize_filename(parse_book(url, book_id)["book_title"])}.txt'
            with open(images_dir_path / f'{book_id}. {parsed_book_name}', 'w') as file:
                for comment in comments:
                    if comment:
                        file.write(f'{comment}\n')
        except requests.ConnectTimeout:
            print(traceback.format_exc())


def download_book_image(url):
    images_dir_path = Path('images')
    images_dir_path.mkdir(parents=True, exist_ok=True)
    for book_id in range(4, 11):
        img_link = parse_book(url, book_id)['image_link']
        split_url = urllib.parse.urlsplit(img_link)
        split_domain = urllib.parse.unquote(split_url[2])
        file_format = os.path.splitext(split_domain)
        if file_format[1] != '.gif':
            try:
                response = requests.get(img_link)
                response.raise_for_status()
                parsed_book_name = f'{sanitize_filename(parse_book(url, book_id)["book_title"])}.jpg'
                with open(images_dir_path / f'{book_id}. {parsed_book_name}', 'wb') as file:
                    file.write(response.content)
            except requests.ConnectionError:
                print(traceback.format_exc())


def download_book_txt(url):
    book_dir_path = Path('books')
    book_dir_path.mkdir(parents=True, exist_ok=True)
    for book_id in range(11):
        params = {
            'id': book_id
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        try:
            check_for_redirect(response)
            parsed_book_name = f'{sanitize_filename(parse_book(book_id)["book_title"])}.txt'
            with open(book_dir_path / f'{book_id}. {parsed_book_name}', 'wb') as file:
                file.write(response.content)
        except requests.HTTPError:
            print(traceback.format_exc())


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def main():
    url = 'https://tululu.org'
    download_book_comments(url)


if __name__ == '__main__':
    main()
