import json
import datetime
import pandas as pd
from bcex.service import Bcex


symbol = 'newos2eth'
api_key = ""
secret_key = ""
bcex = Bcex(api_key, secret_key)


def balance():
    try:
        msg = bcex.user_balance()
        msg = json.loads(msg)
        data = msg['data']
        print('eth剩余资产：', data['eth_over'])
        print('eth冻结资产：', data['eth_lock'])
        print('newos剩余资产：', data['newos_over'])
        print('newos冻结资产：', data['newos_lock'])
    except Exception as err:
        print(err)


if __name__ == '__main__':
    balance()

