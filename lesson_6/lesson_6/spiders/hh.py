import scrapy

from lesson_6.loaders import HHLoader
from lesson_6.lesson_6.xpaths import HH_PAGE_XPATH, HH_VACANCY_XPATH

class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['nn.hh.ru']
    start_urls = ['https://nn.hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    def _get_follow_xpath(self, response, xpath, callback):
        for url in response.xpath(xpath):
            yield response.follow(url, callback=callback)

    def parse(self, response):
        callbacks = {"pagination": self.parse, "vacancy": self.vacancy_parse}

        for key, xpath in HH_PAGE_XPATH.items():
            yield from self._get_follow_xpath(response, xpath, callbacks[key])

    def vacancy_parse(self, response):
        loader = HHLoader(response=response)
        loader.add_value("url", response.url)
        for key, xpath in HH_VACANCY_XPATH.items():
            loader.add_xpath(key, xpath)

        yield loader.load_item()