from dg.service import Digi

api_key = '5af415c00a1e5'
api_secret = '6a29ac697137bc0e66d613ec110b105805af415c5'
member_id = 171940386
dg = Digi(api_key, api_secret)

if __name__ == '__main__':
    msg = dg.get_userinfo(member_id)
    info = msg['info']
    free = info['free']
    freezed = info['freezed']
    print('eth可用资产：', free['ETH'])
    print('eth冻结资产：', freezed['ETH'])
    print('newos可用资产：', free['NEWOS'])
    print('newos冻结资产：', freezed['NEWOS'])



