import time
import asyncio
import pandas as pd

from cg.cg_spot.service import CgCoin

pd.set_option('expand_frame_repr', False)


async def repeal_orders(side, symbol, api_key, secret_key, num=25):
    """
    :param side: "side" : 控制交易方向 1.买入 2.卖出
    :param symbol: 交易对
    :param api_key:
    :param secret_key:
    :param num: 用于控制触发撤单的数目
    :return:
    """
    exchange = CgCoin()
    exchange.auth(api_key, secret_key)
    try:
        for _ in range(10):
            # state : [int] 订单状态 0.正常 1.已完成 2.已撤销 3.部分成交 4.部分成交已撤销 5.撤销中 -1.获取历史成交
            info = exchange.get_order_list(symbol=symbol, state=0, page=0, size=30000)  # 可能会报签名错误
            if info['status'] == 200:
                break
            print(info)
        data = pd.DataFrame(info['data']['list'])  # 取order_info['data']['list']的信息，并将其转换成DataFrame格式
        await  asyncio.sleep(1)

        # "side" : 交易方向 1.买入 2.卖出
        if side == 1:
            msg = data[data['side'] == 1]  # 筛选买单深度列表信息
            orders = pd.DataFrame(msg, columns=['price', 'amount', 'id'])  # 过滤信息，只看'price', 'amount', 'id'这三列
            orders = orders.sort_values(by='price', ascending=False)  # 对买单按价格排降序
            orders_dup = orders.drop_duplicates(subset='price', keep='first')  # 价格去重，重复元素保留第一个
            counter_1 = orders_dup.count()['id']  # 数量
            print('%s买单深度:%s档' % (symbol, counter_1))
            if counter_1 >= num:
                all_orders = orders.append(orders_dup.head(num))
                all_orders = all_orders.sort_values(by='price', ascending=False)  # 排降序
                _orders = all_orders.drop_duplicates(subset=['id'], keep=False)  # _orders为orders与orders_dup.head(num)的差集
                buy_ids = _orders['id']  # 卖单的所有ID
                print('需要撤销的买单ID：', '\n', buy_ids)
                for id in buy_ids:
                    await asyncio.sleep(1)
                    for _ in range(5):
                        order = exchange.cancel(id)
                        print('(%10s)撤买单：%s - %s' % (symbol, id, order))
                        if order['status'] == 200:
                            break
                    # time.sleep(1)
            else:
                print('%s暂无撤销的买单！' % symbol)

        elif side == 2:
            msg = data[data['side'] == 2]  # 筛选买单深度列表信息
            orders = pd.DataFrame(msg, columns=['price', 'amount', 'id'])  # 过滤信息，只看'price', 'amount', 'id'这三列
            orders = orders.sort_values(by='price')  # 对卖单按价格排升序
            orders_dup = orders.drop_duplicates(subset='price', keep='first')  # 价格去重，重复元素保留第一个
            counter_2 = orders_dup.count()['id']  # 数量
            print('%s卖单深度:%s档' % (symbol, counter_2))
            if counter_2 >= num:
                all_orders = orders.append(orders_dup.head(num))
                all_orders = all_orders.sort_values(by='price')
                _orders = all_orders.drop_duplicates(subset=['id'], keep=False)   # _orders为orders与orders_dup.head(num)的差集
                sell_ids = _orders['id']  # 卖单的所有ID
                print('需要撤销的卖单ID：', '\n', sell_ids)
                for id in sell_ids:
                    await asyncio.sleep(1)
                    for _ in range(5):
                        order = exchange.cancel(id)
                        print('(%10s)撤卖单：%s - %s' % (symbol, id, order))
                        if order['status'] == 200:
                            break
                    # time.sleep(1)
            else:
                print('%s暂无撤销的卖单！' % symbol)

        else:
            print('传参错误, "side"控制交易方向:  1.买入 2.卖出')

        print('*******************************************************************')
    except Exception as error:
        print('错误：', error)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [
        repeal_orders(2, 'cgt_eth', '', '', num=0),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

