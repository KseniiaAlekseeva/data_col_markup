from pymongo import MongoClient
import json

import sys

file_path = 'log1.txt'
sys.stdout = open(file_path, "w")

def insert_data(collection, filename: str):
    with open(filename, 'r') as file:
        data = json.load(file)
    collection.insert_many(data)


client = MongoClient("mongodb://localhost:27017/")
db = client['book_data']
books = db['books']

# insert_data(books, '../homework2/book_data.json')

# вывод первой записи в коллекции
all_docs = books.find()
first_doc = all_docs[0]
pretty_json = json.dumps(first_doc, indent=4, default=str)
print(pretty_json)

# Получение количества документов в коллекции с помощью функции count_documents()
count = books.count_documents({})
print(f'Число записей в базе данных: {count}')

# фильтрация документов по критериям
filter = {"Amount": 19}
print(f"Количество документов c Amount=19: {books.count_documents(filter=filter)}")

# Использование проекции
projection = {"Name": 1, "Description": 1, "_id": 0}
proj_docs = books.find(filter=filter, projection=projection)
for doc in proj_docs:
    print(doc)

# Использование оператора $lt и $gte
query = {"Price": {"$lt": 19}}
print(f"Количество документов c категорией Price < 19: {books.count_documents(query)}")
query = {"Price": {"$gte": 19}}
print(f"Количество документов c категорией Price >= 19: {books.count_documents(query)}")

# Использование оператора $regex
filter = {"Name": {"$regex": "rain", "$options": "i"}}
projection = {"Name": 1, "_id": 0}
print(f"Количество документов, содержащих 'rain': {books.count_documents(filter=filter)}")
proj_docs = books.find(filter=filter, projection=projection)
for doc in proj_docs:
    print(doc)

# Использование оператора $in
filter = {"Amount": {"$in": [1, 2, 3]}}
print(f"Количество документов в категории Amount = 1, 2 или 3: {books.count_documents(filter=filter)}")

# Использование оператора $all
filter = {"Amount": {"$all": [22]}}
print(f"Количество документов в категории Amount = 22: {books.count_documents(filter=filter)}")

# Использование оператора $ne
filter = {"Amount": {"$ne": 22}}
print(f"Количество документов в категории Amount <> 22: {books.count_documents(filter=filter)}")
