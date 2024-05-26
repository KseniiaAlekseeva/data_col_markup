# Задание 1
# - использовать библиотеку requests в Python для отправки запросов GET, POST, PUT и DELETE
# на конечную точку REST API https://jsonplaceholder.typicode.com/posts/1.
# - использовать методы requests.get(), requests.post(), requests.put() и requests.delete()
# для отправки соответствующих HTTP-запросов.
# - проверить код состояния ответа и вывести текст ответа, если запрос был успешным.

import json
import requests

get_url = 'https://jsonplaceholder.typicode.com/posts/1'
response = requests.get(get_url)
if response.status_code == 200:
    print(response.text)

post_url = 'https://jsonplaceholder.typicode.com/posts'
data = {
    "userId": 1,
    "id": 1,
    "title": "My title",
    "body": "My body"
}

response = requests.post(post_url, json=data)
if response.status_code == 201:
    print(response.text)
else:
    print(f'Request failed: status {response.status_code}')

data = {'field1': 'value1', 'field2': 'value2'}
response = requests.put(get_url, json=data)
if response.status_code == 200:
    print(response.text)
else:
    print(f'Request failed: status {response.status_code}')

response = requests.delete(get_url)
if response.status_code == 200:
    print(response.text)
else:
    print(f'Request failed: status {response.status_code}')