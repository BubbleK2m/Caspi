from caspi.api import cu, gs25
from pprint import pprint

if __name__ == '__main__':
    print('\n - CU PB products - \n')
    pprint(cu.get_pb_products())

    print('\n - CU plus event products - \n')
    pprint(cu.get_plus_event_products())

    print('\n - GS25 youus fresh foods - \n')
    pprint(gs25.get_youus_products(gs25.YOUUS_FRESH_FOOD))

    print('\n - GS25 youus diffrent services - \n')
    pprint(gs25.get_youus_products(gs25.YOOUS_DIFFRENT_SERVICE))
