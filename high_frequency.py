#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time

from kumex.client import Trade, Market

# read configuration from json file
with open('config.json', 'r') as file:
    config = json.load(file)


api_key = config['api_key']
api_secret = config['api_secret']
api_passphrase = config['api_passphrase']
symbol_a = config['symbol_a']
symbol_b = config['symbol_b']
spread_mean = int(config['spread_mean'])
leverage = int(config['leverage'])
size = int(config['size'])
sandbox = config['is_sandbox']
num_param = int(config['num_param'])
trade = Trade(api_key, api_secret, api_passphrase, is_sandbox=sandbox)
market = Market(api_key, api_secret, api_passphrase, is_sandbox=sandbox)

while 1:
    time.sleep(60)
    # ticker of symbols
    price_a = market.get_ticker(symbol_a)
    price_af = float(price_a['price'])
    price_b = market.get_ticker(symbol_b)
    price_bf = float(price_b['price'])
    # position of symbols
    position_a = trade.get_position_details(symbol_a)
    position_b = trade.get_position_details(symbol_b)
    # interval of price
    new_spread = price_af - price_bf
    print('new_spread =', new_spread)

    if position_a['currentQty'] == position_b['currentQty'] == 0 and new_spread < (spread_mean - num_param):
        buy_order = trade.create_limit_order(symbol_a, 'buy', leverage, size, price_af + 1)
        print('buy %s,order id =%s' % (symbol_a, buy_order['orderId']))
        sell_order = trade.create_limit_order(symbol_b, 'sell', leverage, size, price_bf - 1)
        print('sell %s,order id =%s' % (symbol_b, sell_order['orderId']))
    elif position_a['currentQty'] == position_b['currentQty'] == 0 and new_spread > (spread_mean + num_param):
        buy_order = trade.create_limit_order(symbol_a, 'sell', leverage, size, price_af - 1)
        print('sell %s,order id =%s' % (symbol_a, buy_order['orderId']))
        sell_order = trade.create_limit_order(symbol_b, 'buy', leverage, size, price_bf + 1)
        print('buy %s,order id =%s' % (symbol_b, sell_order['orderId']))
    elif position_a['currentQty'] > 0 and position_b['currentQty'] < 0 and new_spread > spread_mean:
        buy_order = trade.create_limit_order(symbol_a, 'sell', position_a['realLeverage'],
                                             position_a['currentQty'], price_af + 1)
        print('sell %s,order id =%s' % (symbol_a, buy_order['orderId']))
        sell_order = trade.create_limit_order(symbol_b, 'buy', position_a['realLeverage'],
                                              position_a['currentQty'], price_bf - 1)
        print('buy %s,order id =%s' % (symbol_b, sell_order['orderId']))
    elif position_a['currentQty'] < 0 and position_b['currentQty'] > 0 and new_spread < spread_mean:
        buy_order = trade.create_limit_order(symbol_a, 'buy', position_a['realLeverage'],
                                             position_a['currentQty'], price_af - 1)
        print('buy %s,order id =%s' % (symbol_a, buy_order['orderId']))
        sell_order = trade.create_limit_order(symbol_b, 'sell', position_a['realLeverage'],
                                              position_a['currentQty'], price_bf + 1)
        print('sell %s,order id =%s' % (symbol_b, sell_order['orderId']))

