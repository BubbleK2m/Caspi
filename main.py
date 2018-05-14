from caspi import cu, gs25, seven_eleven
from datetime import datetime as Datetime

import requests
import json

if __name__ == '__main__':
    stores = []

    stores.extend(cu.get_stores('대전광역시'))
    stores.extend(gs25.get_stores(30))
    stores.extend(seven_eleven.get_stores('대전'))

    print(len(stores))
    print(json.dumps(stores, ensure_ascii=False, indent=2))
