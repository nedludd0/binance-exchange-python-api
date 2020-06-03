"""
https://python-binance.readthedocs.io/en/latest/index.html#quick-start
"""

# General
from my_class import BinanceAPIClass

from pprint import pprint

"""
import config_api
from binance.client import Client
_binance_client_obj = Client(config_api.API_KEY, config_api.API_SECRET)
"""

# Prepare
_symbol_first   = 'ADA'
_symbol_second  = 'BTC'
_what_fee       = 'taker'
_what_bal       = 'buy'
_size           = 100

_binance_client_obj = BinanceAPIClass()
#_binance_client_obj = BinanceAPIClass(_size, _symbol_first, _symbol_second)

#print(f'{my_class.get_quantity_to_buy(_symbol_first, _symbol_second, _what_fee, _size ):.20f}')


#pprint(_binance_client_obj.get_trade_fee(symbol=_symbol))

#_out = my_class.get_my_wallet_balance(_binance_client_obj)

"""
_out = my_class.get_my_quantity_to_buy(_binance_client_obj,_symbol_first, _symbol_second, _what_fee, _size=100)
"""

    
_out = _binance_client_obj.get_rate_limits()

if _out[0] == 'OK':
    print(f"OK {_out[1]}")
elif _out[0] == 'NOK':
    print(f"NOK {_out[1]}")


"""""""""""""""""""""
General Endpoints
"""""""""""""""""""""

# get market depth
#depth = _binance_client_obj.get_order_book(symbol='BNBBTC')


"""""""""""""""""""""
Account Endpoints
"""""""""""""""""""""

#balance = _binance_client_obj.get_asset_balance(asset='USDT')

"""
_user_balance = my_class.get_tg_user_balance()

pprint(_user_balance)
"""

"""
_out = my_class.create_order_spot_market('market', 'sell', _symbol_first, _symbol_second, _size)

if _out[0] == 'OK':
    pprint(f"OK {_out[1]}")
elif _out[0] == 'NOK':
    print(f"NOK {_out[1]}")
"""
