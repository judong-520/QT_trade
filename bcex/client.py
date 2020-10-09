import json
import random
import time
import datetime
from bcex.service import Bcex


symbol = 'newos2eth'
api_key = ""
secret_key = ""

bcex = Bcex(api_key, secret_key)


def get_depth(symbol='newos2eth'):
    depth = bcex.depth(symbol)
    depth = json.loads(depth)
    bids = depth['data']['bids']
    bid = bids[0]
    asks = depth['data']['asks']
    ask = asks[-1]
    return bid, ask


if __name__ == '__main__':
    try:
        bid, ask = get_depth()
        now = str(datetime.datetime.now()).split('.')[0]
        print('当前时刻：%s， 买一价：%s， 卖一价：%s' % (now, bid[0], ask[0]))
        for _ in range(500):
            price = round(random.uniform(float(bid[0]), float(ask[0])), 8)
            if float(bid[0]) < price < float(ask[0]):
                break
        if float(bid[0]) < price < float(ask[0]):
            amount = round(random.uniform(100, 300), 2)
            print('成交价格：%s， 数量：%s' % (price, amount))
            rand = random.choice([0, 1])
            if rand == 0:
                order_sell = bcex.coin_trust(symbol, 'sale', price, amount)  # 挂卖单
                order_sell = json.loads(order_sell)
                print('卖单：', order_sell)
                order_buy = bcex.coin_trust(symbol, 'buy', price, amount)  # 挂买单
                order_buy = json.loads(order_buy)
                print('买单：', order_buy)
            else:
                order_buy = bcex.coin_trust(symbol, 'buy', price, amount)  # 挂买单
                order_buy = json.loads(order_buy)
                print('买单：', order_buy)
                order_sell = bcex.coin_trust(symbol, 'sale', price, amount)  # 挂卖单
                order_sell = json.loads(order_sell)
                print('卖单：', order_sell)
        else:
            print('价差过小')
        print()
    except Exception as error:
        print(error)
