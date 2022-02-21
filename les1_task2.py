import requests
import json

url = 'https://api.vk.com/method/groups.get'

ver = '5.131'
user_id = input('Введите user_id: ')
access_token = input('Введите access_token: ')

params = {'user_id': user_id, 'access_token': access_token, 'v': ver}
response = requests.get(url, params)

data = json.loads(response.text)
print(data)

with open('groups.json', 'w') as json_file:
    json.dump(data, json_file)
