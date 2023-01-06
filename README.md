# Book scraper:
Scraper script to download books, images and comments from tululu.ru.

### How to execute:

- Download or clone [repo](https://github.com/Ash2803/book-parser)
- You must have Python 3.9 or higher already installed;
- Create the virtual environment using command:
```
python3 -m venv venv
```
- Install the requirements using command:
```
pip install -r requirements.txt
``` 
### Scraping books
There are 6 variables in `tululu.py`: 
- `--start_page` - specify the starting page of books collection,
from which you will start scraping and downloading books, you can specify only `start_page` then the
script will start scraping books from that page till the end, default value is `1`;
- `--end_page` - which specify final page, where the scraping ends, default value is `999`;
- `--dest_folder` - specify the path where all the scraped books will be stored, default path is `Books`;
- `--skip_imgs` - if set as a script execution argument (e.g. `python tululu.py --skip_imgs`),
images won't be downloaded;
- `--skipt_txt` - if set as a script execution argument (e.g. `python tululu.py --skip_txt`),
txt books won't be downloaded;
- `--json_path` - specify the path where the json file will be saved, default path is `Books`;

Script execution examples:
```
python tululu.py --start_page 1 --skip_imgs
python tululu.py --start_page 10 --end_page 40 --skip_txt
```

### Project Goals

The code is written for educational purposes at online-course for web-developers [dvmn.org](https://dvmn.org/)
