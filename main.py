# General
from my_class import BinanceAPIClass

from pprint import pprint

"""
import config_api
from binance.client import Client
_binance_client_obj = Client(config_api.API_KEY, config_api.API_SECRET)
pprint(_binance_client_obj.get_avg_price(symbol='BNBBTC'))
exit(0)
"""

# Prepare
_symbol_first   = 'ADA'
_symbol_second  = 'BTC'
_symbol         = f"{_symbol_first}{_symbol_second}"
_what_fee       = 'taker'
_what_bal       = 'buy'
_size           = 100

#_binance_client_obj = BinanceAPIClass()
_binance_client_obj = BinanceAPIClass(_symbol_first, _symbol_second, _size)

"""""""""""""""""""""
General Endpoints
"""""""""""""""""""""
#_out = _binance_client_obj.get_avg_price('BTCUSDT')

"""""""""""""""""""""
Account Endpoints
"""""""""""""""""""""


_out = _binance_client_obj.get_my_wallet_balance()

# Print My Wallet
if _out[0] == 'OK':
    
    _binance_client_obj.print_my_wallet_balance_result(_out[1])
    
elif _out[0] == 'NOK':
    
    print(f"NOK {_out[1]}")


"""
_out = my_class.create_order_spot_market('market', 'sell', _symbol_first, _symbol_second, _size)

if _out[0] == 'OK':
    pprint(f"OK {_out[1]}")
elif _out[0] == 'NOK':
    print(f"NOK {_out[1]}")
"""
