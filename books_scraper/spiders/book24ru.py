import scrapy
from scrapy.http import HtmlResponse
from books_scraper.items import BooksScraperItem


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/catalog/fiction-1592/page-1']
    i = 1

    def parse(self, response: HtmlResponse):
        if response.status != 404:
            next_page = f'https://book24.ru/catalog/fiction-1592/page-{self.i}/'
            self.i += 1
            yield response.follow(next_page, callback=self.parse)

            links = response.xpath("//a[@class='product-card__name smartLink']/@href").getall()

            for link in links:
                link = f'https://book24.ru{link}'
                yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        author = response.xpath("(//div[@class='product-characteristic__value'])[1]//text()").get()
        name = response.xpath("(//span[@itemprop='name'])[3]/text()").get()
        priceold = response.xpath("//span[@class='app-price product-sidebar-price__price-old']/text()").get()
        price = response.xpath("//span[@class='app-price product-sidebar-price__price']/text()").get()
        rate = response.xpath("//div[@itemprop='aggregateRating']/meta[1]/@content").get()
        link = response.url
        item = BooksScraperItem(author=author, name=name, priceold=priceold, price=price, rate=rate, link=link)
        yield item
