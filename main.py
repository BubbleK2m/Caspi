from model import CU, GS25, SevenEleven
from pprint import pprint
from util import Browser
from datetime import datetime

if __name__ == '__main__':
    start = datetime.now()

    browser = Browser()
    cu = CU()

    # print('\n- CU pb products -\n')
    # pprint(cu.get_products(browser, 'pb'))

    # print('\n- CU best products -\n')
    # pprint(cu.get_products(browser, 'best'))

    # print('\n - CU stores -\n')
    # pprint(cu.get_stores(browser))

    gs25 = GS25()

    # print('\n- GS25 youus fresh foods -\n')
    # pprint(gs25.get_products(browser, 'youus-freshfood'))

    # print('\n- GS25 youus different services -\n')
    # pprint(gs25.get_products(browser, 'youus-different-service'))

    print('\n- GS25 1+1 products')
    pprint(gs25.get_event_products(browser, 'ONE_TO_ONE'))

    # print('\n- GS25 stores -\n')
    # pprint(gs25.get_stores(browser))

    seven_eleven = SevenEleven()

    # print('\n- 7Eleven dosiraks -\n')
    # pprint(seven_eleven.get_products(browser, 'bestdosirak'))

    # print('\n- 7Eleven 7 selects -\n')
    # pprint(seven_eleven.get_products(browser, '7select'))

    browser.close()
    finish = datetime.now()

    print('total times: {0}'.format(str(finish - start)))
