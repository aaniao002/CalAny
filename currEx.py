#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import requests
import base64

result={}

# api-endpoint 
URLB64="aHR0cHM6Ly9jY3NhLmVic25ldy5ib2MuY24vQk1QUy9fYmZ3YWpheC5kbz9fbG9jYWxlPXpoX0NO"
URLBytes = base64.b64decode(URLB64)
URL = str(URLBytes, "utf-8")
PARAMS = r'json=%7B%22header%22%3A%7B%22agent%22%3A%22X-ANDR%22%2C%22version%22%3A%221.0.0%22%2C%22device%22%3A%22aPhone%22%2C%22platform%22%3A%22android%22%2C%22plugins%22%3A%225%22%2C%22page%22%3A%226%22%2C%22local%22%3A%22zh_CN%22%2C%22uuid%22%3A%2215833315211599819%22%2C%22ext%22%3A%228%22%2C%22cipherType%22%3A%221%22%7D%2C%22method%22%3A%22PsnGetAllExchangeRatesOutlay%22%2C%22params%22%3A%7B%22ibknum%22%3A%2247504%22%2C%22offerType%22%3A%22R%22%2C%22paritiesType%22%3A%22F%22%2C%22openId_log%22%3A%22%22%2C%22pubId_log%22%3A%22%22%7D%7D'
r = requests.get(url = URL, params = PARAMS) 
result=r.json()

if "result" not in result:
	print("[ERROR] cannot get data in currEx module")
	exit()
# result["result"][0]["sourceCurrency"]["i18nId"] 
result=result["result"]


# build data
data=[]
for i in result:
	srctmp=(""+i["sourceCurrency"]["i18nId"]).lower()
	destmp=(""+i["targetCurrency"]["i18nId"]).lower()
	buyRatetmp=i["buyRate"]
	sellRatetmp=i["sellRate"]
	data.append(
		{"src": srctmp, 
		"des":destmp, 
		"buyRate": buyRatetmp, 
		"sellRate": sellRatetmp}
	)
	codetmp="""
def cal_{0}_{1}(md):
	md.d=float(md.d)*{2}
	return md

def cal_{1}_{0}(md):
	md.d=float(md.d)/float({3})
	return md
""".format(
	srctmp, destmp,
	buyRatetmp, sellRatetmp
)
	exec(codetmp)
	print(codetmp)
	# if (srctmp=="usd" and destmp=="hkd") or (srctmp=="hkd" and destmp=="usd"):
	# 	print(codetmp)


# def cal_usd_cny(md):
#         md.d=float(md.d)*6.9
#         return md

# def cal_cny_usd(md):
#         md.d=float(md.d)/float(6.9)
#         return md



"""
def cal_usd_hkd(md):
        md.d=float(md.d)*7.76298
        return md

def cal_hkd_usd(md):
        md.d=float(md.d)/float(7.78222)
        return md
"""






