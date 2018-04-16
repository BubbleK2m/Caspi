from selenium.webdriver import Chrome, ChromeOptions
import re

"""
    module for 
    utility classes & functions
"""


class HeadlessChrome(Chrome):
    def __init__(self):
        """
            initialize chrome driver instance
            with headless options ('--headless', '--disable-gpu')
        """

        # chrome options for headless chrome
        options = ChromeOptions()

        # add optional arguments for headless
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')

        # initialize chrome driver
        super(HeadlessChrome, self).__init__(chrome_options=options)

    def __enter__(self):
        """
            return self instance
            for with ~ as statement

            Return:
                HeadlessChrome: self instance for with ~ as statement
        """

        # return instance to with statement
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
            close all resource in web driver
            for after with ~ as statement
        """

        # close browser
        self.close()


def escape_unit_suffix(src):
    """
        escape unit suffix like '~원' by regex

        Args:
            src (str) : text would you want to convert

        Return:
            str: text which escaped unit suffix
    """

    return re.sub(r'([,원])', '', src)
