from dg.utils import http_post, build_my_sign, http_get


class Digi:

    def __init__(self, apikey, appsecret):
        self.__url = 'www.digifinex.com'
        self.__apikey = apikey
        self.__appsecret = appsecret

    def get_market_depth(self, symbol='eth_newos'):
        """
        获取
        :param symbol:交易对，例如usdt_btc
        :return:
        """
        MARKET_DEPTH_RESOURCE = "/api/depth"
        params = {
            'symbol': symbol
        }
        sign = build_my_sign(params, self.__appsecret)
        params = 'symbol=%(symbol)s&appKey=%(appKey)s&sign=%(sign)s' \
                 % {'symbol': symbol, 'appKey': self.__apikey, 'sign': sign}
        return http_get(self.__url, MARKET_DEPTH_RESOURCE, params)

    def get_trades(self, symbol='eth_newos'):
        """
        :param symbol:
        :return: 返回交易信息
        """
        TRADES_RESOURCE = "/api/trades"
        params = {
            'symbol': symbol
        }
        sign = build_my_sign(params, self.__appsecret)
        params = 'symbol=%(symbol)s&appKey=%(appKey)s&sign=%(sign)s' \
                 % {'symbol': symbol, 'appKey': self.__apikey, 'sign': sign}
        return http_get(self.__url, TRADES_RESOURCE, params)

    def get_kline(self, type='kline_1m', symbol='eth_newos'):
        """
        获取K线信息
        :param symbol:交易对，例如usdt_btc
        :param type:K线类型: kline_1m/kline_5m/kline_15m/kline_30m/kline_1h/kline_1d/kline_1w
        :return:
        """
        KLINE_RESOURCE = "/api/kline"
        params = {
            'symbol': symbol,
            'type': type
        }
        sign = build_my_sign(params, self.__appsecret)
        if symbol and type:
            params = 'symbol=%(symbol)s&type=%(type)s&appKey=%(appKey)s&sign=%(sign)s' \
                     % {'symbol': symbol, 'type': type, 'appKey': self.__apikey, 'sign': sign}
        return http_get(self.__url, KLINE_RESOURCE, params)

    def get_ticker(self, symbol='eth_newos'):
        """
        获取详情数据
        :param symbol: 交易对，如btc_ltc；类型string
        :return:
        """
        TICKER_RESOURCE = "/api/ticker"
        params = {
            'symbol': symbol,
            'appKey': self.__apikey
        }
        sign = build_my_sign(params, self.__appsecret)
        params = 'symbol=%(symbol)s&appKey=%(appKey)s&sign=%(sign)s' \
                 % {'symbol': symbol, 'appKey': self.__apikey, 'sign': sign}
        return http_get(self.__url, TICKER_RESOURCE, params)

    def send_trade_order(self, symbol, amount, price, tradetype, member_id):
        """
        发送买/卖交易订单操作
        :param symbol: 币对,string
        :param tradetype: 交易类型，sell/buy,string
        :param amount: 交易数量，float
        :param price: 交易价格，float
        :param member_id: 账号ID,int
        :return:
        """
        TRADE_ORDER_RESOURCE = "/api/trade"
        params = {
            'symbol': symbol,
            'price': price,
            'amount': amount,
            'tradetype': tradetype,
            'member_id': member_id,
            'appKey': self.__apikey
        }
        sign = build_my_sign(params, self.__appsecret)
        params = 'symbol=%(symbol)s&tradetype=%(tradetype)s&amount=%(amount)s&' \
                 'price=%(price)s&member_id=%(member_id)s&appKey=%(appKey)s&sign=%(sign)s' \
                 % {'symbol': symbol, 'tradetype': tradetype, 'amount': amount,
                    'price': price, 'member_id': member_id, 'appKey': self.__apikey, 'sign': sign}
        return http_get(self.__url, TRADE_ORDER_RESOURCE, params)

    def get_order_info(self, symbol, jobid, member_id):
        """
        获取订单详情
        :param symbol:
        :param jobid: 要查询的订单ID，多个订单用逗号分隔，最多支持20个订单
        :param member_id:
        :return:订单状态：-1/已撤单，0/挂单成功，1/部分成交，2/完全成交
        """
        ORDER_INFO_RESOURCE = "/api/order_info"
        params = {
            'symbol': symbol,
            'jobid': jobid,
            'member_id': member_id,
            'appKey': self.__apikey
        }
        sign = build_my_sign(params, self.__appsecret)
        params = 'symbol=%(symbol)s&jobid=%(jobid)s&member_id=%(member_id)s&appKey=%(appKey)s&sign=%(sign)s' \
                 % {'symbol': symbol, 'jobid': jobid, 'member_id': member_id, 'appKey': self.__apikey, 'sign': sign}
        return http_get(self.__url, ORDER_INFO_RESOURCE, params)

    def cancel_order(self, jobid, member_id):
        """
        撤销订单
        :param jobid: | orders_id | true | int/string | 订单ID，支持单词传多个，用英文逗号隔开，每次最多20个 |
        :param member_id:
        :return:
        """
        CANCEL_ORDER_RESOURCE = "/api/cancel_order"
        params = {
            'jobid': jobid,
            'member_id': member_id,
            'appKey': self.__apikey
        }
        sign = build_my_sign(params, self.__appsecret)
        params = 'jobid=%(jobid)s&member_id=%(member_id)s&appKey=%(appKey)s&sign=%(sign)s' \
                 % {'jobid': jobid, 'member_id': member_id, 'appKey': self.__apikey, 'sign': sign}
        return http_get(self.__url, CANCEL_ORDER_RESOURCE, params)

    def get_userinfo(self, member_id):
        """
        获取用户资产信息
        :param member_id:
        :return:
        """
        USER_INFO_RESOURCE = "/api/userinfo"
        params = {
            'member_id': member_id,
            'appKey': self.__apikey
        }
        sign = build_my_sign(params, self.__appsecret)
        params = 'member_id=%(member_id)s&appKey=%(appKey)s&sign=%(sign)s' \
                 % {'member_id': member_id, 'appKey': self.__apikey, 'sign': sign}
        return http_get(self.__url, USER_INFO_RESOURCE, params)

    def get_open_orders(self, type, member_id, symbol='eth_newos', page=0):
        OPEN_ORDER_RESOURCE = "/api/open_orders"
        params = {
            'symbol': symbol,
            'page': page,
            'type': type,
            'member_id': member_id,
            'appKey': self.__apikey
        }
        sign = build_my_sign(params, self.__appsecret)
        print(sign)
        params = 'symbol=%(symbol)s&type=%(type)s&page=%(page)s&appKey=%(appKey)s&sign=%(sign)s' \
                 % {'symbol': symbol, 'type': type,'page': page, 'appKey': self.__apikey, 'sign': sign}
        print(params)
        return http_get(self.__url, OPEN_ORDER_RESOURCE, params)


if __name__ == '__main__':
    api_key = '5af415c00a1e5'
    api_secret = '6a29ac697137bc0e66d613ec110b105805af415c5'
    member_id = 171940386
    dg = Digi(api_key, api_secret)
    symbol = 'eth_newos'

    msg = dg.get_open_orders('sell', member_id)
    print(msg)

    # mag = dg.get_trades()
    # print(mag)
