from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def parse_book(url, book_id) -> dict:
    response = requests.get(f'{url}/b{book_id}')
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('div', id='content').find('h1')
    img = soup.find('table').find('div', class_='bookimage').find('img')['src']
    img_link = urljoin(url, img)
    comments = soup.find_all(class_='texts')
    grouped_comments = []
    for comment in comments:
        grouped_comments.append(comment.find(class_='black').text)
    return {'image_link': img_link,
            'book_title': title.text.split('::')[0].strip(),
            'comments': grouped_comments
    }


a = []
print(a is True)