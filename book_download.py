import logging
import os
import urllib.parse
from pathlib import Path

import requests
from pathvalidate import sanitize_filename

from parse import check_for_redirect, RedirectedPage


def download_book_comments(book_comments, book_title, book_num: int, dest_folder: str):
    """ Download books comments """
    catalogue_path = Path(dest_folder)
    catalogue_path.mkdir(parents=True, exist_ok=True)
    comments_dir_path = Path(catalogue_path, 'comments')
    comments_dir_path.mkdir(parents=False, exist_ok=True)
    comments = book_comments
    parsed_book_name = f'{sanitize_filename(book_title)}.txt'
    with open(comments_dir_path / f'{book_num}. {parsed_book_name}', 'w') as file:
        for comment in comments:
            if comment:
                file.write(f'{comment}\n')


def download_book_image(book_image_link, book_title, book_num: int, dest_folder: str):
    """ Download books images """
    catalogue_path = Path(dest_folder)
    catalogue_path.mkdir(parents=True, exist_ok=True)
    images_dir_path = Path(catalogue_path, 'images')
    images_dir_path.mkdir(parents=True, exist_ok=True)
    split_url = urllib.parse.urlsplit(book_image_link)
    split_domain = urllib.parse.unquote(split_url[2])
    file_format = os.path.splitext(split_domain)
    if file_format[1] != '.gif':
        response = requests.get(book_image_link)
        response.raise_for_status()
        parsed_book_name = f'{sanitize_filename(book_title)}.jpg'
        image_path = os.path.join(images_dir_path, parsed_book_name)
        with open(images_dir_path / f'{book_num}. {parsed_book_name}', 'wb') as file:
            file.write(response.content)
        return image_path


def download_book_txt(txt_book_link, book_title, book_num: int, dest_folder: str):
    """ Download books in txt format"""
    catalogue_path = Path(dest_folder)
    catalogue_path.mkdir(parents=True, exist_ok=True)
    book_dir_path = Path(catalogue_path, 'books')
    book_dir_path.mkdir(parents=True, exist_ok=True)
    try:
        response = requests.get(txt_book_link)
        response.raise_for_status()
        check_for_redirect(response)
        parsed_book_name = f'{sanitize_filename(book_title)}.txt'
        book_path = os.path.join(book_dir_path, parsed_book_name)
        with open(book_dir_path / f'{book_num}. {parsed_book_name}', 'wb') as file:
            file.write(response.content)
        return book_path
    except RedirectedPage:
        logging.exception('Redirected page')

