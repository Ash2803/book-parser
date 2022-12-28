import os
from pathlib import Path

import requests
from pathvalidate import sanitize_filename

from bs4_tutorial import parse_post


def download_txt(url):
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
            parsed_book_name = f'{sanitize_filename(parse_post(book_id))}.txt'
            with open(book_dir_path / f'{book_id}. {parsed_book_name}', 'wb') as file:
                file.write(response.content)
        except requests.HTTPError:
            pass


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def main():
    download_txt('https://tululu.org/txt.php')


if __name__ == '__main__':
    main()
