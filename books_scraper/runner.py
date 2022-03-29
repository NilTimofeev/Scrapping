from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from books_scraper import settings
from books_scraper.spiders.labirintru import LabirintruSpider
from books_scraper.spiders.book24ru import Book24ruSpider

if __name__ == '__main__':
    crawler_setting = Settings()
    crawler_setting.setmodule(settings)

    process = CrawlerProcess(settings=crawler_setting)

    process.crawl(Book24ruSpider)
    #process.crawl(LabirintruSpider)

    process.start()

