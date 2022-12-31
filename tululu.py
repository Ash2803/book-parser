import argparse

from book_download import download_book_txt, download_book_image, download_book_comments
from parse import get_book_page, parse_book_page, check_for_redirect, RedirectedPage


def main():
    parser = argparse.ArgumentParser(description='Download books')
    parser.add_argument('--start_id', type=int, help='Enter start id', default=600)
    parser.add_argument('--end_id', type=int, help='Enter final id', default=640)
    args = parser.parse_args()
    genre = 'Деловая литература'
    url = 'https://tululu.org'
    for book_id in range(args.start_id, args.end_id):
        try:
            book_page = get_book_page(url, book_id)
            check_for_redirect(book_page)
            parsed_book_page = parse_book_page(book_page)
        except RedirectedPage:
            continue
        except TypeError:
            continue
        download_book_comments(parsed_book_page, genre, book_id)
        download_book_image(parsed_book_page, genre, book_id)
        download_book_txt(parsed_book_page, genre, book_id)


if __name__ == '__main__':
    main()
