# Book scraper:
Scraper script to download books, images and comments from tululu.ru.

### How to execute:

- Download or clone [repo](https://github.com/Ash2803/book-parser)
- You must have Python 3.6 or higher already installed;
- Create the virtual environment using command:
```
python3 -m venv venv
```
- Install the requirements using command:
```
pip install -r requirements.txt
``` 
### Scraping book
There are 2 variables in `tululu.py`: `start_id` - specify the starting book ID,
from which you will start scraping and downloading books and `end_id` - which specify final ID,
where the scraping ends. Default values is `start_id=600` and `end_id=640`.
- Запуск скрипта:
```
python tululu.py --start_id 5 --end_id 30
```
You can specify genre of book  `tululu.py`. Default value is "Научная фантастика".
```python
genre = 'Научная фантастика'
```
The list of genres is available on the [website](https://tululu.org).

### Project Goals

The code is written for educational purposes at online-course for web-developers [dvmn.org](https://dvmn.org/)
