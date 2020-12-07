import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import datetime as dt


def get_date_time_from_url(current_url_func):
    current_str = current_url_func.split('-')
    return dt.datetime.strptime(current_str[-2] + current_str[-1][:-1], '%Y%m%d%H%M%S')


def get_title_from_html(current_url_func):
    first = current_url_func.find('span', {'class': 'f-fake-url__t'})
    second = current_url_func.find('span', {'class': 'f-fake-url__u'})
    if first is None:
        first = ''
    else:
        first = str(first).replace('<span class="f-fake-url__t">', '').replace('</span>', '')
    if second is None:
        second = ''
    else:
        second = str(second).replace('<span class="f-fake-url__u">', '').replace('</span>', '')
    return first + second


def get_url_from_html(current_url_func):
    return 'https://www.finam.ru/' + current_url_func['href']


class FinamProcessing:
    def __init__(self, data=None):
        self.data = data
        if self.data is None:
            self.url = 'https://www.finam.ru/analysis/conews/'
        else:
            self.url = 'https://www.finam.ru/analysis/conews/' + self.data + '/'
        self.urls = []
        self.titles = []
        self.dates = []
        self.process()

    def process(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, features="lxml")
        for i in tqdm(soup.find_all('td', {'class': 'ntitle bdotline'})):
            current_html = i.find('a', {'class': 'f-fake-url'})
            current_url = get_url_from_html(current_html)
            current_title = get_title_from_html(current_html)
            current_date = get_date_time_from_url(current_url)
            self.urls.append(current_url)
            self.titles.append(current_title)
            self.dates.append(current_date)
