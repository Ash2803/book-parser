import requests
from pathlib import Path


def download_book():
    book_dir_path = Path('books')
    book_dir_path.mkdir(parents=True, exist_ok=True)
    for book_id in range(11):
        params = {
            'id': book_id
        }
        response = requests.get('https://tululu.org/txt.php', params=params)
        response.raise_for_status()
        try:
            check_for_redirect(response)
            with open(book_dir_path / f'Book_{book_id}.txt', 'wb') as file:
                file.write(response.content)
        except requests.HTTPError:
            pass


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def main():
    download_book()


if __name__ == '__main__':
    main()
