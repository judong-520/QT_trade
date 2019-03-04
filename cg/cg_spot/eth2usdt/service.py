import json
import hmac
import hashlib
import requests
import time
import base64
import datetime
from websocket import create_connection
from urllib.request import urlopen, Request


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

    @staticmethod
    def exception_record(filename, msg):
        now = str(datetime.datetime.now()).split('.')[0]
        content = '时间：%s，异常信息：%s' % (now, msg)
        with open(filename, 'a') as f:
            f.write(content + '\n')

    @staticmethod
    def get_url_data(url, retry_times=3):
        """
        从API接口中获取数据
        :param url: API接口
        :param retry_times:最大尝试次数
        :return: API json格式数据
        """
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            request = Request(url=url, headers=headers)
            b_data = urlopen(request, timeout=10).read()
            str_data = b_data.decode('utf-8')
            json_data = json.loads(str_data)
            return json_data
        except Exception as http_error:
            if retry_times > 0:
                return CgCoin.get_url_data(url, retry_times=retry_times - 1)
            else:
                CgCoin.exception_record('./url_data_info.txt', str(http_error))
                return None

    @staticmethod
    def get_depth_from_bcex(symbol, num=10):
        """
        获取bcex市场深度信息
        :param symbol: 币种, 比如 btc2ckusd、ltc2btc、eos2cnet(注意:数字2前面代表币名，2后面是币对应的交易区)
        :param num: 数量限制，只取有用的多少个数据
        :return:买单深度、卖单深度
        """
        base_url = 'https://www.bcex.top/Api_Order/depth?symbol='
        url = base_url + symbol
        info = CgCoin.get_url_data(url)
        if info:
            try:
                data = info['data']
                bids = data['bids'][:num]
                asks = data['asks'][:num:-1]
                return bids, asks
            except Exception as data_error:
                CgCoin.exception_record('./bcex_data_info.txt', str(data_error))
        else:
            return None, None

    @staticmethod
    def get_depth_from_huobi(symbol, num=10, type='step1'):
        """
        火币市场深度信息
        :param symbol:交易对
        :param num: 数量限制，只取有用的多少个数据
        :param type:
        :return:
        """
        base_url = 'https://api.huobi.pro'
        url = base_url + '/market/depth?symbol=%s&type=%s' % (symbol, type)
        info = CgCoin.get_url_data(url)
        if info:
            try:
                tick = info['tick']
                bids = tick['bids'][:num]
                asks = tick['asks'][:num]
                return bids, asks
            except Exception as data_error:
                CgCoin.exception_record('./huobi_data_info.txt', str(data_error))
        else:
            return None, None

    @staticmethod
    def get_grades_from_cg(symbol):
        """
        获取cg平台市场深度的买卖方的档数
        :param symbol:交易对
        :return:
        """
        data = {}
        url = 'wss://i.cg.net/wi/ws'
        for _ in range(5):  # 链接，连接上就退出循环
            try:
                ws = create_connection(url)
                break
            except Exception as e:
                CgCoin.exception_record('./ws_data_info.txt', str(e))
                continue
        for _ in range(5):  # 连接上，退出第一个循环之后，此循环用于获取数据
            sign = '%s.deep' % symbol
            msg = '{"event":"subscribe", "channel":"%s"}' % sign
            ws.send(msg)
            response = str(ws.recv())
            response = json.loads(response)
            if response['type'] == sign:
                bids = response['data']['bids']
                bids_num = int(len(bids) / 2)
                data['bids'] = bids_num
                asks = response['data']['asks']
                asks_num = int(len(asks) / 2)
                data['asks'] = asks_num
                return data



