from bs4 import BeautifulSoup as Soup
from caspi.util import HeadlessChrome

import re
import time

SITE_URL = 'http://gs25.gsretail.com/gscvs/ko'

YOUUS_FRESH_FOOD = 'fresh-food'
YOOUS_DIFFRENT_SERVICE = 'diffrent-service'


def get_youus_products(kind=""):
    if not kind:
        return get_youus_products(YOUUS_FRESH_FOOD) + get_youus_products(YOOUS_DIFFRENT_SERVICE)
    
    products = []
    
    with HeadlessChrome as chrome:
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
            chrome.execute('goodsPageController.movePage({0})'.format(page))

    return products


def get_event_products():
    pass