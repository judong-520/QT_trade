import logging
import sys
import time
from logging.handlers import RotatingFileHandler
from time import sleep
import datetime
import random


from cg.cg_futrues.service import CgCoin
from cg.cg_spot.huobi_exchange import get_market_depth

f_cg = CgCoin()
f_cg.auth('', '')


if __name__ == '__main__':

    order_id = []
    buy_price = []
    buy_amount = []
    sell_price = []
    sell_amount = []

    while True:
        sleep(7)
        try:
            bids_list, asks_list = get_market_depth('btcusdt', 'step1')
            bids_list = bids_list[0:10]
            asks_list = asks_list[0:10]
            '''获取买方市场深度的价格数量'''
            for x in bids_list:
                if x[1] >= 10 and x[1] < 100:
                    x[1] = x[1] / 2000
                elif x[1] >= 100 and x[1] < 1000:
                    x[1] = x[1] / 20000
                elif x[1] >= 1 and x[1] < 10:
                    x[1] = x[1] / 200
                elif x[1] >= 1000 and x[1] < 10000:
                    x[1] = x[1] / 200000
                elif x[1] >= 10000:
                    x[1] = x[1] / 2000000
                if x[1] > 0.15:
                    x[1] = random.uniform(0.05, 0.15)
                buy_order_depth = f_cg.create_order(symbol='xbtc_usdt', side=1, type=1, action=0, price=x[0],
                                                    amount=x[1], source=3)
                print('摆单 buy',buy_order_depth)
                # logger.info('no.1 buy_order_depth {}'.format(buy_order_depth))
                if buy_order_depth['status'] == 200:
                    buy_price.append(x[0])
                    buy_amount.append(x[1])
                    order_id.append(buy_order_depth['data'])
                    sleep(1)

            '''获取卖方市场深度的价格'''
            for y in asks_list:
                if y[1] >= 10 and y[1] < 100:
                    y[1] = y[1] / 2000
                elif y[1] >= 1 and y[1] < 10:
                    y[1] = y[1] / 200
                elif y[1] >= 100 and y[1] < 1000:
                    y[1] = y[1] / 20000
                elif y[1] >= 1000 and y[1] < 10000:
                    y[1] = y[1] / 200000
                elif y[1] >= 10000:
                    y[1] = y[1] / 2000000
                #  y = list(filter(lambda x : x<0.16 ,y))
                if y[1] > 0.15:
                    y[1] = random.uniform(0.05, 0.15)
                sell_order_depth = f_cg.create_order(symbol='xbtc_usdt', side=2, type=1, action=0, price=y[0],
                                                     amount=y[1], source=3)
                print('摆单 sell',sell_order_depth)
                # logger.info('no.1 sell_order_depth {}'.format(sell_order_depth))
                if sell_order_depth['status'] == 200:
                    sell_price.append(y[0])
                    sell_amount.append(y[1])
                    order_id.append(sell_order_depth['data'])
                    sleep(1)

            '''挂卖单，卖单价格数量等于买一的价格数量'''
            if buy_amount != []:

                sell_order = f_cg.create_order(symbol='xbtc_usdt', side=2, type=1, action=1, price=buy_price[0],
                                               amount=buy_amount[0], source=3)
                if sell_order['status'] == 200:
                    order_id.append(sell_order['data'])

            '''挂买单，买单价格数量等于卖一的价格数量'''
            if sell_amount != []:
                buy_order = f_cg.create_order(symbol='xbtc_usdt', side=1, type=1, action=1, price=sell_price[0],
                                              amount=sell_amount[0], source=3)
                if buy_order['status'] == 200:
                    order_id.append(buy_order['data'])

            if order_id != []:
                for i in order_id:
                    sleep(1)
                    f_cg.cancel(i)

            order_id.clear()
            buy_price.clear()
            buy_amount.clear()
            sell_price.clear()
            sell_amount.clear()

        except Exception as e:
            # logger.error('btc_usdt_program_1 is exception {}'.format(e))
            continue
