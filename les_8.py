import requests
import geojson
from pymongo import MongoClient
import folium
import pandas as pd

client = MongoClient('localhost', 27017)
mongobase = client.velo
collection = mongobase['bike_paths']

api_key = input('Input API-key: ')
params = {'api_key': api_key}
url = 'https://apidata.mos.ru/v1/datasets/897/features'
response = requests.get(url, params=params)

data = geojson.loads(response.text)

for i in range(len(data['features'])):
    collection.insert_one(data['features'][i]['properties']['Attributes'])

map_obj = folium.Map(location=[55.727883425773065, 37.457199096679695], zoom_start=11)
folium.GeoJson(data=response.text, name='velo').add_to(map_obj)
map_obj.save('output.html')

cursor = collection.find()
dataframe = pd.DataFrame(list(cursor))
del dataframe['_id']

print(dataframe.info())
