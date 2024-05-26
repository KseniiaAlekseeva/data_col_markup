# - установите библиотеку Beautiful Soup.
# - создайте новый сценарий Python и импортируйте библиотеку Beautiful Soup.
# - напишите код для запроса веб-страницы https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab
# с помощью библиотеки requests.
# - выведите HTML-содержимое веб-страницы в консоль.
import urllib.parse

import requests
from bs4 import BeautifulSoup
import pandas

url = "https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab"
base_url = "https://www.boxofficemojo.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
# print(soup.prettify())

parse = []
# <td class="a-text-left mojo-field-type-release mojo-cell-wide">
for link in soup.find_all("td", {"class": "a-text-left mojo-field-type-release mojo-cell-wide"}):
    href = link.find("a")
    if href:
        parse.append(href.get("href"))
# print(parse)

join_parse = [urllib.parse.urljoin(base_url, link) for link in parse]
# print(join_parse)

# <table class="a-bordered a-horizontal-stripes a-size-base a-span12 mojo-body-table mojo-table-annotated"><tbody><tr>
tab = soup.find("table", {"class": "a-bordered"})
headers = [header.text.strip() for header in tab.find_all("th") if header.text]

data = []

for row in tab.find_all("tr"):
    row_dict = {}
    cells = row.find_all("td")
    if cells:
        row_dict[headers[0]] = cells[0].find("a").text if cells[0].find("a") else ""
        row_dict[headers[1]] = cells[1].text
        row_dict[headers[2]] = cells[2].text
        row_dict[headers[3]] = cells[3].find("a").text if cells[3].find("a") else ""
        row_dict[headers[4]] = cells[4].text.strip()
        row_dict[headers[5]] = cells[5].text.replace("$", "").replace(",", "")
        data.append(row_dict)
print(data)

df = pandas.DataFrame(data)
print(df)
