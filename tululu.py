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
        try:
            url = f'https://tululu.org/l55/{page_number}/'
            collection_page = get_page(url)
            try:
                check_for_redirect(collection_page)
            except RedirectedPage:
                logging.exception('Redirected page')
                break
            books_links = parse_category(collection_page)
            books = []
            for book_num, book_link in enumerate(books_links, 1):
                book_page = get_page(book_link)
                check_for_redirect(book_page)
                parsed_book_page = parse_book_page(book_page)
                book_title = parsed_book_page["book_title"]
                book_author = parsed_book_page["author"]
                book_genres = parsed_book_page["genres"]
                book_comments = parsed_book_page["comments"]
                txt_book_link = parsed_book_page["txt_book_link"]
                book_image_link = parsed_book_page["image_link"]
                book_image_path = ''
                if not args.skip_imgs:
                    book_image_path = download_book_image(book_image_link, book_title, book_num, args.dest_folder)
                txt_book_path = ''
                if not args.skip_txt:
                    txt_book_path = download_book_txt(txt_book_link, book_title, book_num, args.dest_folder)
                download_book_comments(book_comments, book_title, book_num, args.dest_folder)
                print(dedent(f'''\
                    Title: {book_title}
                    Author: {book_author}
                    Genres: {book_genres}'''))
                books.append({
                    'Title': book_title,
                    'Author': book_author,
                    'Image': book_image_path,
                    'Book path': txt_book_path,
                    'Genres': book_genres,
                    'Comments': book_comments
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
