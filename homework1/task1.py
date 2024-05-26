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
    print('Successful request...')
    data = json.loads(response.text)
    values = data["results"]
    lst = []
    for value in values:
        name = value["name"]
        address = value.get("location", {}).get("address", 'none')
        postcode = value.get("location", {}).get("postcode", 'none')
        distance = value.get("distance", 'none')
        lst.append({'Name': name, 'Address': address, 'Postcode': postcode, 'Distance': distance})
    df = pandas.DataFrame(lst)
    df.to_csv('museums.csv')
    print(df.head(20))
else:
    print(f'Request failed: code {response.status_code}')
