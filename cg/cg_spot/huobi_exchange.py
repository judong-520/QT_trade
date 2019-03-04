import json
import pandas as pd

from urllib.request import urlopen, Request

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# API 请求地址
BASE_URl = "https://api.huobi.pro"


def get_url_content(url, max_try_number=5, headers=None):
    """抓取数据"""
    try_num = 0

    while True:
        try:
            request = Request(url=url, headers=headers)
            content = urlopen(request, timeout=15).read()
            return content
        except Exception as e:
            print(url, "抓取报错", e)
            try_num += 1
            if try_num >= max_try_number:
                print("尝试失败次数过多， 放弃尝试")
                return None


def get_market_trade(symbol='btcusdt'):
    """
    获取最近的成交交易数据（价格，数量）
    :param symbol:
    :return:
    """
    while True:
        url = BASE_URl + '/market/trade?symbol=%s' % symbol
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
            "Content - Type": "application / x - www - form - urlencoded"
        }
        content = get_url_content(url, 5, headers=headers)

        if content:
            content = content.decode('utf-8')
            json_dict = json.loads(content)
            print('huobi_trade-->',json_dict)
            price = json_dict.get('tick').get('data')[0]['price']
            amount = json_dict.get('tick').get('data')[0]['amount']
            # close = tick_dict.get('close', None)
            return price, amount


def get_market_detail_merged(symbol='btcusdt'):
    """
    获取聚合行情(Ticker) GET /market/detail/merged
    :param symbol:交易对 列如：btcusdt, bchbtc, rcneth ...
    :return: amount:成交量 close:收盘价,当K线为最晚的一根时，是最新成交价
    """
    while True:
        url = BASE_URl + '/market/detail/merged?symbol=%s' % symbol
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
            "Content - Type": "application / x - www - form - urlencoded"
        }
        content = get_url_content(url, 5, headers=headers)

        if content:
            content = content.decode('utf-8')
            json_dict = json.loads(content)
            print(json_dict)
            tick_dict = json_dict.get('tick', None)
            amount = tick_dict.get('amount', None)
            close = tick_dict.get('close', None)
            return amount, close


def get_market_depth(symbol='btcusdt', type='step1'):
    """
    获取市场深度数据 GET /market/depth
    :param symbol: 交易对 列如：btcusdt, bchbtc, rcneth ...
    :param type:[string]step0, step1, step2, step3, step4, step5（合并深度0-5）；step0时，不合并深度
    :return: bids_list:[[price(成交价), amount(成交量)], ...],按price降序; asks_list:[[price(成交价), amount(成交量)], ...] 按price升序
    """
    while True:
        url = BASE_URl + '/market/depth?symbol=%s&type=%s' % (symbol, type)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
            "Content - Type": "application / x - www - form - urlencoded"
        }
        content = get_url_content(url, 5, headers=headers)
        if content:
            content = content.decode('utf-8')
            json_dict = json.loads(content)
            tick_dict = json_dict.get('tick', None)
            bids_list = tick_dict.get('bids', None)
            asks_list = tick_dict.get('asks', None)
            if bids_list and asks_list:
                return bids_list, asks_list


if __name__ == '__main__':
    print(get_market_trade())

# api接口地址
# https://github.com/huobiapi/API_Docs/wiki/REST_api_reference#get-marketdepth-%E8%8E%B7%E5%8F%96-market-depth-%E6%95%B0%E6%8D%AE

