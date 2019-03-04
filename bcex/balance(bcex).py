import json
import datetime
import pandas as pd
from bcex.service import Bcex


symbol = 'newos2eth'
api_key = "5697f192d83a7c0c505f10a4975a519b6c82c12eda173dd414854a90f86ea99c"
secret_key = "5bd1-93170-0b0b1-6680-0830"
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

