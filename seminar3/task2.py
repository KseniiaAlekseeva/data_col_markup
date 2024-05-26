import collections

from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
db = client['town_cary']
crashes = db['crashes']
data = crashes.find()
first_el = data[0]

print(crashes)
print(data)
print(first_el)
first_el_json = json.dumps(first_el, indent=4, default=str)
print(first_el_json)

crashes_count = crashes.count_documents({})
print(crashes_count)

filter = {'properties.fatalities': 'Yes'}
print(crashes.count_documents(filter=filter))

projection = {"_id": 0, "properties.lightcond": 1, "properties.weather": 1}
fatal_data = crashes.find(filter=filter, projection=projection)
for el in fatal_data:
    print(el)

print("Greater then 6: ", crashes.count_documents(filter={"properties.month": {"$gte": "6"}}))
print("Less then 6: ", crashes.count_documents(filter={"properties.month": {"$lt": "6"}}))
