import urllib
import re
import json
import requests

from bs4 import BeautifulSoup


baseurl = 'https://books.toscrape.com/catalogue/'


def scrape_books():
    page_num = 1
    books_description = []
    while page_num == 1:
        url = f'https://books.toscrape.com/catalogue/page-{page_num}.html'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
                link_a = link.find('a')
                if link_a:
                    book_url = urllib.parse.urljoin(baseurl, link_a.get('href'))
                    books_description.append(extract_book_data(book_url))
            page_num += 1
        else:
            break
    return books_description


def extract_quantity(text):
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    return 0


def extract_book_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        book_data = []
        for book in soup.find_all('div', {'class': 'col-sm-6 product_main'}):
            title = book.find('h1').text.strip()
            price = book.find('p', {'class': 'price_color'}).text.strip()
            available_text = book.find_next('p', {'class': 'instock availability'}).text.strip()
            available = extract_quantity(available_text)

            book_data.append({'title': title, 'price': price, 'available': available})
            print(f'{title} | {price} | {available}')
        return book_data


books_dat = scrape_books()
with open('books_description.json', 'w+', encoding='utf-8') as outfile:
    json.dump(books_dat, outfile, ensure_ascii=False, indent=4)



