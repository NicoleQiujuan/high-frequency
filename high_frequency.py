#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time

from kumex.client import Trade, Market


class Hf(object):

    def __init__(self):
        # read configuration from json file
        with open('config.json', 'r') as file:
            config = json.load(file)

        self.api_key = config['api_key']
        self.api_secret = config['api_secret']
        self.api_passphrase = config['api_passphrase']
        self.sandbox = config['is_sandbox']
        self.symbol_a = config['symbol_a']
        self.symbol_b = config['symbol_b']
        self.spread_mean = int(config['spread_mean'])
        self.leverage = config['leverage']
        self.size = int(config['size'])
        self.num_param = int(config['num_param'])
        self.trade = Trade(self.api_key, self.api_secret, self.api_passphrase, is_sandbox=self.sandbox)
        self.market = Market(self.api_key, self.api_secret, self.api_passphrase, is_sandbox=self.sandbox)

    def get_symbol_price(self, symbol):
        ticker = self.market.get_ticker(symbol)
        return float(ticker['price'])


if __name__ == '__main__':
    hf = Hf()
    while 1:
        # ticker of symbols
        price_af = hf.get_symbol_price(hf.symbol_a)
        price_bf = hf.get_symbol_price(hf.symbol_b)
        # position of symbols
        position_a = hf.trade.get_position_details(hf.symbol_a)
        position_a_qty = int(position_a['currentQty'])
        position_b = hf.trade.get_position_details(hf.symbol_b)
        position_b_qty = int(position_b['currentQty'])
        # interval of price
        new_spread = price_af - price_bf
        print('new_spread =', new_spread)

        if position_a_qty == position_b_qty == 0 and new_spread < (hf.spread_mean - hf.num_param):
            buy_order = hf.trade.create_limit_order(hf.symbol_a, 'buy', hf.leverage, hf.size, price_af + 1)
            print('buy %s,order id =%s' % (hf.symbol_a, buy_order['orderId']))
            sell_order = hf.trade.create_limit_order(hf.symbol_b, 'sell', hf.leverage, hf.size, price_bf - 1)
            print('sell %s,order id =%s' % (hf.symbol_b, sell_order['orderId']))
        elif position_a_qty == position_b_qty == 0 and new_spread > (hf.spread_mean + hf.num_param):
            buy_order = hf.trade.create_limit_order(hf.symbol_a, 'sell', hf.leverage, hf.size, price_af - 1)
            print('sell %s,order id =%s' % (hf.symbol_a, buy_order['orderId']))
            sell_order = hf.trade.create_limit_order(hf.symbol_b, 'buy', hf.leverage, hf.size, price_bf + 1)
            print('buy %s,order id =%s' % (hf.symbol_b, sell_order['orderId']))
        elif position_a_qty > 0 and position_b_qty < 0 and new_spread > hf.spread_mean:
            buy_order = hf.trade.create_limit_order(hf.symbol_a, 'sell', position_a['realLeverage'],
                                                    position_a_qty, price_af + 1)
            print('sell %s,order id =%s' % (hf.symbol_a, buy_order['orderId']))
            sell_order = hf.trade.create_limit_order(hf.symbol_b, 'buy', position_a['realLeverage'],
                                                     position_a_qty, price_bf - 1)
            print('buy %s,order id =%s' % (hf.symbol_b, sell_order['orderId']))
        elif position_a_qty < 0 and position_b_qty > 0 and new_spread < hf.spread_mean:
            buy_order = hf.trade.create_limit_order(hf.symbol_a, 'buy', position_a['realLeverage'],
                                                    position_a_qty, price_af - 1)
            print('buy %s,order id =%s' % (hf.symbol_a, buy_order['orderId']))
            sell_order = hf.trade.create_limit_order(hf.symbol_b, 'sell', position_a['realLeverage'],
                                                     position_a_qty, price_bf + 1)
            print('sell %s,order id =%s' % (hf.symbol_b, sell_order['orderId']))

        time.sleep(60)

