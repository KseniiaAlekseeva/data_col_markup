import collections

from pymongo import MongoClient
import json


def chunk_data(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


client = MongoClient("mongodb://localhost:27017/")
db = client['town_cary']
crashes = db['crashes']
with open('crash-data.json', 'r') as file:
    data = json.load(file)

data = data['features']
chunk_size = 5000

for chunk in chunk_data(data, chunk_size):
    crashes.insert_many(chunk)

