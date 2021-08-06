# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import json
import requests

url = 'https://api.github.com'
user = 'Alemaksus'

repos = requests.get(f'{url}/users/{user}/repos')

with open('data.json', 'w') as f:
    json.dump(repos.json(), f)

for i in repos.json():
    print(i['name'])