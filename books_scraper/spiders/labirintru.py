import scrapy
from scrapy.http import HtmlResponse
from books_scraper.items import BooksScraperItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/genres/1852/?page=1']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            next_page = f'https://www.labirint.ru/genres/1852/{next_page}'
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='product-title-link']/@href").getall()

        for link in links:
            link = f'https://www.labirint.ru{link}'
            yield response.follow(link, callback=self. book_parse)

    def book_parse(self, response: HtmlResponse):
        author = response.xpath("//a[@data-event-label='author']/text()").get()
        name = response.xpath("//div[@id='product-about']/h2/text()").get()[18:]
        priceold = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        if priceold:
            price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        else:
            price = response.xpath("//span[@class='buying-price-val-number']/text()").get()
        rate = response.xpath("//div[@id='rate']/text()").get()
        link = response.url
        item = BooksScraperItem(author=author, name=name, priceold=priceold, price=price, rate=rate, link=link)
        yield item
