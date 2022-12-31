import argparse
import logging
import time

import requests

from book_download import download_book_txt, download_book_image, download_book_comments
from parse import get_book_page, parse_book_page, check_for_redirect, RedirectedPage


def main():
    parser = argparse.ArgumentParser(description='Download books')
    parser.add_argument('--start_id', type=int, help='Enter start id', default=600)
    parser.add_argument('--end_id', type=int, help='Enter final id', default=640)
    args = parser.parse_args()
    genre = 'Деловая литература'
    url = 'https://tululu.org'
    logging.basicConfig(format="%(lineno)d %(funcName)s %(filename)s %(levelname)s %(message)s")
    for book_id in range(args.start_id, args.end_id):
        try:
            time.sleep(5)
            try:
                book_page = get_book_page(url, book_id)
                check_for_redirect(book_page)
                parsed_book_page = parse_book_page(book_page)
            except RedirectedPage:
                logging.error('URL has been redirected')
                continue
            except TypeError:
                logging.error('There is no available book to download')
                continue
            if genre in parsed_book_page['genres']:
                download_book_comments(parsed_book_page, genre, book_id)
                download_book_image(parsed_book_page, genre, book_id)
                download_book_txt(parsed_book_page, genre, book_id)
                print(f'Название: {parsed_book_page["book_title"]}\n'
                      f'Автор: {parsed_book_page["author"]}\n'
                      f'Жанр: {parsed_book_page["genres"]}')
        except requests.exceptions.ConnectionError:
            logging.error('Connection lost')
        except requests.exceptions.HTTPError:
            logging.error('Invalid url')


if __name__ == '__main__':
    main()
