from bs4 import BeautifulSoup as Soup
from selenium.common.exceptions import NoSuchElementException

import re
import time


class Brand:
    def __init__(self, name, url):
        self.name = name
        self.url = url


class CU(Brand):
    def __init__(self):
        super(CU, self).__init__('CU', 'http://cu.bgfretail.com')

    def get_products(self, browser, kind):
        browser.move('{0}/product/{1}.do'.format(self.url, kind), 3)
        products = list()

        while True:
            try:
                prod_list_btn = browser.find_element_by_class_name('prodListBtn')

                if prod_list_btn is not None:
                    browser.execute('nextPage(1)', 3)

            except NoSuchElementException:
                break

        soup = browser.load()

        for item in soup.select('div.prodListWrap > ul > li'):
            name = item.select('p.prodName')[0].get_text().strip()
            name = name if name != '' else None

            price = re.sub(r'([,원])', '', item.select('p.prodPrice')[0].get_text().strip())
            price = int(price) if price != '' else None

            product = Product(name, price)
            products.append(product.__dict__)

        return products

    def get_stores(self, browser):
        browser.move('{0}/store/list.do'.format(self.url), 3)

        stores = list()
        page = 1

        while True:
            soup = browser.load()
            store_rows = soup.select('div.detail_store tbody tr')

            if len(store_rows) == 0:
                break

            for row in store_rows:
                name = row.select('span.name')[0].get_text().strip()
                name = name if name != '' else None

                tel = row.select('span.tel')[0].get_text().strip()
                tel = tel if tel != '' else None

                address = row.select('div.detail_info > address')[0].get_text().split(', ')[0].strip()
                address = address if address != '' else None

                store = CStore(name, tel, address)
                print(store.__dict__)

                stores.append(store.__dict__)

            page += 1
            browser.execute('newsPage({0})'.format(page), 3)

        return stores


class SevenEleven(Brand):
    def __init__(self):
        super(SevenEleven, self).__init__('7 Eleven', 'http://www.7-eleven.co.kr')

    def get_products(self, browser, kind):
        browser.move('{0}/product/{1}List.asp'.format(self.url, kind), 5)
        products = list()

        while True:
            try:
                more_prod_btn = browser.driver.find_element_by_class_name('btn_more')

                if more_prod_btn is not None:
                    browser.execute("fncMore('')", 5)

            except NoSuchElementException:
                break

        soup = browser.load()

        for box in soup.select('div.pic_product'):
            name = box.select('div.infowrap > div.name')[0].get_text()
            price = int(re.sub(r',', '', box.select('div.infowrap > div.price')[0].get_text()))

            product = Product(name, price)
            products.append(product.__dict__)

        return products


class GS25(Brand):
    def __init__(self):
        super(GS25, self).__init__('GS25', 'http://gs25.gsretail.com/gscvs/ko')

    def get_products(self, browser, kind):
        browser.move('{0}/products/{1}'.format(self.url, kind), 3)

        products = list()
        page = 1

        while True:
            soup = browser.load()
            boxes = soup.select('div.prod_box')

            if len(boxes) == 0:
                break

            for box in boxes:
                name = box.select('p.tit')[0].get_text().strip()
                name = name if name != '' else None

                price = re.sub(r'([,원])', '', box.select('span.cost')[0].get_text().strip())
                price = int(price) if price != '' else None

                product = Product(name, price)
                products.append(product.__dict__)

            page += 1
            browser.execute('vagelistCommonFn.movePage({0})'.format(page), 3)

        return products

    def get_stores(self, browser):
        browser.move('{0}/store-services/locations'.format(self.url), 3)

        stores = list()
        page = 1

        while True:
            soup = browser.load()
            rows = soup.select('tbody#storeInfoList tr')

            if rows[0].get_text('') == '조회 조건에 맞는 매장이 없습니다.':
                break

            for row in rows:
                name = row.select('a.st_name')[0].get_text().strip()
                name = name if name != '' else None

                address = re.split(r"[,(]", row.select('a.st_address')[0].get_text().strip())[0]
                address = address if address != '' else None

                store = CStore(name, None, address)
                print(store.__dict__)

                stores.append(store.__dict__)

            page += 1
            browser.execute('boardViewController.getDataList({0})'.format(page), 3)

        return stores


class CStore:
    def __init__(self, name, tel, address):
        self.name = name
        self.tel = tel
        self.address = address


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
