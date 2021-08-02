import scrapy
import re
import os
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class Lesson6Pipeline:
    def process_item(self, item, spider):
        return item

class SuperJobSpiderPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy
        # self.mongo_base = client.vacancy_hh_scrapy

    def process_item(self, item, spider):
        collection = self.mongo_base['vacancy']

        if spider.name == 'hhru':
            salary_list = []
            for _ in item['salary']:
                s = _.replace(" ", "").replace("\xa0", "")
                salary_list.append(s)
            item['salary'] = salary_list
            if item['salary'][0] == 'от':
                item['salary_min'] = int(item['salary'][1])
                if item['salary'][2] == 'до':
                    item['salary_max'] = int(item['salary'][3])
                    item['currency'] = item['salary'][5]
                else:
                    item['salary_max'] = 'NA'
                    item['currency'] = item['salary'][3]
            elif item['salary'][0] == 'до':
                item['salary_min'] = 'NA'
                item['salary_max'] = int(item['salary'][1])
                item['currency'] = item['salary'][3]
            elif item['salary'][0] == 'з/пнеуказана':
                item['salary_min'] = 'NA'
                item['salary_max'] = 'NA'
            else:
                item['salary_min'] = 'wrong'
                item['salary_max'] = 'wrong'
            del item['salary']

            item['location'] = ' '.join(item['location']).replace("  ", " ").replace(" ,", ",")
            item['company'] = ' '.join(item['company']).replace("\xa0", "").replace("  ", " ").strip()
            item['site'] = 'https://hh.ru'
            item['link'] = item['link'][:item['link'].find('?')]

        if spider.name == 'sjru':
            salary_list = []
            for _ in item['salary']:
                s = _.replace(" ", "").replace("\xa0", "")
                salary_list.append(s)
            item['salary'] = salary_list

            if item['salary'][0] == 'Подоговорённости':
                item['salary_min'] = 'NA'
                item['salary_max'] = 'NA'

            elif item['salary'][2] == '—':
                item['salary_min'] = int(item['salary'][0])
                item['salary_max'] = int(item['salary'][4])
                item['currency'] = item['salary'][6]

            elif item['salary'][0] == 'от':
                pos = item['salary'][2].find('руб.')
                item['salary_min'] = item['salary'][2][:pos]
                item['currency'] = item['salary'][2][pos:]

            elif item['salary'][0] == 'до':
                pos = item['salary'][2].find('руб.')
                item['salary_max'] = item['salary'][2][:pos]
                item['currency'] = item['salary'][2][pos:]

            elif item['salary'][2] == 'руб.':
                item['salary_min'] = item['salary'][0]
                item['salary_max'] = item['salary'][0]
                item['currency'] = item['salary'][2]
            else:
                item['salary_min'] = 'wrong'
                item['salary_max'] = 'wrong'
            del item['salary']

            item['location'] = ' '.join(item['location']).replace("  ", " ")\
                .replace(" ,", ",").replace(" Показать на карте", "")
            item['site'] = 'https://superjob.ru'

        collection.insert_one(item)  # Добавляем в базу данных
        return item

class LeroyparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy_products

    def process_item(self, item, spider):

        item['_id'] = item['_id'][0]
        item['link'] = item['link'][0]
        item['price'] = item['price'][0]
        item['characteristic'] = {
            item['terms'][i]: item['definitions'][i] for i in range(len(item['terms']))
        }

        del item['terms'], item['definitions']
        collection = self.mongo_base[spider.name]
        collection.update_one({'link': item['link']}, {'$set': item}, upsert=True)

        return item


class LeroyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                yield scrapy.Request(img)

    def file_path(self, request, response=None, info=None):
        pattern = re.compile('\/(\d+)')
        name = re.findall(pattern, request.url)[0]
        path = f'{os.getcwd()}\\images\\{name}\\'
        if os.path.exists(path) == False:
            os.mkdir(path)
        tail = os.path.basename(request.url)
        result = f'{path}{tail}'
        return result

    def item_completed(self, results, item, info):
        if results[0]:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item