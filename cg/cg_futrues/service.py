import hmac
import hashlib
import requests
import time
import base64


class CgCoin():
    def __init__(self, base_url='https://i.cg.net'):
        self.base_url = base_url

    def auth(self, key, secret):
        self.key = bytes(key, 'utf-8')
        self.secret = bytes(secret, 'utf-8')

    def public_request(self, method, api_url, **payload):
        """request public url"""
        r_url = self.base_url + api_url
        try:
            r = requests.request(method, r_url, params=payload)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        if r.status_code == 200:
            return r.json()

    def get_signed(self, sig_str):
        """signed params use sha512"""
        sig_str = base64.b64encode(sig_str)
        signature = hmac.new(self.secret, sig_str, digestmod=hashlib.sha1).hexdigest()
        return signature

    def signed_request(self, method, api_url, **payload):
        """request a signed url"""
        param = ''
        if payload:
            sort_pay = sorted(payload.items())
            for k in sort_pay:
                param += '&' + str(k[0]) + '=' + str(k[1])
            param = param.lstrip('&')
        timestamp = str(int(time.time()) * 1000)
        full_url = self.base_url + api_url
        if method == 'GET':
            if param:
                get_url = api_url + '?' + param
                sig_str = timestamp + get_url
            else:
                sig_str = timestamp + api_url
        elif method == 'POST':
            sig_str = timestamp + api_url + param
        signature = self.get_signed(bytes(sig_str, 'utf-8'))

        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'X-ACCESS-KEY': self.key,
            'X-ACCESS-SIGNATURE': signature,
            'X-ACCESS-TIMESTAMP': timestamp,

        }

        if method == 'POST':
            try:
                r = requests.post(url=full_url, headers=headers, data=payload)
                r.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
                print(r.text)
            if r.status_code == 200:
                return r.json()
        elif method == 'GET':
            try:
                r = requests.request(method, full_url, headers=headers, params=payload)
                r.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
                print(r.text)
            if r.status_code == 200:
                return r.json()

    def get_symbols(self):
        """get all symbols"""
        return self.signed_request('GET', '/api/symbols')

    def get_user_balance(self):
        """查询账户余额"""
        return self.signed_request('GET', '/api/user/balance/spot')

    def get_order_info(self, id):
        """查询订单信息"""
        return self.signed_request('GET', '/api/order/{id}'.format(id=id))

    def get_order_list(self, symbol, state, **payload):
        """获取订单列表"""
        return self.signed_request('GET', '/api/orders/{symbol}/{state}'.format(symbol=symbol, state=state), **payload)

    def create_order(self, **payload):
        """下单"""
        return self.signed_request('POST', '/api/order', **payload)

    def cancel(self, id):
        """撤单"""
        return self.signed_request('POST', '/api/order/{id}/cancel'.format(id=id))

    def get_trades(self, symbol, **payload):
        """获取成交历史记录"""
        return self.signed_request('GET', '/api/trades/{symbol}'.format(symbol=symbol), **payload)

    def get_kline(self, symbol, candle_type, **payload):
        """获取k线"""
        return self.signed_request('GET',
                                   '/api/candle/{symbol}/{candle_type}'.format(symbol=symbol, candle_type=candle_type),
                                   **payload)

