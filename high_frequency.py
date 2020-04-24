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
spread_mean = config['spread_mean']
leverage = config['leverage']
size = config['size']
sandbox = config['is_sandbox']
num_param = config['num_param']
trade = Trade(api_key, api_secret, api_passphrase, is_sandbox=sandbox)
market = Market(api_key, api_secret, api_passphrase, is_sandbox=sandbox)

while 1:
    time.sleep(60)
    # ticker of symbols
    price_a = market.get_ticker(symbol_a)
    price_b = market.get_ticker(symbol_b)
    # position of symbols
    position_a = trade.get_position_details(symbol_a)
    position_b = trade.get_position_details(symbol_b)
    # interval of price
    new_spread = float(price_a['price']) - float(price_b['price'])
    print('new_spread =', new_spread)

    if position_a['currentQty'] == position_b['currentQty'] == 0 and new_spread < (spread_mean - num_param):
        buy_order = trade.create_limit_order(symbol_a, 'buy', leverage, size, price_a['price'] + 1)
        print('buy %s,order id =%s' % (symbol_a, buy_order['orderId']))
        sell_order = trade.create_limit_order(symbol_b, 'sell', leverage, size, price_b['price'] - 1)
        print('sell %s,order id =%s' % (symbol_b, sell_order['orderId']))
    elif position_a['currentQty'] == position_b['currentQty'] == 0 and new_spread > (spread_mean + num_param):
        buy_order = trade.create_limit_order(symbol_a, 'sell', leverage, size, price_a['price'] - 1)
        print('sell %s,order id =%s' % (symbol_a, buy_order['orderId']))
        sell_order = trade.create_limit_order(symbol_b, 'buy', leverage, size, price_b['price'] + 1)
        print('buy %s,order id =%s' % (symbol_b, sell_order['orderId']))
    elif position_a['currentQty'] > 0 and position_b['currentQty'] < 0 and new_spread > spread_mean:
        buy_order = trade.create_limit_order(symbol_a, 'sell', position_a['realLeverage'],
                                             position_a['currentQty'], price_a['price'] + 1)
        print('sell %s,order id =%s' % (symbol_a, buy_order['orderId']))
        sell_order = trade.create_limit_order(symbol_b, 'buy', position_a['realLeverage'],
                                              position_a['currentQty'], price_b['price'] - 1)
        print('buy %s,order id =%s' % (symbol_b, sell_order['orderId']))
    elif position_a['currentQty'] < 0 and position_b['currentQty'] > 0 and new_spread < spread_mean:
        buy_order = trade.create_limit_order(symbol_a, 'buy', position_a['realLeverage'],
                                             position_a['currentQty'], price_a['price'] - 1)
        print('buy %s,order id =%s' % (symbol_a, buy_order['orderId']))
        sell_order = trade.create_limit_order(symbol_b, 'sell', position_a['realLeverage'],
                                              position_a['currentQty'], price_b['price'] + 1)
        print('sell %s,order id =%s' % (symbol_b, sell_order['orderId']))

