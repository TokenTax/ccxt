# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.huobipro import huobipro

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable


class cointiger (huobipro):

    def describe(self):
        return self.deep_extend(super(cointiger, self).describe(), {
            'id': 'cointiger',
            'name': 'CoinTiger',
            'countries': ['CN'],
            'hostname': 'cointiger.pro',
            'has': {
                'fetchCurrencies': False,
                'fetchTickers': True,
                'fetchTradingLimits': False,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchOrderTrades': False,  # not tested yet
                'cancelOrders': True,
            },
            'headers': {
                'Language': 'en_US',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/39797261-d58df196-5363-11e8-9880-2ec78ec5bd25.jpg',
                'api': {
                    'public': 'https://api.{hostname}/exchange/trading/api/market',
                    'private': 'https://api.{hostname}/exchange/trading/api',
                    'exchange': 'https://www.{hostname}/exchange',
                    'v2public': 'https://api.{hostname}/exchange/trading/api/v2',
                    'v2': 'https://api.{hostname}/exchange/trading/api/v2',
                },
                'www': 'https://www.cointiger.pro',
                'referral': 'https://www.cointiger.pro/exchange/register.html?refCode=FfvDtt',
                'doc': 'https://github.com/cointiger/api-docs-en/wiki',
            },
            'api': {
                'v2public': {
                    'get': [
                        'timestamp',
                        'currencys',
                    ],
                },
                'v2': {
                    'get': [
                        'order/orders',
                        'order/match_results',
                        'order/make_detail',
                        'order/details',
                    ],
                    'post': [
                        'order',
                        'order/batch_cancel',
                    ],
                },
                'public': {
                    'get': [
                        'history/kline',  # 获取K线数据
                        'detail/merged',  # 获取聚合行情(Ticker)
                        'depth',  # 获取 Market Depth 数据
                        'trade',  # 获取 Trade Detail 数据
                        'history/trade',  # 批量获取最近的交易记录
                        'detail',  # 获取 Market Detail 24小时成交量数据
                    ],
                },
                'exchange': {
                    'get': [
                        'footer/tradingrule.html',
                        'api/public/market/detail',
                    ],
                },
                'private': {
                    'get': [
                        'user/balance',
                        'order/new',
                        'order/history',
                        'order/trade',
                    ],
                    'post': [
                        'order',
                    ],
                    'delete': [
                        'order',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0.0008,
                    'taker': 0.0015,
                },
            },
            'exceptions': {
                #    {"code":"1","msg":"系统错误","data":null}
                #    {"code":"1","msg":"Balance insufficient,余额不足","data":null}
                '1': ExchangeError,
                '2': BadRequest,  # {"code":"2","msg":"Parameter error","data":null}
                '5': InvalidOrder,
                '6': InvalidOrder,
                '8': OrderNotFound,
                '16': AuthenticationError,  # funding password not set
                '100001': ExchangeError,
                '100002': ExchangeNotAvailable,
                '100003': ExchangeError,
                '100005': AuthenticationError,
                '110030': DDoSProtection,
            },
            'commonCurrencies': {
                'FGC': 'FoundGameCoin',
                'TCT': 'The Tycoon Chain Token',
            },
        })

    def fetch_markets(self, params={}):
        response = self.v2publicGetCurrencys()
        #
        #     {
        #         code: '0',
        #         msg: 'suc',
        #         data: {
        #             'bitcny-partition': [
        #                 {
        #                     baseCurrency: 'btc',
        #                     quoteCurrency: 'bitcny',
        #                     pricePrecision: 2,
        #                     amountPrecision: 4,
        #                     withdrawFeeMin: 0.0005,
        #                     withdrawFeeMax: 0.005,
        #                     withdrawOneMin: 0.01,
        #                     withdrawOneMax: 10,
        #                     depthSelect: {step0: '0.01', step1: '0.1', step2: '1'}
        #                 },
        #                 ...
        #             ],
        #             ...
        #         },
        #     }
        #
        keys = list(response['data'].keys())
        result = []
        for i in range(0, len(keys)):
            key = keys[i]
            partition = response['data'][key]
            for j in range(0, len(partition)):
                market = partition[j]
                baseId = self.safe_string(market, 'baseCurrency')
                quoteId = self.safe_string(market, 'quoteCurrency')
                base = baseId.upper()
                quote = quoteId.upper()
                base = self.common_currency_code(base)
                quote = self.common_currency_code(quote)
                id = baseId + quoteId
                uppercaseId = id.upper()
                symbol = base + '/' + quote
                precision = {
                    'amount': market['amountPrecision'],
                    'price': market['pricePrecision'],
                }
                active = True
                entry = {
                    'id': id,
                    'uppercaseId': uppercaseId,
                    'symbol': symbol,
                    'base': base,
                    'quote': quote,
                    'baseId': baseId,
                    'quoteId': quoteId,
                    'info': market,
                    'active': active,
                    'precision': precision,
                    'limits': {
                        'amount': {
                            'min': math.pow(10, -precision['amount']),
                            'max': None,
                        },
                        'price': {
                            'min': math.pow(10, -precision['price']),
                            'max': None,
                        },
                        'cost': {
                            'min': 0,
                            'max': None,
                        },
                    },
                }
                result.append(entry)
        self.options['marketsByUppercaseId'] = self.index_by(result, 'uppercaseId')
        return result

    def parse_ticker(self, ticker, market=None):
        symbol = None
        if market:
            symbol = market['symbol']
        timestamp = self.safe_integer(ticker, 'id')
        close = self.safe_float(ticker, 'last')
        percentage = self.safe_float(ticker, 'percentChange')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high24hr'),
            'low': self.safe_float(ticker, 'low24hr'),
            'bid': self.safe_float(ticker, 'highestBid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'lowestAsk'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': close,
            'last': close,
            'previousClose': None,
            'change': None,
            'percentage': percentage,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'baseVolume'),
            'quoteVolume': self.safe_float(ticker, 'quoteVolume'),
            'info': ticker,
        }

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetDepth(self.extend({
            'symbol': market['id'],  # self endpoint requires a lowercase market id
            'type': 'step0',
        }, params))
        data = response['data']['depth_data']
        if 'tick' in data:
            if not data['tick']:
                raise ExchangeError(self.id + ' fetchOrderBook() returned empty response: ' + self.json(response))
            orderbook = data['tick']
            timestamp = data['ts']
            return self.parse_order_book(orderbook, timestamp, 'buys')
        raise ExchangeError(self.id + ' fetchOrderBook() returned unrecognized response: ' + self.json(response))

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        marketId = market['uppercaseId']
        response = self.exchangeGetApiPublicMarketDetail(params)
        if not(marketId in list(response.keys())):
            raise ExchangeError(self.id + ' fetchTicker symbol ' + symbol + '(' + marketId + ') not found')
        return self.parse_ticker(response[marketId], market)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.exchangeGetApiPublicMarketDetail(params)
        result = {}
        ids = list(response.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            market = None
            symbol = id
            if id in self.options['marketsByUppercaseId']:
                # self endpoint returns uppercase ids
                symbol = self.options['marketsByUppercaseId'][id]['symbol']
                market = self.options['marketsByUppercaseId'][id]
            result[symbol] = self.parse_ticker(response[id], market)
        return result

    def parse_trade(self, trade, market=None):
        #
        #   {     volume: "0.014",
        #          symbol: "ethbtc",
        #         buy_fee: "0.00001400",
        #         orderId:  32235710,
        #           price: "0.06923825",
        #         created:  1531605169000,
        #              id:  3785005,
        #          source:  1,
        #            type: "buy-limit",
        #     bid_user_id:  326317         }]}
        #
        # --------------------------------------------------------------------
        #
        #     {
        #         "volume": {
        #             "amount": "1.000",
        #             "icon": "",
        #             "title": "成交量"
        #                   },
        #         "price": {
        #             "amount": "0.04978883",
        #             "icon": "",
        #             "title": "委托价格"
        #                  },
        #         "created_at": 1513245134000,
        #         "deal_price": {
        #             "amount": 0.04978883000000000000000000000000,
        #             "icon": "",
        #             "title": "成交价格"
        #                       },
        #         "id": 138
        #     }
        #
        id = self.safe_string(trade, 'id')
        orderId = self.safe_string(trade, 'orderId')
        orderType = self.safe_string(trade, 'type')
        type = None
        side = None
        if orderType is not None:
            parts = orderType.split('-')
            side = parts[0]
            type = parts[1]
        side = self.safe_string(trade, 'side', side)
        amount = None
        price = None
        cost = None
        if side is None:
            price = self.safe_float(trade['price'], 'amount')
            amount = self.safe_float(trade['volume'], 'amount')
            cost = self.safe_float(trade['deal_price'], 'amount')
        else:
            side = side.lower()
            price = self.safe_float(trade, 'price')
            amount = self.safe_float_2(trade, 'amount', 'volume')
        fee = None
        feeCost = self.safe_float(trade, 'fee')
        if feeCost is not None:
            feeCurrency = None
            if market is not None:
                if side == 'buy':
                    feeCurrency = market['base']
                elif side == 'sell':
                    feeCurrency = market['quote']
            fee = {
                'cost': feeCost,
                'currency': feeCurrency,
            }
        if amount is not None:
            if price is not None:
                if cost is None:
                    cost = amount * price
        timestamp = self.safe_integer_2(trade, 'created_at', 'ts')
        timestamp = self.safe_integer_2(trade, 'created', 'mtime', timestamp)
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'info': trade,
            'id': id,
            'order': orderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    def fetch_trades(self, symbol, since=None, limit=1000, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['size'] = limit
        response = self.publicGetHistoryTrade(self.extend(request, params))
        return self.parse_trades(response['data']['trade_data'], market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 100
        response = self.privateGetOrderTrade(self.extend({
            'symbol': market['id'],
            'offset': 1,
            'limit': limit,
        }, params))
        return self.parse_trades(response['data']['list'], market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            ohlcv['id'] * 1000,
            ohlcv['open'],
            ohlcv['high'],
            ohlcv['low'],
            ohlcv['close'],
            ohlcv['vol'],
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=1000, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'period': self.timeframes[timeframe],
        }
        if limit is not None:
            request['size'] = limit
        response = self.publicGetHistoryKline(self.extend(request, params))
        return self.parse_ohlcvs(response['data']['kline_data'], market, timeframe, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetUserBalance(params)
        #
        #     {
        #         "code": "0",
        #         "msg": "suc",
        #         "data": [{
        #             "normal": "1813.01144179",
        #             "lock": "1325.42036785",
        #             "coin": "btc"
        #         }, {
        #             "normal": "9551.96692244",
        #             "lock": "547.06506717",
        #             "coin": "eth"
        #         }]
        #     }
        #
        balances = response['data']
        result = {'info': response}
        for i in range(0, len(balances)):
            balance = balances[i]
            id = balance['coin']
            code = id.upper()
            code = self.common_currency_code(code)
            if id in self.currencies_by_id:
                code = self.currencies_by_id[id]['code']
            account = self.account()
            account['used'] = float(balance['lock'])
            account['free'] = float(balance['normal'])
            account['total'] = self.sum(account['used'], account['free'])
            result[code] = account
        return self.parse_balance(result)

    def fetch_order_trades(self, id, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrderTrades requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'order_id': id,
        }
        response = self.v2GetOrderMakeDetail(self.extend(request, params))
        #
        # the above endpoint often returns an empty array
        #
        #     {code:   "0",
        #        msg:   "suc",
        #       data: [{     volume: "0.014",
        #                      symbol: "ethbtc",
        #                     buy_fee: "0.00001400",
        #                     orderId:  32235710,
        #                       price: "0.06923825",
        #                     created:  1531605169000,
        #                          id:  3785005,
        #                      source:  1,
        #                        type: "buy-limit",
        #                 bid_user_id:  326317         }]}
        #
        return self.parse_trades(response['data'], market, since, limit)

    def fetch_orders_by_status_v1(self, status=None, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 100
        method = 'privateGetOrderNew' if (status == 'open') else 'privateGetOrderHistory'
        response = getattr(self, method)(self.extend({
            'symbol': market['id'],
            'offset': 1,
            'limit': limit,
        }, params))
        orders = response['data']['list']
        result = []
        for i in range(0, len(orders)):
            order = self.extend(orders[i], {
                'status': status,
            })
            result.append(self.parse_order(order, market))
        return result

    def fetch_open_orders_v1(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_status_v1('open', symbol, since, limit, params)

    def fetch_orders_v1(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_status_v1(None, symbol, since, limit, params)

    def fetch_orders_by_states_v2(self, states, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 50
        response = self.v2GetOrderOrders(self.extend({
            'symbol': market['id'],
            # 'types': 'buy-market,sell-market,buy-limit,sell-limit',
            'states': states,  # 'new,part_filled,filled,canceled,expired'
            # 'from': '0',  # id
            'direct': 'next',  # or 'prev'
            'size': limit,
        }, params))
        return self.parse_orders(response['data'], market, since, limit)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_states_v2('new,part_filled,filled,canceled,expired', symbol, since, limit, params)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_states_v2('new,part_filled', symbol, since, limit, params)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_states_v2('filled,canceled', symbol, since, limit, params)

    def fetch_order(self, id, symbol=None, params={}):
        #
        #     {code:   "0",
        #        msg:   "suc",
        #       data: {     symbol: "ethbtc",
        #                       fee: "0.00000200",
        #                 avg_price: "0.06863752",
        #                    source:  1,
        #                      type: "buy-limit",
        #                     mtime:  1531340305000,
        #                    volume: "0.002",
        #                   user_id:  326317,
        #                     price: "0.06863752",
        #                     ctime:  1531340304000,
        #               deal_volume: "0.00200000",
        #                        id:  31920243,
        #                deal_money: "0.00013727",
        #                    status:  2              }}
        #
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'order_id': str(id),
        }
        response = self.v2GetOrderDetails(self.extend(request, params))
        return self.parse_order(response['data'], market)

    def parse_order_status(self, status):
        statuses = {
            '0': 'open',  # pending
            '1': 'open',
            '2': 'closed',
            '3': 'open',
            '4': 'canceled',
            '6': 'error',
        }
        if status in statuses:
            return statuses[status]
        return status

    def parse_order(self, order, market=None):
        #
        #  v1
        #
        #      {
        #            volume: {"amount": "0.054", "icon": "", "title": "volume"},
        #         age_price: {"amount": "0.08377697", "icon": "", "title": "Avg price"},
        #              side: "BUY",
        #             price: {"amount": "0.00000000", "icon": "", "title": "price"},
        #        created_at: 1525569480000,
        #       deal_volume: {"amount": "0.64593598", "icon": "", "title": "Deal volume"},
        #   "remain_volume": {"amount": "1.00000000", "icon": "", "title": "尚未成交"
        #                id: 26834207,
        #             label: {go: "trade", title: "Traded", click: 1},
        #          side_msg: "Buy"
        #      },
        #
        #  v2
        #
        #     {code:   "0",
        #        msg:   "suc",
        #       data: {     symbol: "ethbtc",
        #                       fee: "0.00000200",
        #                 avg_price: "0.06863752",
        #                    source:  1,
        #                      type: "buy-limit",
        #                     mtime:  1531340305000,
        #                    volume: "0.002",
        #                   user_id:  326317,
        #                     price: "0.06863752",
        #                     ctime:  1531340304000,
        #               deal_volume: "0.00200000",
        #                        id:  31920243,
        #                deal_money: "0.00013727",
        #                    status:  2              }}
        #
        id = self.safe_string(order, 'id')
        side = self.safe_string(order, 'side')
        type = None
        orderType = self.safe_string(order, 'type')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        timestamp = self.safe_integer_2(order, 'created_at', 'ctime')
        lastTradeTimestamp = self.safe_integer_2(order, 'mtime', 'finished-at')
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'symbol')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        remaining = None
        amount = None
        filled = None
        price = None
        cost = None
        fee = None
        average = None
        if side is not None:
            side = side.lower()
            amount = self.safe_float(order['volume'], 'amount')
            remaining = self.safe_float(order['remain_volume'], 'amount') if ('remain_volume' in list(order.keys())) else None
            filled = self.safe_float(order['deal_volume'], 'amount') if ('deal_volume' in list(order.keys())) else None
            price = self.safe_float(order['price'], 'amount') if ('price' in list(order.keys())) else None
            average = self.safe_float(order['age_price'], 'amount') if ('age_price' in list(order.keys())) else None
        else:
            if orderType is not None:
                parts = orderType.split('-')
                side = parts[0]
                type = parts[1]
                cost = self.safe_float(order, 'deal_money')
                price = self.safe_float(order, 'price')
                average = self.safe_float(order, 'avg_price')
                amount = self.safe_float_2(order, 'amount', 'volume')
                filled = self.safe_float(order, 'deal_volume')
                feeCost = self.safe_float(order, 'fee')
                if feeCost is not None:
                    feeCurrency = None
                    if market is not None:
                        if side == 'buy':
                            feeCurrency = market['base']
                        elif side == 'sell':
                            feeCurrency = market['quote']
                    fee = {
                        'cost': feeCost,
                        'currency': feeCurrency,
                    }
        if amount is not None:
            if remaining is not None:
                if filled is None:
                    filled = max(0, amount - remaining)
            elif filled is not None:
                cost = filled * price
                if remaining is None:
                    remaining = max(0, amount - filled)
        if status is None:
            if remaining is not None:
                if remaining == 0:
                    status = 'closed'
        result = {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'average': average,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
            'trades': None,
        }
        return result

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        if not self.password:
            raise AuthenticationError(self.id + ' createOrder requires exchange.password to be set to user trading password(not login passwordnot )')
        self.check_required_credentials()
        market = self.market(symbol)
        orderType = 1 if (type == 'limit') else 2
        order = {
            'symbol': market['id'],
            'side': side.upper(),
            'type': orderType,
            'volume': self.amount_to_precision(symbol, amount),
            'capital_password': self.password,
        }
        if (type == 'market') and(side == 'buy'):
            if price is None:
                raise InvalidOrder(self.id + ' createOrder requires price argument for market buy orders to calculate total cost according to exchange rules')
            order['volume'] = self.amount_to_precision(symbol, float(amount) * float(price))
        if type == 'limit':
            order['price'] = self.price_to_precision(symbol, price)
        else:
            if price is None:
                order['price'] = self.price_to_precision(symbol, 0)
            else:
                order['price'] = self.price_to_precision(symbol, price)
        response = self.privatePostOrder(self.extend(order, params))
        #
        #     {"order_id":34343}
        #
        timestamp = self.milliseconds()
        return {
            'info': response,
            'id': str(response['data']['order_id']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'filled': None,
            'remaining': None,
            'cost': None,
            'trades': None,
            'fee': None,
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder requires a symbol argument')
        market = self.market(symbol)
        response = self.privateDeleteOrder(self.extend({
            'symbol': market['id'],
            'order_id': id,
        }, params))
        return {
            'id': id,
            'symbol': symbol,
            'info': response,
        }

    def cancel_orders(self, ids, symbol=None, params={}):
        self.load_markets()
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrders requires a symbol argument')
        market = self.market(symbol)
        marketId = market['id']
        orderIdList = {}
        orderIdList[marketId] = ids
        request = {
            'orderIdList': self.json(orderIdList),
        }
        response = self.v2PostOrderBatchCancel(self.extend(request, params))
        return {
            'info': response,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        self.check_required_credentials()
        url = self.implode_params(self.urls['api'][api], {
            'hostname': self.hostname,
        })
        url += '/' + self.implode_params(path, params)
        if api == 'private' or api == 'v2':
            timestamp = str(self.milliseconds())
            query = self.keysort(self.extend({
                'time': timestamp,
            }, params))
            keys = list(query.keys())
            auth = ''
            for i in range(0, len(keys)):
                auth += keys[i] + str(query[keys[i]])
            auth += self.secret
            signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha512)
            urlParams = {} if (method == 'POST') else query
            url += '?' + self.urlencode(self.keysort(self.extend({
                'api_key': self.apiKey,
                'time': timestamp,
            }, urlParams)))
            url += '&sign=' + signature
            if method == 'POST':
                body = self.urlencode(query)
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
        elif api == 'public' or api == 'v2public':
            url += '?' + self.urlencode(self.extend({
                'api_key': self.apiKey,
            }, params))
        else:
            if params:
                url += '?' + self.urlencode(params)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response):
        if not isinstance(body, basestring):
            return  # fallback to default error handler
        if len(body) < 2:
            return  # fallback to default error handler
        if (body[0] == '{') or (body[0] == '['):
            if 'code' in response:
                #
                #     {"code": "100005", "msg": "request sign illegal", "data": null}
                #
                code = self.safe_string(response, 'code')
                if code is not None:
                    message = self.safe_string(response, 'msg')
                    feedback = self.id + ' ' + self.json(response)
                    if code != '0':
                        exceptions = self.exceptions
                        if code in exceptions:
                            if code == '1':
                                #
                                #    {"code":"1","msg":"系统错误","data":null}
                                #    {“code”:“1",“msg”:“Balance insufficient,余额不足“,”data”:null}
                                #
                                if message.find('Balance insufficient') >= 0:
                                    raise InsufficientFunds(feedback)
                            elif code == '2':
                                if message == 'offsetNot Null':
                                    raise ExchangeError(feedback)
                                elif message == 'api_keyNot EXIST':
                                    raise AuthenticationError(feedback)
                                elif message == 'price precision exceed the limit':
                                    raise InvalidOrder(feedback)
                                elif message == 'Parameter error':
                                    raise BadRequest(feedback)
                            raise exceptions[code](feedback)
                        else:
                            raise ExchangeError(self.id + ' unknown "error" value: ' + self.json(response))
                    else:
                        #
                        # Google Translate:
                        # 订单状态不能取消,订单取消失败 = Order status cannot be canceled
                        # 根据订单号没有查询到订单,订单取消失败 = The order was not queried according to the order number
                        #
                        # {"code":"0","msg":"suc","data":{"success":[],"failed":[{"err-msg":"订单状态不能取消,订单取消失败","order-id":32857051,"err-code":"8"}]}}
                        # {"code":"0","msg":"suc","data":{"success":[],"failed":[{"err-msg":"Parameter error","order-id":32857050,"err-code":"2"},{"err-msg":"订单状态不能取消,订单取消失败","order-id":32857050,"err-code":"8"}]}}
                        # {"code":"0","msg":"suc","data":{"success":[],"failed":[{"err-msg":"Parameter error","order-id":98549677,"err-code":"2"},{"err-msg":"根据订单号没有查询到订单,订单取消失败","order-id":98549677,"err-code":"8"}]}}
                        #
                        if feedback.find('订单状态不能取消,订单取消失败') >= 0:
                            if feedback.find('Parameter error') >= 0:
                                raise OrderNotFound(feedback)
                            else:
                                raise InvalidOrder(feedback)
                        elif feedback.find('根据订单号没有查询到订单,订单取消失败') >= 0:
                            raise OrderNotFound(feedback)
