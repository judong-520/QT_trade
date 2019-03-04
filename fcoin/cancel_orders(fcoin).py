import ccxt
import pandas as pd
from fcoin.service import cancel_order


pd.set_option('expand_frame_repr', False)
symbol = "NEWOS/ETH"
apiKey = '1ca4c9f5f5bf45b4a984fee9cc392dae'
secret = '2f3abdb44cc341088383d91e08e689ef'
fcoin = ccxt.fcoin({'apiKey': apiKey, 'secret': secret})

if __name__ == '__main__':
    # data = fcoin.fetch_trades(symbol, limit=50)  # 获取订单信息
    # data = pd.DataFrame(data)
    # print(data)

    # data = fcoin.fetch_closed_orders(symbol)  # 获取关闭订单
    # data = pd.DataFrame(data)
    # print(data)

    data = fcoin.fetch_open_orders(symbol)  # 获取开放订单
    data = pd.DataFrame(data)
    orders = data.sort_values(by='price')  # 对卖单按照价格排升序
    # print(orders)
    orders = pd.DataFrame(orders, columns=[ 'side', 'price', 'amount', 'id', 'symbol'])  # 对所有的columes进行帅选

    buy_orders = orders[orders['side'] == 'buy']
    print('买单：')
    print(buy_orders)

    sell_orders = orders[orders['side'] == 'sell']
    print('卖单：')
    print(sell_orders)

    for id in sell_orders['id']:
        cancel_order = fcoin.cancel_order(id)
        print('撤销卖单：', cancel_order)

    # for id in buy_orders['id']:
    #     cancel_order = fcoin.cancel_order(id)
    #     print('撤销买单：', cancel_order)

