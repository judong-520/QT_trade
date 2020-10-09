import json
from bcex.service import Bcex


symbol = 'newos2eth'
api_key = ""
secret_key = ""
bcex = Bcex(api_key, secret_key)


if __name__ == '__main__':
    price = 0.00000890
    amount = 300

    # order_sell = bcex.coin_trust(symbol, 'sale', price, amount)  # 挂卖单
    # order_sell = json.loads(order_sell)
    # print(order_sell)
    order_buy = bcex.coin_trust(symbol, 'buy', price, amount)  # 挂买单
    order_buy = json.loads(order_buy)
    print(order_buy)
