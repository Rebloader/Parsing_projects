import aiohttp
import asyncio
import re
import json
from bs4 import BeautifulSoup

baseurl = 'https://books.toscrape.com/catalogue/'


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()


async def scrape_books():
    page_num = 1
    books_description = []
    async with aiohttp.ClientSession() as session:
        while True:
            url = f'https://books.toscrape.com/catalogue/page-{page_num}.html'
            html = await fetch(url, session)

            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

            if not links:
                break

            for link in links:
                link_a = link.find('a')
                if link_a:
                    book_url = baseurl + link_a['href']
                    books_description.append(await extract_book_data(book_url, session))
            page_num += 1
    return books_description


async def extract_book_data(url, session):
    html = await fetch(url, session)
    soup = BeautifulSoup(html, 'html.parser')

    book_data = {}
    for book in soup.find_all('div', {'class': 'col-sm-6 product_main'}):
        title = book.find('h1').text.strip()
        price = book.find('p', {'class': 'price_color'}).text.strip()
        available_text = book.find('p', {'class': 'instock availability'}).text.strip()
        available = extract_quantity(available_text)
        book_data.update({'title': title, 'price': price, 'available': available})
        print(f'{title} | {price} | {available}')
    return book_data


def extract_quantity(text):
    match = re.search(r'\d+', text)
    if match:
        return float(match.group())
    return 0


async def main():
    books_data = await scrape_books()
    with open('books_description.json', 'w+', encoding='utf-8') as outfile:
        json.dump(books_data, outfile, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    asyncio.run(main())
