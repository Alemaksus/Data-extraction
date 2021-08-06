# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import TakeFirst, MapCompose, Compose

class Lesson6Item(scrapy.Item):
    name = scrapy.Field()
    pass

class SuperJobSpiderItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    location = scrapy.Field()
    link = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    company = scrapy.Field()
    currency = scrapy.Field()
    site = scrapy.Field()

# Leroy:

def get_id(values):
    pattern = re.compile('(\d+)\/')
    values = int(re.findall(pattern, values)[0])
    return values


def get_link(values):
    pattern = re.compile('<\d+ (.+)>')
    values = re.findall(pattern, values)
    return values


def edit_definitions(values):
    pattern = re.compile('\\n +')
    values = re.sub(pattern, '', values)
    try:
        return float(values)
    except ValueError:
        return values


def change_price(values):
    values = float(values)
    return values

class LeroySpyderItem(scrapy.Item):
    _id = scrapy.Field(input_processor=MapCompose(get_id))
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose())
    terms = scrapy.Field(input_processor=MapCompose())
    definitions = scrapy.Field(input_processor=MapCompose(edit_definitions))
    price = scrapy.Field(input_processor=MapCompose(change_price))
    characteristic = scrapy.Field()
    link = scrapy.Field(output_processor=MapCompose(get_link))