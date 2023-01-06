import os
import urllib.parse
from pathlib import Path

import requests
from pathvalidate import sanitize_filename


def download_book_comments(parsed_book: dict, book_id: int, dest_folder: str):
    """ Download books comments """
    catalogue_path = Path(dest_folder)
    catalogue_path.mkdir(parents=True, exist_ok=True)
    comments_dir_path = Path(catalogue_path, 'comments')
    comments_dir_path.mkdir(parents=False, exist_ok=True)
    comments = parsed_book['comments']
    parsed_book_name = f'{sanitize_filename(parsed_book["book_title"])}.txt'
    with open(comments_dir_path / f'{book_id}. {parsed_book_name}', 'w') as file:
        for comment in comments:
            if comment:
                file.write(f'{comment}\n')


def download_book_image(parsed_book: dict, book_id: int, dest_folder: str, skip_imgs: bool):
    """ Download books images """
    if skip_imgs:
        catalogue_path = Path(dest_folder)
        catalogue_path.mkdir(parents=True, exist_ok=True)
        images_dir_path = Path(catalogue_path, 'images')
        images_dir_path.mkdir(parents=True, exist_ok=True)
        book_image_link = parsed_book['image_link']
        split_url = urllib.parse.urlsplit(book_image_link)
        split_domain = urllib.parse.unquote(split_url[2])
        file_format = os.path.splitext(split_domain)
        if file_format[1] != '.gif':
            response = requests.get(book_image_link)
            response.raise_for_status()
            parsed_book_name = f'{sanitize_filename(parsed_book["book_title"])}.jpg'
            with open(images_dir_path / f'{book_id}. {parsed_book_name}', 'wb') as file:
                file.write(response.content)
            return os.path.join(images_dir_path, parsed_book_name)


def download_book_txt(parsed_book: dict, book_id: int, dest_folder: str, skip_txt: bool):
    """ Download books in txt format"""
    if skip_txt:
        catalogue_path = Path(dest_folder)
        catalogue_path.mkdir(parents=True, exist_ok=True)
        book_dir_path = Path(catalogue_path, 'books')
        book_dir_path.mkdir(parents=True, exist_ok=True)
        txt_book_link = parsed_book['txt_book_link']
        response = requests.get(txt_book_link)
        response.raise_for_status()
        parsed_book_name = f'{sanitize_filename(parsed_book["book_title"])}.txt'
        with open(book_dir_path / f'{book_id}. {parsed_book_name}', 'wb') as file:
            file.write(response.content)
            return os.path.join(book_dir_path, parsed_book_name)
