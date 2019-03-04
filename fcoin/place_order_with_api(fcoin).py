import ccxt
import time
import random
import datetime
from fcoin.service import get_bid_and_ask, place_order

symbol = "NEWOS/ETH"
apiKey = '1ca4c9f5f5bf45b4a984fee9cc392dae'
secret = '2f3abdb44cc341088383d91e08e689ef'
fcoin = ccxt.fcoin({'apiKey': apiKey, 'secret': secret})


if __name__ == '__main__':
    bid, ask = get_bid_and_ask(fcoin)
    price = 0.0000072
    amount = 200
    # order_sell = place_order(2, price, amount, fcoin)  # 挂卖单
    # print('卖单：', order_sell)
    order_buy = place_order(1, price, amount, fcoin)  # 挂买单
    print('买单：', order_buy)
    print()

