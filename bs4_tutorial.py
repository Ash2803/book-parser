import requests
from bs4 import BeautifulSoup


def parse_post(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    # print(response.text)
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('div', id='content').find('h1')
    return title_tag.text.split('::')[0].strip()

