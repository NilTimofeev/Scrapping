import requests
import json

url = 'https://api.github.com/users/NilTimofeev/repos'
response = requests.get(url)

data = json.loads(response.text)

for val in data:
    print(val['name'])

with open('repo.json', 'w') as json_file:
    json.dump(data, json_file)
