from caspi import cu, gs25, seven_eleven
from pprint import pprint

if __name__ == '__main__':
    print('\n - GS25 youus products - \n')
    pprint(gs25.get_youus_products())

    print('\n - GS25 1+1 products - \n')
    pprint(gs25.get_plus_event_products(gs25.ONE_PLUS_ONE))

    print('\n - GS25 2+1 products - \n')
    pprint(gs25.get_plus_event_products(gs25.TWO_PLUS_ONE))
