from bs4 import BeautifulSoup as Soup
from pprint import pprint

from caspi.util import HeadlessChrome
from selenium.common.exceptions import NoSuchElementException

import re
import time

SITE_URL = 'http://cu.bgfretail.com'


def get_pb_products():
    products = []

    with HeadlessChrome() as chrome:
        chrome.get('{0}/product/pb.do'.format(SITE_URL, ))

        while True:
            try:
                time.sleep(5)

                prod_list_btn = chrome.find_element_by_class_name('prodListBtn')
                prod_list_btn.click()

            except NoSuchElementException:
                break

        soup = Soup(chrome.page_source, 'html.parser')

        for item in soup.select('div.prodListWrap > ul > li'):
            product = {
                'name': item.select('p.prodName')[0].get_text().strip(),
                'price': int(re.sub(r'([,원])', '', item.select('p.prodPrice')[0].get_text().strip()))
            }

            products.append(product)

    return products


def get_plus_event_products():
    products = []

    with HeadlessChrome() as chrome:
        chrome.get('{0}/event/plus.do'.format(SITE_URL))

        while True:
            try:
                time.sleep(5)

                prod_list_btn = chrome.find_element_by_class_name('prodListBtn')
                prod_list_btn.click()

            except NoSuchElementException:
                break

        soup = Soup(chrome.page_source, 'html.parser')

        for item in soup.select('div.prodListWrap > ul > li'):
            product = {
                'name': item.select('p.prodName')[0].get_text().strip(),
                'price': int(re.sub(r'([,원])', '', item.select('p.prodPrice')[0].get_text().strip())),
                'flag': item.select('li')[0].get_text().strip(),
            }

            products.append(product)

    return products


def get_stores():
    stores = []

    with HeadlessChrome() as chrome:
        chrome.get('{0}/store/list.do'.format(SITE_URL))
        page = 1

        while True:
            time.sleep(5)

            soup = Soup(chrome.page_source, 'html.parser')
            store_rows = soup.select('div.detail_store tbody tr')

            if len(store_rows) == 0:
                break

            for row in store_rows:
                store = {
                    'name': row.select('span.name')[0].get_text().strip(),
                    'tel': row.select('span.tel')[0].get_text().strip() or None,
                    'address': row.select('div.detail_info > address')[0].get_text().split(', ')[0].strip() or None
                }

                pprint(store)
                stores.append(store)

            page += 1
            chrome.execute_script('newsPage({0})'.format(page))

    return stores
