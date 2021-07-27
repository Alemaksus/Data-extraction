# Необходимо собрать информацию по продуктам питания  сайтов:

# https://rskrf.ru/ratings/produkty-pitaniya/
# https://roscontrol.com/category/produkti/#popup

# Получившийся список должен содержать:

# - Наименование продукта.
# - Категорию продукта (например «Бакалея»).
# - Подкатегорию продукта (например «Рис круглозерный»).
# - Параметр «Безопасность».
# - Параметр «Качество».
# - Общий балл.
# - Сайт, откуда получена информация.

### Структура должна быть одинаковая для продуктов с обоих сайтов.

# Общий результат можно вывести с помощью dataFrame через Pandas.

from bs4 import BeautifulSoup
import requests
import lxml
from fake_headers import Headers
import pandas as pd

header = Headers(headers=True).generate()

url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=python+developer&customDomain=1&page={}'

pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

siteName = 'hh_ru'
save = [] # - сборка для DF

for i in pages:
    try:
        page_url = url.format(i)
        response = requests.get(page_url, headers=header)
        soup = BeautifulSoup(response.text, 'lxml')
        names = [i.text for i in soup.select('span.g-user-content a.bloko-link')][:10] # bloko-link класс наименования вакансии
        salary = [i.text for i in soup.select('div.vacancy-serp-item__sidebar span.bloko-header-section-3.bloko-header-section-3_lite')][:10] # bloko-header-section-3_lite - класс з/пл
        for index, j in enumerate(names):
            save.append({
                'name': j,
                'salary': salary[index],
                'site': siteName
            })
    except:
        pass

pd.DataFrame(save).to_csv('gb_2_hh.csv')