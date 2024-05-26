# Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/
# и извлечь информацию о всех книгах на сайте во всех категориях:
# название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.
# Затем сохранить эту информацию в JSON-файле.
import urllib.parse
import re

import pandas
import requests
import json
import time
from bs4 import BeautifulSoup


def get_book_data():
    url = "http://books.toscrape.com"
    catalogue_url = "http://books.toscrape.com/catalogue/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    count = int(soup.find("li", class_="current").text.strip().split("of ")[1]) + 1
    book_urls = []
    for i in range(1, count):
        page_url = f"http://books.toscrape.com/catalogue/page-{i}.html"
        response = requests.get(page_url)
        page = BeautifulSoup(response.content, 'html.parser')
        books = page.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        for book in books:
            book_urls.append(urllib.parse.urljoin(catalogue_url, book.find("h3").find("a").get("href")))

    data = []
    book_num = 0
    for book_url in book_urls:
        book_dict = {}
        response = requests.get(book_url)
        book = BeautifulSoup(response.content, 'html.parser')
        book_dict["Name"] = book.find("div", class_="col-sm-6 product_main").find("h1").text
        try:
            book_dict["Price"] = float(re.findall("\d+\.\d+", book.find("p", class_="price_color").text)[0])
            book_dict["Amount"] = int(book.find("p", class_="instock availability").text.split("(")[1].split()[0])
            book_dict["Description"] = book.find("div", id="product_description").findNext("p").text
        except AttributeError:
            book_dict["Price"] = None
            book_dict["Amount"] = None
            book_dict["Description"] = None
        if book_dict:
            book_num += 1
            data.append(book_dict)
            print(f'Loading {book_num}...')
        if book_num % 10 == 0:
            time.sleep(1)
    return data


def save_to_json(data, filename='book_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def save_to_csv(data, filename='book_data.csv'):
    df = pandas.DataFrame(data)
    df.to_csv(filename)
    print(df)


if __name__ == "__main__":
    data = get_book_data()
    save_to_json(data)
    save_to_csv(data)
