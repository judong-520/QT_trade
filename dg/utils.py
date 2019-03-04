# -*- coding: utf-8 -*-
# 用于进行http请求，以及MD5加密，生成签名的工具类

import http.client
import urllib
import json
import hashlib


def build_my_sign(params, appSecret):
    """
    针对digifinex api 的签名方法
    :param params: 请求参数
    :param secretKey: 对请求进行签名的秘钥
    :return: md5加密的请求
    """
    m = hashlib.md5()
    params['appSecret'] = appSecret

    sign = ''
    for key in sorted(params.keys()):
        sign += str(params[key])
    m.update(sign.encode("utf-8"))
    encode_sign = m.hexdigest()
    return encode_sign


def http_get(url, resource, params):
    """
    获取数据
    :param url:
    :param resource:
    :param params:
    :return:
    """
    conn = http.client.HTTPSConnection(url, timeout=10)
    conn.request("GET", resource + '?' + params)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    return json.loads(data)


def http_post(url, resource, params):
    """
    提交数据
    :param url:
    :param resource:
    :param params:
    :return:
    """
    headers = {
        "Content-type": "application/x-www-form-urlencoded",  # 表单的数据形式导入
    }
    conn = http.client.HTTPSConnection(url, timeout=10)
    temp_params = urllib.parse.urlencode(params)  # 编码请求参数
    conn.request("POST", resource, temp_params, headers)  # 传入 POST请求方式，resource资源路径，temp_params请求参数，headers请求头
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    params.clear()
    conn.close()
    return data
