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
        # 鞠东
        # repeal_orders(1, 'eth_usdt', 'UQKf7SoPPCEY', 'tBLWXqyHeb6q'),
        # repeal_orders(2, 'eth_usdt', 'UQKf7SoPPCEY', 'tBLWXqyHeb6q'),
        #
        # repeal_orders(1, 'cgt_eth', 'UQKf7SoPPCEY', 'tBLWXqyHeb6q', num=50),
        # repeal_orders(2, 'cgt_eth', 'UQKf7SoPPCEY', 'tBLWXqyHeb6q', num=0),

        # 邓志强
        # repeal_orders(1, 'btc_usdt', 'j6sVMtrKDBnx', '0tjriE7pYSFB'),
        # repeal_orders(2, 'btc_usdt', 'j6sVMtrKDBnx', '0tjriE7pYSFB'),
        # repeal_orders(1, 'ltc_usdt', 'j6sVMtrKDBnx', '0tjriE7pYSFB'),
        # repeal_orders(2, 'ltc_usdt', 'j6sVMtrKDBnx', '0tjriE7pYSFB'),

        # 王庆磊
        # repeal_orders(1, 'ltc_usdt', 't58MnHss3YLl', 'EEuJPo9fcHYl', num=15),
        # repeal_orders(2, 'ltc_usdt', 't58MnHss3YLl', 'EEuJPo9fcHYl', num=15),

        # repeal_orders(1, 'cgt_eth', 't58MnHss3YLl', 'EEuJPo9fcHYl', num=50),
        repeal_orders(2, 'cgt_eth', 't58MnHss3YLl', 'EEuJPo9fcHYl', num=0),

        # 堉博文
        # repeal_orders(1, 'eth_btc', 'WYKP0c3Eu2IO', 'Lehrk7QBal55', num=15),
        # repeal_orders(2, 'eth_btc', 'WYKP0c3Eu2IO', 'Lehrk7QBal55', num=15),

        # 杨熙然
        # repeal_orders(1, 'newos_eth', 'w2hItHQpAaMf', 'tssEhCRv3Y1n'),
        # repeal_orders(2, 'newos_eth', 'w2hItHQpAaMf', 'tssEhCRv3Y1n'),
        #
        # # 胥新新
        # repeal_orders(1, 'newos_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        # repeal_orders(2, 'newos_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        #
        # repeal_orders(1, 'soc_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        # repeal_orders(2, 'soc_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        #
        # repeal_orders(1, 'eos_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        # repeal_orders(2, 'eos_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        #
        # repeal_orders(1, 'omg_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        # repeal_orders(2, 'omg_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        #
        # repeal_orders(1, 'zil_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        # repeal_orders(2, 'zil_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        #
        # repeal_orders(1, 'ocn_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        # repeal_orders(2, 'ocn_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        #
        # repeal_orders(1, 'gnt_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        # repeal_orders(2, 'gnt_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        #
        # repeal_orders(1, 'iost_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        # repeal_orders(2, 'iost_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        #
        # repeal_orders(1, 'dta_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        # repeal_orders(2, 'dta_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        #
        # repeal_orders(1, 'cvc_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        # repeal_orders(2, 'cvc_usdt', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        #
        # repeal_orders(1, 'ae_eth', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        # repeal_orders(2, 'ae_eth', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        #
        # repeal_orders(1, 'bat_eth', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
        # repeal_orders(2, 'bat_eth', 't14p3fPVY5dv', 'UsF1rrABRTHg'),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

