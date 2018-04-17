from bs4 import BeautifulSoup as Soup
from caspi.util import HeadlessChrome

import re
import time

from pprint import pprint

"""
    Module for GS25 convenience store API
    
    Attribute:
        SITE_URL (str): base url in CU website
        YOUUS_FRESH_FOOD (str): url to youus fresh foods page
        YOUUS_DIFFERENT_SERVICES (str): url to youus different services page
        STORE_LISTS (str): url to store lists page
"""

SITE_URL = 'http://gs25.gsretail.com/gscvs/ko'

YOUUS_FRESH_FOODS = 'freshfood'
YOOUS_DIFFRENT_SERVICES = 'different-service'

EVENT_GOODS = "{0}/products/event-goods".format(SITE_URL)
ONE_PLUS_ONE = "ONE_TO_ONE"
TWO_PLUS_ONE = "TWO_TO_ONE"

STORE_SERVICE = "{0}/store-services/locations".format(SITE_URL)


def get_youus_products(kind=""):
    if not kind:
        return get_youus_products(YOUUS_FRESH_FOODS) + get_youus_products(YOOUS_DIFFRENT_SERVICES)

    products = []

    with HeadlessChrome() as chrome:
        chrome.get('{0}/products/youus-{1}'.format(SITE_URL, kind))
        page = 1

        while True:
            time.sleep(5)

            soup = Soup(chrome.page_source, 'html.parser')
            boxes = soup.select('div.prod_box')[3:]

            if len(boxes) == 0:
                break

            for box in boxes:
                product = {
                    'name': box.select('p.tit')[0].get_text().strip(),
                    'price': int(re.sub(r'([,원])', '', box.select('span.cost')[0].get_text().strip()))
                }

                products.append(product)

            page += 1
            chrome.execute_script('vagelistCommonFn.movePage({0})'.format(page))

    return products


def get_plus_event_products(kind=""):
    if not kind:
        return get_plus_event_products(ONE_PLUS_ONE) + get_plus_event_products(TWO_PLUS_ONE)

    products = []

    with HeadlessChrome() as chrome:
        chrome.get(EVENT_GOODS)
        time.sleep(5)

        target_tab_item = chrome.find_element_by_id(kind)
        target_tab_item.click()

        page = 1

        while True:
            time.sleep(5)

            soup = Soup(chrome.page_source, 'html.parser')
            boxes = soup.select('div.prod_box')[3:]

            if len(boxes) == 0:
                break

            for box in boxes:
                product = {
                    'name': box.select('p.tit')[0].get_text().strip(),
                    'price': int(re.sub(r'([,원])', '', box.select('span.cost')[0].get_text().strip())),
                    'flag': box.select('p.flg01')[0].get_text().strip()
                }

                products.append(product)

            page += 1
            chrome.execute_script('goodsPageController.movePage({0})'.format(page))

    return products


def get_stores():
    stores = []

    with HeadlessChrome() as chrome:
        chrome.get(STORE_SERVICE)
        page = 1

        while True:
            time.sleep(5)

            soup = Soup(chrome.page_source, 'html.parser')
            rows = soup.select('tbody#storeInfoList > tr')

            if rows[0].get_text().strip() == '조회 조건에 맞는 매장이 없습니다.':
                break

            for row in rows:
                store = {
                    'name': row.select('a.st_name')[0].get_text().strip(),
                    'address': row.select('a.st_address')[0].get_text().strip() or None
                }

                pprint(store)
                stores.append(store)

            page += 1
            chrome.execute_script('boardViewController.getDataList({0})'.format(page))
