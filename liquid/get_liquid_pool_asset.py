#!/usr/bin/python3
import json
from datetime import datetime
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *

poolDesc = [[2, "BUSDUSDT", ["BUSD", "USDT"], False],
            [3, "BUSDDAI",  ["DAI",  "BUSD"],  True],
            [4, "USDTDAI",  ["DAI",  "USDT"],  True],
            [5, "USDCUSDT", ["USDC", "USDT"], False]]

info = open("liquid/info.csv", "a")
no_price_info = open("liquid/no_price_info.csv", "a")
    
request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
with open('liquid/cost.conf') as json_file:
        cost = json.load(json_file)

now = datetime.now().strftime("%D %H:%M")
info.write("{},".format(now))
all_pool_sum = 0.0
all_pool_cost =0.0

no_price_info.write("{},".format(now))
no_price_all_pool_sum = 0.0

for pool, sym, ass, inv in poolDesc:
    price = request_client.get_price_ticker(symbol=sym).price
    if inv:
        price = 1 / price;
    asset = request_client.get_liquid_swap_info(poolId=pool).asset
    print(asset, price)
    total = float(asset[ass[0]]) * price + float(asset[ass[1]])
    pool_cost = cost[sym]
    earn = total - pool_cost
    earn_percent = earn / pool_cost
    all_pool_sum += total
    all_pool_cost += pool_cost
    print("pool{}: {} {}, earn:{}({})".format(pool, total, ass[1], earn, earn_percent))
    info.write("{:.4f}({:.4%}),".format(earn, earn_percent))

    no_price_total = float(asset[ass[0]]) + float(asset[ass[1]])
    no_price_earn = no_price_total - pool_cost
    no_price_earn_percent = no_price_earn / pool_cost
    no_price_all_pool_sum += no_price_total
    print("no_price pool{}: {} {}, earn:{}({})".format(pool, no_price_total, ass[1], no_price_earn, no_price_earn_percent))
    no_price_info.write("{:.4f}({:.4%}),".format(no_price_earn, no_price_earn_percent))

all_pool_earn = all_pool_sum - all_pool_cost
all_pool_earn_percent = all_pool_earn / all_pool_cost
info.write("{:.4f}({:.4%}),".format(all_pool_earn, all_pool_earn_percent))
info.write("\n")
info.close()

no_price_all_pool_earn = no_price_all_pool_sum - all_pool_cost
no_price_all_pool_earn_percent = no_price_all_pool_earn / all_pool_cost
no_price_info.write("{:.4f}({:.4%}),".format(no_price_all_pool_earn, no_price_all_pool_earn_percent))
no_price_info.write("\n")
no_price_info.close()
