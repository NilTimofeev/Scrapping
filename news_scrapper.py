import requests
from lxml import html
import datetime
from pymongo import MongoClient

header = {
    'User-Agent': 'Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 81.0.4044.92 Safari / 537.36'}
months = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
          'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'}
news_list = []


def get_dom(url):
    response = requests.get(url, headers=header)
    dom = html.fromstring(response.text)

    return dom


def get_news():
    dom = get_dom('https://yandex.ru/news/')
    items = dom.xpath(
        "//div[@class='mg-grid__col mg-grid__col_xs_6'] | //div[@class='mg-grid__col mg-grid__col_xs_4']")

    for item in items:

        date = item.xpath(
                ".//div/div[contains (@class,'mg-card-footer')]/div/div/span[@class='mg-card-source__time']/text()")[0]
        d = datetime.datetime.now()

        if len(date) == 5:  # '18:43'
            date = f'{date}-{d.strftime("%d-%m-%Y")}'
        elif date.split()[0] == 'вчера':  # вчера в 15:38
            date = f"{date.split()[2]}-{(d - datetime.timedelta(days=1)).strftime('%d-%m-%Y')}"
        else:  # 28 февраля в 23:44
            date_list = date.split()
            date_list[1] = months[date_list[1]]
            date = '-'.join([date_list[-1], date_list[0], date_list[1], d.year])

        news = {}
        news['source'] = item.xpath(".//div/div[contains (@class,'mg-card-footer')]/div/div/span[@class='mg-card-source__source']/a/text() | \
                //div[@class='mg-card__inner']/div[contains (@class, 'mg-card-footer')]/div/div/span[@class='mg-card-source__source']/a/text()")[0]

        news['text'] = item.xpath(".//div[@class='mg-card__text-content']/div/h2/a/text() | \
                                        //div[@class='mg-card__inner']/h2/a/text()")[0].replace('\xa0', ' ')
        news['link'] = item.xpath(".//div[@class='mg-card__text-content']/div/h2/a/@href | \
                                        //div[@class='mg-card__inner']/h2/a/@href")[0]
        news['date'] = date

        news_list.append(news)

    dom = get_dom('https://lenta.ru/')
    items = dom.xpath("//div[@class='topnews__column']/a | //div[@class='topnews__column']/div/a")

    for item in items:

        date = item.xpath(".//div/div/time/text() | .//div[@class='card-big__info']/time/text()")[0]

        if len(date) == 5:  # '18:43'
            date = f'{date}-{datetime.date.today().strftime("%d-%m-%Y")}'

        else:  # # 14:42, 28 февраля 2022
            date_list = date.split()
            date_list[2] = months[date_list[2]]
            date_list[0][5].replace(',', '-')
            date = '-'.join(date_list)

        news = {}
        news['source'] = 'Lenta.ru'
        news['text'] = item.xpath(".//div/span/text() | .//div[@class='card-big__titles']/h3/text()")[0]
        news['date'] = date
        news['link'] = f'https://lenta.ru/{item.xpath(".//@href")[0]}'

        news_list.append(news)


def set_data_into_db():
    client = MongoClient('localhost', 27017)
    db_news_list = client['db_news_list']
    news = db_news_list.news

    news.insert_many(news_list)


get_news()
set_data_into_db()
