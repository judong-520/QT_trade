import time
import random
import datetime

from cg.cg_spot.service import CgCoin


def refresh_quantity(api_key, secret_key, price_low, price_high, symbol='cgt_eth', cg=CgCoin()):
    cg.auth(api_key, secret_key)
    differ = int(price_high * pow(10, 6) - price_low * pow(10, 6))
    for _ in range(differ):
        now = str(datetime.datetime.now()).split('.')[0]
        amount = round(random.uniform(700, 1000), 4)
        price_low = round(price_low + 0.000001, 6)
        print('当前时刻：%s， 挂单价格：%s， 挂单数量：%s' % (now, price_low, amount))
        buy_order = cg.create_order(symbol=symbol, side=1, type=1, price=price_low, amount=amount, source=3)  # 买单
        print(buy_order)
        print()
        time.sleep(2)


if __name__ == '__main__':
    api_key = ''
    secret_key = ''
    refresh_quantity(api_key, secret_key, 0.000558, 0.000568)

