import ccxt
import pandas as pd


pd.set_option('expand_frame_repr', False)
symbol = "NEWOS/ETH"
apiKey = '1ca4c9f5f5bf45b4a984fee9cc392dae'
secret = '2f3abdb44cc341088383d91e08e689ef'
fcoin = ccxt.fcoin({'apiKey': apiKey, 'secret': secret})

if __name__ == '__main__':
    data = fcoin.fetch_balance()
    balances = data['info']['data']
    for balance in balances:
        if balance['currency'] == 'newos' or balance['currency'] == 'eth':
            print(balance)

