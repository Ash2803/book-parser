import argparse

from book_download import download_book_txt, download_book_image, download_book_comments


def main():
    parser = argparse.ArgumentParser(description='Download books')
    parser.add_argument('start_id', type=int, help='Enter start id')
    parser.add_argument('end_id', type=int, help='Enter final id')
    args = parser.parse_args()
    genre = 'Научная фантастика'
    url = 'https://tululu.org'
    download_book_comments(url, genre, args.start_id, args.end_id)
    download_book_image(url, genre, args.start_id, args.end_id)
    download_book_txt(url, genre, args.start_id, args.end_id)


if __name__ == '__main__':
    main()
