import numpy
import pandas
from clickhouse_driver import Client
import json

import sys

file_path = 'log2.txt'
sys.stdout = open(file_path, "w")

# Подключение к серверу ClickHouse
client = Client('localhost')

# Создание базы данных (если она не существует)
client.execute('CREATE DATABASE IF NOT EXISTS books_data')

client.execute('''
DROP TABLE IF EXISTS books_data.books
''')

# Создание таблицы
client.execute('''
CREATE TABLE IF NOT EXISTS books_data.books (
    id UInt64 Default 0,
    Name String,
    Price Nullable(Float32),
    Amount Nullable(Int64),
    Description Nullable(String)
) ENGINE = MergeTree()
ORDER BY id;
''')
print("Таблица создана успешно.")

with open('../homework2/book_data.json', 'r') as file:
    data = json.load(file)

count = 0
# Вставка данных в таблицу
for el in data:
    count += 1
    name = el['Name']
    price = el['Price']
    amount = el['Amount']
    description = el['Description']

    # print((name, price, amount, description))

    client.execute("""
    INSERT INTO books_data.books (
        id, Name, Price, Amount, Description
    ) VALUES""",
                   [(count,
                     name,
                     price,
                     amount,
                     description)],types_check=True)

print("Данные введены успешно.")

result = client.execute("SELECT COUNT(*) FROM books_data.books")
print("Записей в таблице:", result[0][0])

# Проверка успешности вставки
result = client.execute("SELECT * FROM books_data.books")
print("Вставленная запись:", result[0])
