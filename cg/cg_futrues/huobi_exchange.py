import json
import pandas as pd

from urllib.request import urlopen, Request

# API 请求地址
BASE_URl = "https://api.huobi.pro"


def get_url_content(url, max_retry=5, headers=None):
    """抓取数据"""
    try_num = 0

    try:
        request = Request(url=url, headers=headers)
        content = urlopen(request, timeout=10).read()
        return content
    except Exception as e:
        print("异常：", e)
        try_num += 1
        if try_num >= max_retry:
            print("尝试失败次数过多， 放弃尝试")
            return None


def get_market_depth(symbol='btcusdt', type='step1'):
    """
    获取市场深度数据 GET /market/depth
    :param symbol: 交易对 列如：btcusdt, bchbtc, rcneth ...
    :param type:[string]step0, step1, step2, step3, step4, step5（合并深度0-5）；step0时，不合并深度
    :return: bids_list:[[price(成交价), amount(成交量)], ...],按price降序; asks_list:[[price(成交价), amount(成交量)], ...] 按price升序
    """
    url = BASE_URl + '/market/depth?symbol=%s&type=%s' % (symbol, type)
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
        bids_list = tick_dict.get('bids', None)
        asks_list = tick_dict.get('asks', None)
        if bids_list and asks_list:
            return bids_list, asks_list


if __name__ == '__main__':
    data = get_market_depth()
    print(data)
