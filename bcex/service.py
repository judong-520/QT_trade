from bcex.utils import build_my_sign, http_post


class Bcex:

    def __init__(self, api_key, secret_key):
        self.__apikey = api_key
        self.__secretkey = secret_key
        self.__url = 'www.bcex.top'

    # 下单交易
    def coin_trust(self, symbol, type, price, number):
        cointrust_resource = "/Api_Order/coinTrust"
        params = {
            'symbol': symbol,
            'type': type
        }
        if price:
            params['price'] = price
        if number:
            params['number'] = number
        params['sign'] = build_my_sign(params, self.__apikey, self.__secretkey)
        params['api_key'] = self.__apikey
        return http_post(self.__url, cointrust_resource, params)

    # 撤销挂单
    def cancel(self, symbol, order_id):
        cancel_source = "/Api_Order/cancel"
        params = {'symbol': symbol, 'order_id': order_id}
        params['sign'] = build_my_sign(params, self.__apikey, self.__secretkey)
        params['api_key'] = self.__apikey
        return http_post(self.__url, cancel_source, params)

    # 获取币种的交易行情
    def get_coin_trade(self, part, coin):
        coin_trade_resource = "/Api_Market/getCoinTrade"
        params = {
            'part': part,
            'coin': coin
        }
        return http_post(self.__url, coin_trade_resource, params)

    # 查询自己委托单的信息
    def trust_list(self, symbol, type):
        trade_list_resource = "/Api_Order/trustList"
        params = {'symbol': symbol, 'type': type}
        params['sign'] = build_my_sign(params, self.__apikey, self.__secretkey)
        params['api_key'] = self.__apikey
        return http_post(self.__url, trade_list_resource, params)

    # 查询自己成交单信息 自己成交的历史记录
    def order_list(self, symbol, type):
        order_list_resource = '/Api_Order/orderList'
        params = {'symbol': symbol, 'type': type}
        params['sign'] = build_my_sign(params, self.__apikey, self.__secretkey)
        params['api_key'] = self.__apikey
        return http_post(self.__url, order_list_resource, params)

    # 获取委托单信息
    def order_info(self, symbol, trust_id):
        """
        :param symbol:
        :param trust_id:
        :return:  status : 【状态  0：未成交  1：部分成交  2：全部成交  3：撤销委托】
        """
        order_info_resource = "/Api_Order/orderInfo"
        params = {'symbol': symbol,'trust_id': trust_id}
        params['sign'] = build_my_sign(params, self.__apikey, self.__secretkey)
        params['api_key'] = self.__apikey
        return http_post(self.__url, order_info_resource, params)

    # 查询挂单信息
    def trade_list(self, symbol, type):
        trade_list_resource = '/Api_Order/tradeList'
        params = {'symbol': symbol, 'type': type}
        params['sign'] = build_my_sign(params, self.__apikey, self.__secretkey)
        params['api_key'] = self.__apikey
        return http_post(self.__url, trade_list_resource, params)

    # 获取用户资产
    def user_balance(self):
        user_balance_resource = '/Api_User/userBalance'
        params = {}
        params['sign'] = build_my_sign(params, self.__apikey, self.__secretkey)
        params['api_key'] = self.__apikey
        return http_post(self.__url, user_balance_resource, params)

    # 获取市场深度
    def depth(self, symbol):
        depth_source = '/Api_Order/depth'
        params = {'symbol': symbol}
        return http_post(self.__url, depth_source, params)
