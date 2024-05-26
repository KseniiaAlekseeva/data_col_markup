# - Создайте сценарий Python, который запрашивает данные из Foursquare API с помощью библиотеки requests.
# - Сценарий должен предложить пользователю ввести название города.
# - Затем сценарий должен отправить запрос в Foursquare API для поиска ресторанов в указанном городе.
# - Сценарий должен обработать ответ API и извлечь название и адрес каждого ресторана.
# - Скрипт должен вывести название и адрес каждого ресторана в консоль.
#
# Требования:
# Использовать API Foursquare для получения данных.
# Использовать библиотеку requests для отправки запросов API
# Использовать библиотеку json для обработки ответа API.
# Запросить у пользователя название города
# Извлечь и вывести название и адрес каждого ресторана из ответа API.

# Работа с API для сбора и обработки данных, а затем создание DataFrame для подготовки данных к анализу.
#
# - Перенести код из блока 3 в Google Colab.
# - Модифицировать код, чтобы извлечь адрес, название ресторана, а также координаты (долгота и широта)
# - Создать pandas DataFrame из полученных данных

import json
import requests
import pandas

client_id = "__"
client_secret = "__"

endpoint = "https://api.foursquare.com/v3/places/search"
city = input('Input the city: ')
place = input('Input the place: ')

params = {'client_id': client_id,
          'client_secret': client_secret,
          'near': city,
          'query': place,
          }
headers = {
    "Accept": "application/json",
    "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
}

response = requests.get(url=endpoint, params=params, headers=headers)
if response.status_code == 200:
    print('Successful request')
    data = json.loads(response.text)
    values = data["results"]
    lst = []
    for value in values:
        name = value["name"]
        # print(f'Name: {name}')
        # try:
        # address = value["location"]["address"]
        # print('fLocation: {address}.')
        # except KeyError:
        # address = None
        address = value.get("location", {}).get("address", 'none')
        lst.append({'Name': name, 'Address': address})
    df = pandas.DataFrame(lst)
    print(df.head(10))
else:
    print(f'Request failed: code {response.status_code}')
