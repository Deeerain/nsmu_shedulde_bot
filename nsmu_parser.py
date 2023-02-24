from datetime import date
import logging

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://ruz.nsmu.ru/"

logger = logging.getLogger(__name__)

soup = BeautifulSoup('', 'lxml')


def request(func: callable) -> requests.Response:
    def wrapper(url: str, **kwargs):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        func(response, soup, **kwargs)
    return wrapper


class Spec(object):

    def __init__(self, title: str, param: str) -> None:
        self.title: str = title
        self.href: str = f'{BASE_URL}{param}'


class Group(Spec):
    pass


class Para:
    def __init__(self, date: date, text: str) -> None:
        self.data = date
        self.text = text

    def __repr__(self) -> str:
        return self.text


def get_specs() -> list[Spec]:
    result: list[Spec] = []
    response = requests.get(BASE_URL)
    soup.markup = BeautifulSoup(response.text, 'lxml')

    for a_el in soup.body.find_all('a'):
        title = a_el.text

        if title == 'СГМУ':
            continue

        result.append(Spec(title, a_el.get('href')))

    return result


def get_groups(link: str) -> list[Group]:
    result: list[Spec] = []
    response = requests.get(link)
    soup.markup = BeautifulSoup(response.text, 'lxml')

    for a_el in soup.body.find_all('a'):
        title = a_el.text

        if title == 'Расписание' or title == 'СГМУ':
            continue

        result.append(Group(title, a_el.get('href')))

    return result


def get_list(c_date: date, link: Group):
    result = []
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')

    columns = soup.find_all('div', {'class': 'row'})

    print(columns)

    for column in columns[-1]:
        print(column)

        d, m, y = column.h3.div.text.split('-')
        l_date = date(int(y), int(m), int(d))

        if l_date != c_date:
            continue

        for para in column.find_all('div'):
            text = para.text
            result.append(Para(l_date, text))

    return result