"""
GET /market/detail/merged 获取聚合行情(Ticker)
请求参数:

参数名称	是否必须	 类型	描述 	默认值	取值范围
symbol	true	string	交易对		    btcusdt, bchbtc, rcneth ...
响应数据:

参数名称	是否必须	数据类型	描述	取值范围
status	true	string	请求处理结果	"ok" , "error"
ts	    true	number	响应生成时间点，单位：毫秒	
tick	true	object	K线数据	
ch	    true	string	数据所属的 channel，格式： market.$symbol.detail.merged	
tick 说明:
  "tick": {
    "id": K线id,
    "amount": 成交量,
    "count": 成交笔数,
    "open": 开盘价,
    "close": 收盘价,当K线为最晚的一根时，是最新成交价
    "low": 最低价,
    "high": 最高价,
    "vol": 成交额, 即 sum(每一笔成交价 * 该笔的成交量)
    "bid": [买1价,买1量],
    "ask": [卖1价,卖1量]
  }

请求响应示例:

/* GET /market/detail/merged?symbol=ethusdt */
{
"status":"ok",
"ch":"market.ethusdt.detail.merged",
"ts":1499225276950,
"tick":{
  "id":1499225271,
  "ts":1499225271000,
  "close":1885.0000,
  "open":1960.0000,
  "high":1985.0000,
  "low":1856.0000,
  "amount":81486.2926,
  "count":42122,
  "vol":157052744.85708200,
  "ask":[1885.0000,21.8804],
  "bid":[1884.0000,1.6702]
  }
}

/* GET /market/detail/merged?symbol=not-exist */
{
  "ts": 1490758171271,
  "status": "error",
  "err-code": "invalid-parameter",
  "err-msg": "invalid symbol”
}
"""

"""
GET /market/depth 获取 Market Depth 数据
请求参数:

参数名称	是否必须	类型	描述	默认值	取值范围
symbol	true	string	交易对		btcusdt, bchbtc, rcneth ...
type	true	string	Depth 类型		step0, step1, step2, step3, step4, step5（合并深度0-5）；step0时，不合并深度
用户选择“合并深度”时，一定报价精度内的市场挂单将予以合并显示。合并深度仅改变显示方式，不改变实际成交价格。

响应数据:
参数名称	是否必须	数据类型	描述	取值范围
status	true	string		"ok" 或者 "error"
ts	    true	number	响应生成时间点，单位：毫秒	
tick	true	object	Depth 数据	
ch	    true	string	数据所属的 channel，格式： market.$symbol.depth.$type	

tick 说明:
  "tick": {
    "id": 消息id,
    "ts": 消息生成时间，单位：毫秒,
    "bids": 买盘,[price(成交价), amount(成交量)], 按price降序,
    "asks": 卖盘,[price(成交价), amount(成交量)], 按price升序
  }

请求响应示例:
/* GET /market/depth?symbol=ethusdt&type=step1 */
{
  "status": "ok",
  "ch": "market.btcusdt.depth.step1",
  "ts": 1489472598812,
  "tick": {
    "id": 1489464585407,
    "ts": 1489464585407,
    "bids": [
      [7964, 0.0678], // [price, amount]
      [7963, 0.9162],
      [7961, 0.1],
      [7960, 12.8898],
      [7958, 1.2],
      [7955, 2.1009],
      [7954, 0.4708],
      [7953, 0.0564],
      [7951, 2.8031],
      [7950, 13.7785],
      [7949, 0.125],
      [7948, 4],
      [7942, 0.4337],
      [7940, 6.1612],
      [7936, 0.02],
      [7935, 1.3575],
      [7933, 2.002],
      [7932, 1.3449],
      [7930, 10.2974],
      [7929, 3.2226]
    ],
    "asks": [
      [7979, 0.0736],
      [7980, 1.0292],
      [7981, 5.5652],
      [7986, 0.2416],
      [7990, 1.9970],
      [7995, 0.88],
      [7996, 0.0212],
      [8000, 9.2609],
      [8002, 0.02],
      [8008, 1],
      [8010, 0.8735],
      [8011, 2.36],
      [8012, 0.02],
      [8014, 0.1067],
      [8015, 12.9118],
      [8016, 2.5206],
      [8017, 0.0166],
      [8018, 1.3218],
      [8019, 0.01],
      [8020, 13.6584]
    ]
  }
}
"""
