# *_*coding:utf-8 *_*
#
import os
import random
import threading  # Python主要通过标准库中的threading包来实现多线程
import time
from typing import Dict

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from constant import *
from utils import find_path


def doChore():  # 作为间隔  每次调用间隔0.5s
	time.sleep(0.5)


user_agent_list = [
	'Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 MicroMessenger/7.0.10.1580(0x27000A5E) Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm64',
	'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
	'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
	'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']

header = {
	'content-type': 'application/json;charset=UTF-8',
	'accept': '*/*',
	'accept-language': 'zh-cn',
	'accesstoken': 'RJI37QNDMKCBQA2P4RUK6XTZY7R4LSS5US4BHPP2PN755Q276TYA113528c',
	'accept-Encoding': 'br,gzip,deflate',
	'cache-control': 'no-cache',
	'content-Length': '274',
	'referer': 'https://servicewechat.com/wx2672757b4553d5d7/602/page-frame.html',
	#'user-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.0(0x18000026) NetType/WIFI Language/zh_CN',
	'user-agent':random.choice(user_agent_list),
	'code-version':'[object Undefined]',
	'xcx-version':'3.19.83'
}

url_A = 'https://api.pinduoduo.com/api/ktt_order_core/customer/ordering/query_base_info_on_order_page?xcx_version=3.19.83'

session = requests.session()

# A
response = session.post(url=url_A, json=PARAMS_MASK, headers=header, verify = False)
data = response.json()

print(data)
print("done")

# A
pay_url_A = 'https://api.pinduoduo.com/api/collection_activity/order/generate_biz_order_no_v3?xcx_version=3.19.83'
response = session.post(url=pay_url_A, json=PAY_A, headers=header, verify = False)
data = response.json()

if data['success']:
	a_id = data['result'][0]

print(data)
print(a_id)
print("done")

# B

pay_url_B = 'https://api.pinduoduo.com/api/collection_activity/order/batch_create_order?xcx_version=3.19.83'
PAY_B['orderGoodsList'][0]['bizOrderNo'] = a_id

print(PAY_B)
print("===")
response = session.post(url=pay_url_B, json=PAY_B, headers=header, verify = False)
data = response.json()

if data['success']:
	#"orderSn": "210123-295424000662898",
	#"bizOrderNo": "5f362fe37733165fd3c3ad8a01ed81f6",
	orderSn = data['result']['orderSn']
	bizOrderNo = data['result']['bizOrderNo']

print(data)
print(orderSn)
print(bizOrderNo)
print("done")

# B2 支付

pay_url_B = 'https://api.pinduoduo.com/order/prepay?xcx_version=3.19.83&pay_app_id=128&order_sn=210123-295424000662898&parent_order_sn=210123-295424000662898&version=3'
PAY_B2['order_sn']= orderSn

time.sleep(3)
print(PAY_B2)
print("===")
response = session.post(url=pay_url_B, params=PAY_B2, json = {} ,headers=header, verify = False)
data = response.json()

if data['success']:
	prepay_id = data['package'].split("=")[1]

print(data)
print(prepay_id)


# C
pay_url_C = 'https://api.pinduoduo.com/api/collection_activity/order/record_prepay_id_v2?xcx_version=3.19.83'
PAY_C['bizOrderSnList'] = [orderSn]
PAY_C['prepayId'] = prepay_id


print(PAY_C)
print("===")
response = session.post(url=pay_url_C, json=PAY_C, headers=header, verify = False)
data = response.json()

if data['success']:
	#"orderSn": "210123-295424000662898",
	#"bizOrderNo": "5f362fe37733165fd3c3ad8a01ed81f6",
	orderSn = data['result']['orderSn']
	bizOrderNo = data['result']['bizOrderNo']
