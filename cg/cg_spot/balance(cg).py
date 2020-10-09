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
    pass



