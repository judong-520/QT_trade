def place_order(side, price, amount, exchange, symbol='NEWOS/ETH'):
    if side == 1:
        order_buy = exchange.create_limit_buy_order(symbol, amount, price)
        return order_buy
    elif side == 2:
        order_sell = exchange.create_limit_sell_order(symbol, amount, price)
        return order_sell
    else:
        print('提示：side的值只能为1或2：1表示买，2表示卖')


def get_bid_and_ask(exchange, symbol='NEWOS/ETH'):
    try:
        data = exchange.fetch_order_book(symbol)  # 获取市场深度信息
        bids = data['bids']  # 筛选买单深度
        bid = bids[0]  # 筛选买一的价格及数量
        asks = data['asks']  # 筛选卖单深度
        ask = asks[0]  # 筛选卖一的价格及数
        return bid[0], ask[0]
    except Exception as err:
        print(err)


def cancel_order(exchange, id):
    return exchange.cancel_order(id)
