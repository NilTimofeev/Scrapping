from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from pymongo import MongoClient
from selenium.webdriver.common.action_chains import ActionChains
import datetime

chrome_options = Options()
chrome_options.add_argument("--start-maximized")


class MailRuScrapper:

    months = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
              'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'}

    def __init__(self):

        self.driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.username = input('Введите логин: ')
        self.pass_ = input('Введите пароль: ')
        self.letters_links = set()
        self.url = 'https://e.mail.ru/inbox/'
        self.client = MongoClient('localhost', 27017)
        self.actions = ActionChains(self.driver)

    def make_letters_links(self):

        start_len = True
        end_len = False

        while start_len != end_len:

            time.sleep(0.5)
            links = []
            start_len = len(self.letters_links)

            letters_list = self.driver.find_elements(By.XPATH, "//a[@data-id]")

            for i in range(len(letters_list)):
                links.append(letters_list[i].get_attribute('data-id'))

            self.letters_links.update(links)

            self.driver.execute_script("arguments[0].scrollIntoView();", letters_list[-1])
            end_len = len(self.letters_links)

    def make_doc(self, link):

        self.driver.get(f'{self.url}{link}')
        theme = self.driver.find_elements(By.CLASS_NAME, 'thread-subject')[0].text
        address = self.driver.find_elements(By.CLASS_NAME, 'letter-contact')[0].get_attribute('title')
        date = self.driver.find_elements(By.CLASS_NAME, 'letter__date')[0].text.split()
        d = datetime.datetime.now()
        # Сегодня, 15:41  |  Вчера, 22:04  |  21 марта, 14:14  |  25 января 2021, 16:51
        if date[0] == 'Сегодня,':
            date = f'{d.strftime("%d-%m-%Y")} {date[1]}'
        elif date[0] == 'Вчера,':
            date = f'{(d - datetime.timedelta(days=1)).strftime("%d-%m-%Y")} {date[1]}'
        elif len(date) == 3:
            date = f'{date[0]}-{self.months[date[1][:-1]]}-{d.year} {date[2]}'
        else:
            date = f'{date[0]}-{self.months[date[1]]}-{date[2][:-1]} {date[3]}'
        text = self.driver.find_element(By.XPATH, "//div[@class='letter__body']").text

        doc = {'address': address, 'date': date, 'theme': theme, 'text': text}

        return doc

    def run_scrapper(self):

        # authorization
        self.driver.implicitly_wait(10)
        self.driver.get('https://account.mail.ru/login/')
        username_input = self.driver.find_element(By.XPATH, "//input[@name='username']")
        username_input.send_keys(self.username)
        self.driver.find_element(By.XPATH, "//button[@data-test-id='next-button']").click()
        pass_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']")))
        pass_input.send_keys(self.pass_)
        self.driver.find_element(By.XPATH, "//button[@data-test-id='submit-button']").click()

        db_mail_ru = self.client['mail_ru']
        letters = db_mail_ru.letters

        self.make_letters_links()

        for link in self.letters_links:

            doc = self.make_doc(link)
            letters.insert_one(doc)

        self.driver.quit()


scrapper = MailRuScrapper()
scrapper.run_scrapper()
