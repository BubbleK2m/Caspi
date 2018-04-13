from caspi import cu, gs25, seven_eleven
from pprint import pprint

if __name__ == '__main__':
    print('\n - CU PB products - \n')
    pprint(cu.get_pb_products())

    print('\n - CU plus event products - \n')
    pprint(cu.get_plus_event_products())

    print('\n - GS25 youus fresh foods - \n')
    pprint(gs25.get_youus_products(gs25.YOUUS_FRESH_FOODS))

    print('\n - GS25 youus diffrent services - \n')
    pprint(gs25.get_youus_products(gs25.YOOUS_DIFFRENT_SERVICES))

    print('\n - GS25 1+1 products - \n')
    pprint(gs25.get_event_products(gs25.ONE_PLUS_ONE))

    print('\n - GS25 2+1 products - \n')
    pprint(gs25.get_event_products(gs25.TWO_PLUS_ONE))

    print('\n - 7 Eleven 7 selects - \n')
    pprint(seven_eleven.get_pb_products())

    print('\n - 7 Eleven 1 + 1 products - \n')
    pprint(seven_eleven.get_event_products(seven_eleven.ONE_PLUS_ONE))

    print('\n - 7 Eleven 2 + 1 products - \n')
    pprint(seven_eleven.get_event_products(seven_eleven.TWO_PLUS_ONE))
