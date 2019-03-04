import time
import json
import random
import datetime
from websocket import create_connection

from cg.cg_spot.service import CgCoin


def get_bid_and_ask_from_cg(symbol='cgt_eth', url='wss://i.cg.net/wi/ws'):
    """
    :param symbol: 交易对
    :param url: 网址
    :return: 返回买一、卖一价
    """
    while True:  # 一直链接，直到连接上就退出循环
        try:
            ws = create_connection(url)
            break
        except Exception as e:
            print('连接异常：', e)
            time.sleep(2)
            continue
    while True:  # 连接上，退出第一个循环之后，此循环用于一直获取数据
        sign = '%s.deep' % symbol
        msg = '{"event":"subscribe", "channel":"%s"}' % sign
        ws.send(msg)
        response = str(ws.recv())
        response = json.loads(response)
        if response['type'] == sign:
            bid = response['data']['bids'][0]
            ask = response['data']['asks'][0]
            return bid, ask


def refresh_quantity(api_key, secret_key, symbol='cgt_eth', cg=CgCoin()):
    cg.auth(api_key, secret_key)
    now = str(datetime.datetime.now()).split('.')[0]
    bid, ask = get_bid_and_ask_from_cg()
    print('当前时刻：%s， 买一价：%s， 卖一价：%s' % (now, bid, ask))
    for _ in range(200):
        price = round(random.uniform(float(bid), float(ask)), 6)
        if float(bid) < price < float(ask):
            break
    if float(bid) < price < float(ask):
        amount = round(random.uniform(200000, 260000), 4)
        print('成交价：%s， 成交量：%s' % (price, amount))
        sell_order = cg.create_order(symbol=symbol, side=2, type=1, price=price, amount=amount, source=3)  # 卖单
        print('卖单:', sell_order)
        if sell_order['status'] == 200:
            order_id = sell_order['data']
            buy_order = cg.create_order(symbol=symbol, side=1, type=1, price=price, amount=amount, source=3)  # 买单
            print('买单:', buy_order)
            if buy_order['status'] != 200:
                for _ in range(3):
                    cancel_order = cg.cancel(order_id)
                    print('撤单:', cancel_order)
                    if cancel_order['status'] == 200:
                        break
    else:
        print('价差过小')
    print()


if __name__ == '__main__':
    api_key = 'UQKf7SoPPCEY'
    api_secret = 'tBLWXqyHeb6q'
    while True:
        refresh_quantity(api_key, api_secret)
        time.sleep(20)

