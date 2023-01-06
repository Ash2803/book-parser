import json
import logging
import time

import requests

from book_download import download_book_txt, download_book_image, download_book_comments
from parse import get_book_page, parse_book_page, check_for_redirect, RedirectedPage
from parse_tululu_category import parse_category, get_collection


def main():
    logging.basicConfig(format="%(lineno)d %(funcName)s %(filename)s %(levelname)s %(message)s")
    for page in range(1, 2):
        url = f'https://tululu.org/l55/{page}/'
        collection = get_collection(url)
        books_links = parse_category(collection)
        books = []
        for index, book_link in enumerate(books_links, 1):
            try:
                book_page = get_book_page(book_link, page)
                check_for_redirect(book_page)
                parsed_book_page = parse_book_page(book_page)
                download_book_comments(parsed_book_page, index)
                books.append({
                    'Title': parsed_book_page["book_title"],
                    'Author': parsed_book_page["author"],
                    'Image': download_book_image(parsed_book_page, index),
                    'Book path': download_book_txt(parsed_book_page, index),
                    'Genres': parsed_book_page["genres"],
                    'Comments': parsed_book_page['comments']
                })
            except requests.exceptions.ConnectionError:
                logging.exception('Connection lost')
                time.sleep(10)
            except requests.exceptions.HTTPError:
                logging.exception('Invalid url')
            except TypeError:
                logging.exception('There is no available book to download')
                continue
            except RedirectedPage:
                logging.exception('URL had been redirected')
                continue
        with open('books.json', "w") as my_file:
            json.dump(books, my_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
