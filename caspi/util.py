from selenium.webdriver import Chrome, ChromeOptions


class HeadlessChrome(Chrome):
    def __init__(self):
        # chrome options for headless chrome
        options = ChromeOptions()

        # add optional arguments for headless
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')

        # initialize chrome driver
        super(HeadlessChrome, self).__init__(chrome_options=options)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
