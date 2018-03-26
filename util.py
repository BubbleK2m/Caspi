from bs4 import BeautifulSoup as Soup
from selenium import webdriver

import time


class Browser:
    def __init__(self, driver=None):
        if driver is None:
            options = webdriver.ChromeOptions()

            # options.add_argument('--headless')
            # options.add_argument('--disable-gpu')

            driver = webdriver.Chrome(chrome_options=options)

        self.driver = driver

    def move(self, path, delay=0):
        self.driver.get(path)
        time.sleep(delay)

    def load(self, delay=0):
        time.sleep(delay)

        soup = Soup(self.driver.page_source, 'html.parser')
        return soup

    def execute(self, script, delay=0):
        self.driver.execute_script(script)
        time.sleep(delay)

    def close(self):
        self.driver.close()
