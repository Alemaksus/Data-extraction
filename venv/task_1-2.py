# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию
# (любого типа). Выполнить запросы к нему, пройдя авторизацию.
# Ответ сервера записать в файл.

import requests
import json
from fake_headers import Headers

header = Headers(Headers=True).generate()

url = 'https://cloud-api.yandex.net/'
response = requests.get(url, headers=header)

token = '3d48f3e21c7a4c1db76e98dbe52bb786'

headers = {
    'Content-Type': 'application/json',
    'Authorization': token
}

disk_info = 'disk'
folder_info = 'disk/resources'

disk = requests.get(f'{url}{disk_info}')

disk.json()

disk = requests.get(f'{url}{disk_info}', headers = headers)
disk.json()

disk = requests.get(f'{url}{folder_info}?path=app:/', headers = headers)

# Названия файлов в папке

for i in disk.json()['_embedded']['items']:
    print(i['name'])

with open('disk.json', 'w') as f:
    json.dump(disk.json(), f)