# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BooksScraperPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books

    def process_item(self, item, spider):
        if spider.name == 'book24ru':
            item = self.process_price(item)

        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def process_price(self, item):
        # 210 р. Если товара нет в наличие, то цен нет.
        if item['priceold']:
            item['priceold'] = item['priceold'].split()[0]

        if item['price']:
            item['price'] = item['price'].split()[0]

        return item
