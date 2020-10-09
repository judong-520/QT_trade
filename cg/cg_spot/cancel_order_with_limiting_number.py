import time
import pandas as pd
from cg.cg_spot.service import CgCoin

pd.set_option('expand_frame_repr', False)


def repeal_ask(symbol, api_key, secret_key, num=15):
    """
    :param num: 限制数量，表示还剩多少的挂单
    :param symbol: 交易对
    :param api_key:
    :param secret_key:
    :return:
    """
    exchange = CgCoin()
    exchange.auth(api_key, secret_key)
    try:
        while True:
            # state : [int] 订单状态 0.正常 1.已完成 2.已撤销 3.部分成交 4.部分成交已撤销 5.撤销中 -1.获取历史成交
            order_info = exchange.get_order_list(symbol=symbol, state=0, page=0, size=1000)  # 可能会报签名错误
            if order_info['status'] == 200:
                break
        order_df = pd.DataFrame(order_info['data']['list'])  # 取order_info['data']['list']的信息，并将其转换成DataFrame格式
        # "side" : 交易方向 1.买入 2.卖出
        orders = order_df[order_df['side'] == 2]  # 筛选卖单深度列表
        orders = orders.sort_values(by='price')  # 对卖单按照价格排升序
        orders = orders.drop_duplicates(subset='price', keep='first')  # 价格去重
        ids = orders['id'][num:]  # 卖单的所有ID
        if list(ids):
            print('需要撤销的卖单ID：', '\n', ids)
            for id in ids:
                for _ in range(5):
                    order = exchange.cancel(id)
                    print('(%s)撤卖单：%s - %s' % (symbol, id, order))
                    if order['status'] == 200:
                        break
            time.sleep(0.5)
        else:
            print('暂无撤销的卖单！')
    except Exception as error:
        print('错误：', error)


def repeal_bid(symbol, api_key, secret_key, num=25):
    """
    :param num: 限制数量，表示还剩多少的挂单
    :param symbol: 交易对
    :param api_key:
    :param secret_key:
    :return:
    """
    exchange = CgCoin()
    exchange.auth(api_key, secret_key)
    try:
        while True:
            # state : [int] 订单状态 0.正常 1.已完成 2.已撤销 3.部分成交 4.部分成交已撤销 5.撤销中 -1.获取历史成交
            order_info = exchange.get_order_list(symbol=symbol, state=0, page=0, size=1000)  # 可能会报签名错误
            if order_info['status'] == 200:
                break
        order_df = pd.DataFrame(order_info['data']['list'])  # 取order_info['data']['list']的信息，并将其转换成DataFrame格式
        # "side" : 交易方向 1.买入 2.卖出
        orders = order_df[order_df['side'] == 1]  # 筛选买单深度列表
        orders = orders.sort_values(by='price', ascending=False)  # 对买单按价格排降序
        orders = orders.drop_duplicates(subset='price', keep='first')  # 价格去重
        # counter = orders.count()['id']  # 数量
        # print(counter)
        ids = orders['id'][num:]  # 买单的所有ID
        if list(ids):
            print('需要撤销的买单ID：', '\n', ids)
            for id in ids:
                for _ in range(5):
                    order = exchange.cancel(id)
                    print('(%s)撤买单：%s - %s' % (symbol, id, order))
                    if order['status'] == 200:
                        break
            time.sleep(0.5)
        else:
            print('暂无撤销的卖单！')
    except Exception as error:
        print('错误：', error)


def tasks():
    pass

if __name__ == '__main__':
    while True:
        tasks()
        time.sleep(30)
