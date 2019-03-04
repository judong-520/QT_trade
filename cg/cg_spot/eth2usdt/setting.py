# 需要修改项
api_key = "t14p3fPVY5dv"
secret_key = "UsF1rrABRTHg"
price_low = 0.01  # 货币获取的价格，在该价格上加上随机价格下限（改该参数的时候注意小数点后保留的位数）
price_up = 0.09  # 货币获取的价格，在该价格上加上随机价格上限
gross_low = 10  # 总金额下限
gross_up = 20   # 总金额上限
amount_digit = 4  # cg平台该交易对数量有几位小数点，这里就填几
number = 25   # 默认有25个挂单，用于控制深度的数量，大于该数量，则撤单，否则默认处理（不撤单）
symbol_cg = 'eth_usdt'
symbol_bcex = 'eth2usdt'
symbol_huobi = 'ethusdt'

# 无需修改项
buy_id_list = []
sell_id_list = []
buy_prices = []
sell_prices = []
buy_amounts = []
sell_amounts = []
