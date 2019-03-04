# -*- coding:utf-8 -*-
import time
import pandas as pd
from cg.cg_spot.service import CgCoin

pd.set_option('expand_frame_repr', False)


def user_balance(user, symbol, api_key, secret_key, exchange=CgCoin()):
    for _ in range(30):
        exchange.auth(api_key, secret_key)
        msg = dict(exchange.get_user_balance())
        # print(msg)
        if msg['status'] == 200:
            data = msg['data']
            data = pd.DataFrame(data)  # 转换成dataframe格式
            data = pd.DataFrame(data, columns=['coin', 'amount', 'available'])  # 对dataframe的行进行帅选、从新排序
            data.rename(columns={'coin': '货币', 'amount': '总量', 'available': '可用量'}, inplace=True)
            print('%s(%s)的资产为：' % (user, symbol))
            print(str(data) + '\n')
            break
        time.sleep(1)


if __name__ == '__main__':
    user_balance('鞠东', 'eth_usdt', 'UQKf7SoPPCEY', 'tBLWXqyHeb6q')
    user_balance('未知1', 'cgt_eth(eth_usdt)', 'Lh82ERrRW', 'aXCG5YgtimPOX')

    user_balance('王庆磊', 'ltc_usdt','t58MnHss3YLl', 'EEuJPo9fcHYl')
    user_balance('未知2', 'ltc_usdt', 'aerNzk241QI', 'BFlZgeenMdcHYQ')

    user_balance('郁博文', 'eth_btc', 'WYKP0c3Eu2IO', 'Lehrk7QBal55')
    user_balance('未知3', 'eth_btc', 'RnFvcKkE63T', 'kE63TZUkSnHDmE')

    user_balance('邓志强', 'btc_usdt', 'j6sVMtrKDBnx', '0tjriE7pYSFB')
    user_balance('未知4', 'btc_usdt', 'kx9zjfxOVUR', 'g8qgQ6M46Dy')

    user_balance('胥新鑫', 'newos_eth','t14p3fPVY5dv', 'UsF1rrABRTHg')
    user_balance('未知5', 'newos_eth', 'xOVURpg8fd', '5RWL34NLjmasda')

    user_balance('杨茜然', 'newos_usdt','w2hItHQpAaMf', 'tssEhCRv3Y1n')
    user_balance('未知6', 'newos_usdt', 'mG3Jnp9Ne5', 'shIEIggcZd63T')


