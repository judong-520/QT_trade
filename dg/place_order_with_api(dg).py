import random
import datetime
from dg.service import Digi

api_key = '5af415c00a1e5'
api_secret = '6a29ac697137bc0e66d613ec110b105805af415c5'
member_id = 171940386
dg = Digi(api_key, api_secret)

if __name__ == '__main__':
    try:
        now = str(datetime.datetime.now()).split('.')[0]
        price = float(0.00000830)
        amount = float(1800)
        print('现在时刻：%s， 成交价：%s， 成交数量：%s' % (now, price, amount))

        # order_buy = dg.send_trade_order('eth_newos', amount, price, 'buy', member_id)  # 下买单
        # print('买单：', order_buy)
        order_sell = dg.send_trade_order('eth_newos', amount, price, 'sell', member_id)  # 下卖单
        print('卖单：', order_sell)

        print()
    except Exception as error:
        print(error)


