import ccxt
import random
import datetime
from fcoin.service import get_bid_and_ask, place_order

symbol = "NEWOS/ETH"
apiKey = '1ca4c9f5f5bf45b4a984fee9cc392dae'
secret = '2f3abdb44cc341088383d91e08e689ef'
fcoin = ccxt.fcoin({'apiKey': apiKey, 'secret': secret})


if __name__ == '__main__':
    try:
        bid, ask = get_bid_and_ask(fcoin)
        now = str(datetime.datetime.now()).split('.')[0]
        print('当前时刻：%s， 买一价：%s， 卖一价：%s' % (now, str(bid), str(ask)))
        for _ in range(500):
            price = round(random.uniform(float(bid), float(ask)), 8)
            if float(bid) < price < float(ask):
                break
        if float(bid) < price < float(ask):
            amount = round(random.uniform(100, 150), 2)
            print('成交价：%s, 成交数量：%s' % (price, amount))
            rand = random.choice([0, 1])
            if rand == 0:
                order_buy = place_order(1, price, amount, fcoin)  # 挂买单
                print('买单：', order_buy)
                order_sell = place_order(2, price, amount, fcoin)  # 可能会报价格不在最新成交价上下浮动10%的价差错误
                print('卖单：',order_sell)
            else:
                order_sell = place_order(2, price, amount, fcoin)  # 可能会报价格不在最新成交价上下浮动10%的价差错误
                print('卖单：',order_sell)
                order_buy = place_order(1, price, amount, fcoin)  # 挂买单
                print('买单：', order_buy)
        else:
            print('价差过小')
        print()
    except Exception as error:
        print(error)
        print()
