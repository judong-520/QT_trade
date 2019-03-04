import json
import datetime
import pandas as pd
from bcex.service import Bcex


symbol = 'newos2eth'
api_key = "a10c97e18377e3ae66cd1bc27f32f97536453d6cf4dcd88532a5f8ead5179802"
secret_key = "5bf7-d27aa-9c937-3626-5654"
bcex = Bcex(api_key, secret_key)

pd.set_option('expand_frame_repr', False)

if __name__ == '__main__':
    msg = bcex.trust_list(symbol, 'all')
    msg = json.loads(msg)
    data = msg['data']
    data = pd.DataFrame(data)
    orders = data[data['status'] == '0']
    orders = orders.sort_values(by='price')  # 对卖单按照价格排升序
    print(orders)
    # print()
    id_list = ['261849230', '261845394', '261843456']
    for id in orders['id']:
    # for id in id_list:
        cancel_order = bcex.cancel(symbol, id)
        cancel_order = json.loads(cancel_order)
        print(cancel_order)



