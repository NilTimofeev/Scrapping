# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksScraperItem(scrapy.Item):

    author = scrapy.Field()
    name = scrapy.Field()
    priceold = scrapy.Field()
    price = scrapy.Field()
    rate = scrapy.Field()
    link = scrapy.Field()
    _id = scrapy.Field()
