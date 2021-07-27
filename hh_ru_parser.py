# import requests
# from lxml import html
# from fake_headers import Headers
#
# header = Headers(headers=True).generate()
# paths = ['//*[@id="compare-gallery-notebook"]/div/div[1]/div/h3/text()',
# '//*[@id="compare-gallery-notebook"]/div/div[12]/div/h3/text()',
# '//*[@id="compare-gallery-notebook"]/div/div[23]/div/h3/text()']
#
# url = 'https://www.apple.com/mac/'
# response = requests.get(url, headers=header)
# parsed = html.fromstring(response.text)
# for i in paths:
#     result = parsed.xpath(i)[0]
#     print(result)

import requests
from bs4 import BeautifulSoup
import lxml
from fake_headers import Headers

header = Headers(headers=True).generate()

url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=python+developer&customDomain=1&page={}'
import pandas as pd
pages = [1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,20]

siteName = 'hh'
save = []
for i in pages:
    try:
        page_url = url.format(i)
        response = requests.get(page_url, headers=header)
        soup = BeautifulSoup(response.text, 'lxml')
        names = [i.text for i in soup.select('span.g-user-content a.bloko-link')][:10]
        salary = [i.text for i in soup.select('div.vacancy-serp-item__sidebar span.bloko-header-section-3.bloko-header-section-3_lite')][:10]
        for index, j in enumerate(names):
            save.append({
                'name': j,
                'salary': salary[index],
                'site': siteName
            })
    except:
        pass

pd.DataFrame(save).to_csv('gb_2_hh.csv')