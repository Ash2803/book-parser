from book_download import download_book_txt, download_book_image, download_book_comments


def main():
    genre = 'Биографии и мемуары'
    url = 'https://tululu.org'
    download_book_comments()
    download_book_image()
    download_book_txt(url, genre, 13, 40)


if __name__ == '__main__':
    main()