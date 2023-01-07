import argparse
import json
import logging
import time
from pathlib import Path
from textwrap import dedent

import requests

from book_download import download_book_txt, download_book_image, download_book_comments
from parse import get_page, parse_book_page, check_for_redirect, RedirectedPage, parse_category


def main():
    parser = argparse.ArgumentParser(description='Download books')
    parser.add_argument('--start_page', default=0, type=int, help='Enter starting page number', )
    parser.add_argument('--end_page', default=999, type=int, help='Enter final page number')
    parser.add_argument('--dest_folder', type=str, default='Books', help='Enter catalogue path name')
    parser.add_argument('--skip_imgs', action='store_true', help='Default value is True')
    parser.add_argument('--skip_txt', action='store_true', help='Default value is True')
    parser.add_argument('--json_path', type=str, help='Enter json file path name', default='Books')
    args = parser.parse_args()
    logging.basicConfig(format="%(lineno)d %(funcName)s %(filename)s %(levelname)s %(message)s")

    for page_number in range(args.start_page, args.end_page):
        url = f'https://tululu.org/l55/{page_number}/'
        collection_page = get_page(url)
        if collection_page.history:
            logging.error('No pages left')
            break
        books_links = parse_category(collection_page)
        books = []
        for index, book_link in enumerate(books_links, 1):
            try:
                book_page = get_page(book_link)
                check_for_redirect(book_page)
                parsed_book_page = parse_book_page(book_page)
                download_book_comments(parsed_book_page, index, args.dest_folder)
                print(dedent(f'''\
                    Title: {parsed_book_page["book_title"]}
                    Author: {parsed_book_page["author"]}
                    Genres: {parsed_book_page["genres"]}'''))
                books.append({
                    'Title': parsed_book_page["book_title"],
                    'Author': parsed_book_page["author"],
                    'Image': download_book_image(parsed_book_page, index, args.dest_folder, args.skip_imgs),
                    'Book path': download_book_txt(parsed_book_page, index, args.dest_folder, args.skip_txt),
                    'Genres': parsed_book_page["genres"],
                    'Comments': parsed_book_page['comments']
                })
                json_dir_name = Path(args.json_path)
                json_dir_name.mkdir(parents=True, exist_ok=True)
                with open(json_dir_name / 'books.json', "w") as my_file:
                    json.dump(books, my_file, indent=4, ensure_ascii=False)
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


if __name__ == '__main__':
    main()
