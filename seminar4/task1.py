import pandas
import requests
from lxml import html
from pymongo import MongoClient


def one_page_scrape(url: str) -> list:
    response = requests.get(url)
    tree = html.fromstring(response.content)
    xpath = "//table[@class='records-table']/tbody/tr"
    rows = tree.xpath(xpath)

    data = []
    for row in rows:
        row_data = row.xpath(".//td/text()")
        row_dict = {'Rank': int(row_data[0].strip()),
                    'Mark': float(row_data[1].strip()),
                    'WIND': float(row_data[2].strip() if row_data[2].strip() else '0'),
                    'Competitor': row.xpath(".//td[4]/a/text()")[0].strip(),
                    'DOB': row_data[5].strip(),
                    'NAT': row_data[7].strip(),
                    'Pos': row_data[8].strip(),
                    'Venue': row_data[9].strip(),
                    'Date': row_data[10].strip(),
                    'ResultScore': int(row_data[11].strip())}
        # for i in range(len(header)):
        #     row_dict[header[i].strip()] = row_data[i].strip()
        data.append(row_dict)
    return data


def persist_to_mongo_csv(data: list):
    client = MongoClient("mongodb://localhost:27017/")
    db = client['sport_db']
    table = db['women60']
    table.insert_many(data)


def persist_to_csv(data: list, file: str):
    df = pandas.DataFrame(data)
    df.to_csv(file, mode='a', index=False)


def main():
    for num_page in range(1, 4):
        url = f"https://worldathletics.org/records/toplists/sprints/60-metres/indoor/women/senior/2023?page={num_page}"
        data = one_page_scrape(url)
        persist_to_mongo_csv(data)
        persist_to_csv(data, 'women60.csv')
        print(f"Page {num_page} completed...")


main()

# first_row = rows[0].xpath(".//td/text()")
# for el in first_row:
#     print(el.strip())
#
# header_xpath = "//table[@class='records-table']/thead/tr/th/text()"
# header = tree.xpath(header_xpath)
# for col in header:
#     print(col.strip())

# for el in data:
#     print(el)
