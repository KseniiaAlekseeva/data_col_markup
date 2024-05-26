import time

import pandas
import requests
from lxml import html
from pymongo import MongoClient


def one_page_scrape(url: str) -> list:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    tree = html.fromstring(response.content)

    header_xpath = "//table[@id='example2']/thead/tr/th"
    header = tree.xpath(header_xpath)
    col_names = []
    for col in header:
        col_names.append(" ".join(i.strip() for i in col.xpath(".//text()")))

    xpath = "//table[@id='example2']/tbody/tr"
    rows = tree.xpath(xpath)
    data = []
    num_rows = 0
    for j in range(len(rows)):
        row_data = rows[j].xpath(".//td")
        row_dict = {}
        for i in range(len(col_names)):
            cell = row_data[i].xpath(".//text()")
            row_dict[col_names[i]] = cell[0] if len(cell) > 0 else 0
        data.append(row_dict)

        if j % 30 == 0:
            time.sleep(1)
            print(f"{j} rows loaded...")
    print(f"{j} rows loaded...")
    return data


def persist_to_mongo_csv(data: list):
    client = MongoClient("mongodb://localhost:27017/")
    db = client['sport_db']
    table = db['women60']
    table.insert_many(data)


def persist_to_csv(data: list, file: str):
    df = pandas.DataFrame(data)
    df.to_csv(file, mode='w', index=False)


def main():
    url = "https://www.worldometers.info/world-population/population-by-country/"
    data = one_page_scrape(url)
    # persist_to_mongo_csv(data)
    persist_to_csv(data, 'population.csv')


main()
