from bs4 import BeautifulSoup as Soup
from caspi.util import HeadlessChrome, escape_unit_suffix

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

import time
from pprint import pprint

SITE_URL = 'http://www.7-eleven.co.kr'

# url for seven select (pb product) list
SEVEN_SELECT = '7select'
SEVEN_ELEVEN_DOSIRAK = 'bestdosirak'

# url for present (event goods) list
EVENT_PRODUCTS = '{0}/product/presentList.asp'.format(SITE_URL)

# side tab flags for event goods page
ONE_PLUS_ONE = 1
TWO_PLUS_ONE = 2


def get_pb_products(kind=""):
    if not kind:
        return get_pb_products(SEVEN_SELECT) + get_pb_products(SEVEN_ELEVEN_DOSIRAK)

    products = []

    with HeadlessChrome() as chrome:
        chrome.get('{0}/product/{1}List.asp'.format(SITE_URL, kind))

        while True:
            time.sleep(5)

            try:
                more_prod_btn = chrome.find_element_by_class_name('btn_more')
                more_prod_btn.click()

            except NoSuchElementException:
                break

        soup = Soup(chrome.page_source, 'html.parser')

        for box in soup.select('li > div.pic_product'):
            product = {
                'name': box.select('div.name')[0].get_text().strip(),
                'price': int(escape_unit_suffix(box.select('div.price')[0].get_text().strip()))
            }

            products.append(product)

    return products


def get_plus_event_products(kind=0):
    if not kind:
        return get_plus_event_products(ONE_PLUS_ONE) + get_plus_event_products(TWO_PLUS_ONE)

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

        for box in soup.select('li > div.pic_product'):
            product = {
                'name': box.select('div.name')[0].get_text().strip(),
                'price': int(escape_unit_suffix(box.select('div.price')[0].get_text().strip())),
                'flag': box.find_previous("ul").select("li")[0].get_text().strip()
            }

            products.append(product)

    return products


def get_stores():
    stores = []

    with HeadlessChrome() as chrome:
        chrome.get(SITE_URL)
        time.sleep(5)

        open_store_list_btn = chrome.find_element_by_class_name('store_open')
        open_store_list_btn.click()
        time.sleep(5)

        city_name_selections = chrome.find_elements_by_css_selector('select#storeLaySido > option')
        city_names = [o.get_attribute('value') for o in city_name_selections][1:]

        for city_name in city_names:
            city_name_selection = Select(chrome.find_element_by_id('storeLaySido'))
            city_name_selection.select_by_value(city_name)
            time.sleep(1)

            chrome.execute_script('$.Fn_store_search(1)')
            time.sleep(5)

            soup = Soup(chrome.page_source, 'html.parser')

            for item in soup.select('div.list_stroe > ul > li'):
                spans = item.select('span')

                store = {
                    'name': spans[0].get_text().strip(),
                    'address': spans[1].get_text().strip(),
                    'tel': spans[2].get_text().strip() or None if len(spans) > 2 else None
                }

                pprint(store)
                stores.append(store)

    return stores
