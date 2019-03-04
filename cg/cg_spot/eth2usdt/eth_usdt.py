import time
import random
from threading import Thread
from cg.cg_spot.eth2usdt.service import CgCoin
from cg.cg_spot.eth2usdt.setting import *

cg = CgCoin()
cg.auth(api_key, secret_key)


def place_orders(side, buffer_list):
    for factor in buffer_list:
        price = round(factor[0] + random.uniform(price_low, price_up), 8)
        amount = round(random.uniform(gross_low, gross_up) / price, amount_digit)
        if side == 1:
            buy_order_depth = cg.create_order(symbol=symbol_cg, side=1, price=price, amount=amount, sorce=3)
            if buy_order_depth['status'] == 200:
                buy_id_list.append(buy_order_depth['data'])
                buy_prices.append(price)
                buy_amounts.append(amount)
        elif side == 2:
            sell_order_depth = cg.create_order(symbol=symbol_cg, side=2, price=price, amount=amount, sorce=3)
            if sell_order_depth['status'] == 200:
                sell_id_list.append(sell_order_depth['data'])
                sell_prices.append(price)
                sell_amounts.append(amount)
        time.sleep(0.5)


def repeal_orders(buffer_list):
    for order_id in buffer_list:
        print(order_id)
        for _ in range(3):
            cancel_order = cg.cancel(order_id)
            if cancel_order['status'] == 200:
                break
        time.sleep(0.8)


def main():
    start = time.time()
    try:
        bids_list, asks_list = CgCoin.get_depth_from_huobi(symbol_huobi)
        if not bids_list and not bids_list:
            try:
                bids_list, asks_list = CgCoin.get_depth_from_bcex(symbol_bcex)
            except Exception as symbol_error:
                CgCoin.exception_record('./bcex_symbol.txt', str(symbol_error))

        # 挂深度
        t1 = Thread(target=place_orders, args=(1, bids_list))  # 挂买单深度
        t2 = Thread(target=place_orders, args=(2, asks_list))  # 挂卖单深度
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # 挂单成交
        rand = random.choice([0, 1])
        if rand % 2 == 0:
            sell_order = cg.create_order(symbol=symbol_cg, side=2, price=buy_prices[0], amount=buy_amounts[0], sorce=3)
            buy_order = cg.create_order(symbol=symbol_cg, side=1, price=sell_prices[0], amount=sell_amounts[0], sorce=3)
        else:
            buy_order = cg.create_order(symbol=symbol_cg, side=1, price=sell_prices[0], amount=sell_amounts[0], sorce=3)
            sell_order = cg.create_order(symbol=symbol_cg, side=2, price=buy_prices[0], amount=buy_amounts[0], sorce=3)

        # 获取市场深度，买卖的挂单数量
        data = CgCoin.get_grades_from_cg(symbol_cg)
        print('买单深度：%d档，卖单深度：%d档' % (data['bids'], data['asks']))

        # 如果挂单数量足够，就撤单，否则挂单不用撤销
        if data['bids'] > number and data['asks'] <= number:
            repeal_orders(buy_id_list[1:])  # 撤买单
        if data['asks'] > number and data['bids'] <= number:
            repeal_orders(sell_id_list[1:])  # 撤卖单
        if data['bids'] > number and data['asks'] > number:
            t3 = Thread(target=repeal_orders, args=(buy_id_list[1:], ))
            t4 = Thread(target=repeal_orders, args=(sell_id_list[1:], ))
            t3.start()
            t4.start()
            t3.join()
            t4.join()
    except Exception as e:
        print(e)

    buy_id_list.clear()
    sell_id_list.clear()
    buy_prices.clear()
    sell_prices.clear()
    buy_amounts.clear()
    sell_amounts.clear()

    end = time.time()
    print('耗时：%f秒' % (end - start))


if __name__ == '__main__':
    main()





