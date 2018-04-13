from bs4 import BeautifulSoup as Soup
from pprint import pprint

from caspi.util import HeadlessChrome
from selenium.common.exceptions import NoSuchElementException

import re
import time

"""
    module for cu convenience store api
    
    Attribute:
        SITE_URL (str): base url in CU website
        PB_PRODUCT_LIST (str): url to pb products page
        PLUS_EVENT_LIST (str): url to plus event products page
        STORE_LIST (str): url to store lists page
"""

SITE_URL = 'http://cu.bgfretail.com'

PB_PRODUCT_LIST = '{0}/product/pb.do'.format(SITE_URL)
PLUS_EVENT_PRODUCT_LIST = '{0}/evnet/plus.do'.format(SITE_URL)
STORE_LIST = '{0}/store/list.do'.format(SITE_URL)


def get_pb_products():
    """
        get PB products in CU

        Return:
            list: list included PB product dictionary in CU
    """

    products = []

    with HeadlessChrome() as chrome:
        # move into PB products page
        chrome.get(PB_PRODUCT_LIST)

        # click more product button until it's not shown
        while True:
            try:
                # delay prevent latency in requests
                time.sleep(5)

                # find and click button
                prod_list_btn = chrome.find_element_by_class_name('prodListBtn')
                prod_list_btn.click()

            except NoSuchElementException:
                # cannot find button, we'll break
                break

        soup = Soup(chrome.page_source, 'html.parser')

        # get items from list. and parse data
        for item in soup.select('div.prodListWrap > ul > li'):
            product = {
                'name': item.select('p.prodName')[0].get_text().strip(),
                'price': int(re.sub(r'([,원])', '', item.select('p.prodPrice')[0].get_text().strip()))
            }

            products.append(product)

    return products


def get_plus_event_products():
    """
        get plus event (n + n event) products in CU

        Return:
            list: list included plus event product dictionary in CU
    """

    products = []

    with HeadlessChrome() as chrome:
        # move into PB products page
        chrome.get(PLUS_EVENT_PRODUCT_LIST)

        # click more product button until it's not shown
        while True:
            try:
                # delay prevent latency in requests
                time.sleep(5)

                # find and click button
                prod_list_btn = chrome.find_element_by_class_name('prodListBtn')
                prod_list_btn.click()

            except NoSuchElementException:
                # cannot find button, we'll break
                break

        soup = Soup(chrome.page_source, 'html.parser')

        # get items from list. and parse data
        for item in soup.select('div.prodListWrap > ul > li'):
            product = {
                'name': item.select('p.prodName')[0].get_text().strip(),
                'price': int(re.sub(r'([,원])', '', item.select('p.prodPrice')[0].get_text().strip())),
                'flag': item.select('li')[0].get_text().strip(),
            }

            products.append(product)

    return products


def get_stores():
    """
        get stores in CU

        Return:
            list: list included store dictionary in CU
    """
    stores = []

    with HeadlessChrome() as chrome:
        chrome.get(STORE_LIST)
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