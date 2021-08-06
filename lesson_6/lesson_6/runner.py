from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lesson_6.lesson_6 import settings
from lesson_6.lesson_6.spiders.hh import HhSpider
from lesson_6.lesson_6.spiders.SuperJobSpider import SuperJobSpider
from lesson_6.lesson_6.spiders.leroySpider import LeroyspiderSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)            #

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhSpider)
    process.crawl(SuperJobSpider)
    process.crawl(LeroyspiderSpider, text='обои')

    process.start()