from bs4 import BeautifulSoup as Soup

from caspi.util import HeadlessChrome, escape_unit_suffix
from selenium.common.exceptions import NoSuchElementException

import time

SITE_URL = 'http://www.7-eleven.co.kr'

# url for seven select (pb product) list
SEVEN_SELECT_PRODUCTS = '{0}/product/7selectList.asp'.format(SITE_URL)
# url for present (event goods) list
EVENT_PRODUCTS = '{0}/product/presentList.asp'.format(SITE_URL)

# side tab flags for event goods page
ONE_PLUS_ONE = 1
TWO_PLUS_ONE = 2


def get_pb_products():
    products = []

    with HeadlessChrome() as chrome:
        chrome.get(SEVEN_SELECT_PRODUCTS)

        while True:
            time.sleep(5)

            try:
                more_prod_btn = chrome.find_element_by_class_name('btn_more')
                more_prod_btn.click()

            except NoSuchElementException:
                break

        soup = Soup(chrome.page_source, 'html.parser')

        for box in soup.select('div.pic_product'):
            product = {
                'name': box.select('div.name')[0].get_text().strip(),
                'price': escape_unit_suffix(box.select('div.price')[0].get_text().strip()) or None
            }

            if product['price']:
                product['price'] = int(product['price'])

            products.append(product)

    return products


def get_event_products(kind):
    products = []

    with HeadlessChrome() as chrome:
        chrome.get(EVENT_PRODUCTS)
        time.sleep(5)

        chrome.execute_script('fncTab({0})'.format(kind))

        while True:
            time.sleep(5)

            try:
                more_prod_btn = chrome.find_element_by_class_name('btn_more')
                more_prod_btn.click()

            except NoSuchElementException:
                break

        soup = Soup(chrome.page_source, 'html.parser')

        for box in soup.select('div.pic_product'):
            product = {
                'name': box.select('div.name')[0].get_text().strip(),
                'price': int(escape_unit_suffix(box.select('div.price')[0].get_text().strip())),
                'flag': box.find_previous("ul").select("li")[0].get_text().strip()
            }

            products.append(product)

    return products
