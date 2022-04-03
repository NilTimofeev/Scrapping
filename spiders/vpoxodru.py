import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from vpoxod.items import VpoxodItem


class VpoxodruSpider(scrapy.Spider):
    name = 'vpoxodru'
    allowed_domains = ['vpoxod.ru']
    start_urls = ['https://www.vpoxod.ru/route']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            next_page = f'https://www.vpoxod.ru{next_page}'
        yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[@class='main_page_hike_title']/a/@href").getall()

        for link in links:
            link = f'https://www.vpoxod.ru{link}'
            yield response.follow(link, callback=self.parse_route)

    def parse_route(self, response: HtmlResponse):
        loader = ItemLoader(item=VpoxodItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "(//span[@class='price-font']/text())[1]") # '59\xa0900\xa0₽'
        loader.add_value('url', response.url)
        loader.add_xpath('photos', "//div[@class='route_about_gallery']/ul/li/a/@href") # '/gallery/photo/35208'
        yield loader.load_item()
