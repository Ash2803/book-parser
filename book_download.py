import requests
from pathlib import Path


def download_book():
    book_dir_path = Path('books')
    book_dir_path.mkdir(parents=True, exist_ok=True)
    for book_id in range(10):
        url = f'https://tululu.org/txt.php?id={book_id}'
        response = requests.get(url)
        response.raise_for_status()
        with open(book_dir_path / f'Book_{book_id}.txt', 'wb') as file:
            file.write(response.content)


def main():
    download_book()


if __name__ == '__main__':
    main()
