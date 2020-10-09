# -*- coding:utf-8 -*-
import time
import json
import random
import datetime
from websocket import create_connection

from cg.cg_spot.service import CgCoin


def get_data_from_cg(symbol, url='wss://i.cg.net/wi/ws'):
    data = {}
    for _ in range(10):  # 链接，连接上就退出循环
        try:
            ws = create_connection(url)
            break
        except Exception as e:
            print('连接异常：', e)
            time.sleep(2)
            continue
    for _ in range(10):  # 连接上，退出第一个循环之后，此循环用于获取数据
        sign = '%s.deep' % symbol
        msg = '{"event":"subscribe", "channel":"%s"}' % sign
        ws.send(msg)
        response = str(ws.recv())
        response = json.loads(response)
        if response['type'] == sign:
            bids = response['data']['bids']
            bids_num = int(len(bids) / 2)
            data['bids'] = bids_num, bids[0]

            asks = response['data']['asks']
            asks_num = int(len(asks) / 2)
            data['asks'] = asks_num, asks[0]

            return data


def fill_depth(floor, upper, symbol, api_key, secret_key, digit=4, number=20, exchange=CgCoin()):
    """
    :param floor: 挂单数量下限
    :param upper: 挂单数量上限
    :param symbol: 交易对
    :param api_key:
    :param secret_key:
    :param number: 用于补单的触发条件
    :param exchange: 交易所
    :return:
    """
    exchange.auth(api_key, secret_key)
    now = str(datetime.datetime.now()).split('.')[0]
    data = get_data_from_cg(symbol)
    bids = data['bids']
    asks = data['asks']
    print('当前时间:%s，交易对:%s，买单深度:%s档，卖单深度:%s档' % (now, symbol, bids[0], asks[0]))
    if bids[0] <= number:
        for _ in range(10):
            rand = round(random.uniform(0.98, 0.999), 4)
            price = round(bids[1] * rand, digit)
            amount = round(random.uniform(floor, upper), 6)
            order_buy = exchange.create_order(symbol=symbol, side=1, type=1, price=price, amount=amount, source=3)
            print('挂单价格:%s，挂单数量:%s, 买单：%s' % (price, amount, order_buy))
    if asks[0] <= number:
        for _ in range(10):
            rand = round(random.uniform(1.001, 1.02), 4)
            price = round(asks[1] * rand, digit)
            amount = round(random.uniform(floor, upper), 6)
            order_sell = exchange.create_order(symbol=symbol, side=2, type=1, price=price, amount=amount, source=3)
            print('挂单价格:%s，挂单数量:%s, 卖单：%s' % (price, amount, order_sell))
    print()
    time.sleep(0.5)


if __name__ == '__main__':
    fill_depth(0.1, 0.3, 'xeth_usdt', '', '', digit=2)
    fill_depth(0.03, 0.08, 'xbtc_usdt', '', '', digit=2)
    fill_depth(3, 10, 'xeos_usdt', '', '', digit=4)
    fill_depth(6, 10, 'xxrp_usdt', '', '', digit=4)
    # https: // demo.i.cg.net
    fill_depth(0.1, 0.3, 'xeth_usdt', '', '', digit=2, exchange=CgCoin(base_url='https://demo.i.cg.net'))
    fill_depth(0.03, 0.08, 'xbtc_usdt', '', '', digit=2, exchange=CgCoin(base_url='https://demo.i.cg.net'))
    fill_depth(0.12, 0.15, 'eth_usdt', '', '')
    # fill_depth(1, 3, 'cgt_eth', '', '', digit=6)
    fill_depth(5, 20, 'xrp_usdt', '', '')

    fill_depth(0.002, 0.003, 'btc_usdt', '', '')

    fill_depth(0.002, 0.003, 'eth_btc', '', '', digit=8)

    fill_depth(0.35, 0.45, 'ltc_usdt', '', '')

    fill_depth(100, 200, 'newos_eth', '', '', digit=8)
    fill_depth(200, 250, 'zil_usdt', '', '', digit=8)
    fill_depth(1200, 1500, 'dta_usdt', '', '', digit=8)
    fill_depth(400, 600, 'ocn_usdt', '', '', digit=8)
    fill_depth(20, 30, 'gnt_usdt', '', '')
    fill_depth(2, 3, 'eos_usdt', '', '')
    fill_depth(4, 5, 'ae_eth', '', '', digit=8)
    fill_depth(15, 20, 'bat_eth', '', '', digit=8)
    fill_depth(280, 350, 'iost_usdt', '', '', digit=8)

    fill_depth(1500, 1800, 'newos_usdt', '', '', digit=6)


