import random
import datetime
from dg.service import Digi

api_key = ''
api_secret = ''
member_id = 171940386
dg = Digi(api_key, api_secret)

if __name__ == '__main__':
    try:
        now = str(datetime.datetime.now()).split('.')[0]
        symbol = 'eth_newos'  # 获取三次dg的数据，防止数据更新没能及时获取
        data = dg.get_ticker()
        bid = float(data['ticker']['buy'])
        ask = float(data['ticker']['sell'])
        print('当前买一价：%s， 卖一价：%s' % (bid, ask))
        for _ in range(500):
            price = round(random.uniform(bid, ask), 8)
            if bid < price < ask:
                break
        if bid < price < ask:
            amount = round(random.uniform(50000, 100000), 8)
            print('现在时刻：%s， 成交价：%s， 成交数量：%s' % (now, price, amount))
            rand = random.choice([0, 1])
            if rand == 0:
                order_sell = dg.send_trade_order('eth_newos', amount, price, 'sell', member_id)  # 下卖单
                print('卖单：', order_sell)
                order_buy = dg.send_trade_order('eth_newos', amount, price, 'buy', member_id)   # 下买单
                print('买单：', order_buy)
            else:
                order_buy = dg.send_trade_order('eth_newos', amount, price, 'buy', member_id)  # 下买单
                print('买单：', order_buy)
                order_sell = dg.send_trade_order('eth_newos', amount, price, 'sell', member_id)  # 下卖单
                print('卖单：', order_sell)
        else:
            print('价差过小')
        print()
    except Exception as error:
        print(error)

