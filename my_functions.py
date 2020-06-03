from datetime import datetime as dt
from pprint import pprint

from decimal import getcontext, ROUND_DOWN, Decimal
import math
import traceback

import config_env
from binance.client import Client, BinanceAPIException


"""
def my_log(_msg):
    import logging
    import sys
    
    # Create a custom logger
    logger = logging.getLogger(__name__)
    
    # Create handlers
    c_handler = logging.StreamHandler(sys.stdout)
    
    # Create formatters and add it to handlers
    c_format = logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s %(funcName)s - %(message)s')
    
    # Set Formatter
    c_handler.setFormatter(c_format)
    
    # Add handlers to the logger
    logger.addHandler(c_handler)
    
    logger.error(_msg)
"""
    
def my_log(_type,_func,_inputs,_msg):

    if _inputs is not None:
        _msg_error = f"{_type} on function {_func} with inputs {_inputs} --> MSG {_msg}"
    else:
        _msg_error = f"{_type} on function {_func} --> MSG {_msg}"
        
    return(_msg_error)
    

"""""""""""""""""""""
Binance Base Functions
"""""""""""""""""""""
# Get Binance Rate Limits
def get_rate_limits():
    
    # Prepare
    _response_tuple = None
    _rate_limits    = None
    _exchange_info  = None
    _output_verbose = {}
    _inputs         = None
    
    try:

        _exchange_info  = _binance_client_obj.get_exchange_info()
        
        if _exchange_info is not None:
        
            _rate_limits    = _exchange_info.get('rateLimits')
            
            if _rate_limits is not None:
                for _rate_limit in _rate_limits:
                    
                    if _rate_limit.get('rateLimitType') == 'REQUEST_WEIGHT':
                        
                        _key                    = f"Max Requests for {_rate_limit.get('intervalNum')} {_rate_limit.get('interval').lower().capitalize()}"
                        _output_verbose[_key]   = _rate_limit.get('limit')
                        
                    elif _rate_limit.get('rateLimitType') == 'ORDERS' and _rate_limit.get('interval') == 'SECOND':
                        
                        _key                    = f"Max Orders for {_rate_limit.get('intervalNum')} {_rate_limit.get('interval').lower().capitalize()}"
                        _output_verbose[_key]   = _rate_limit.get('limit')
                    
                    elif _rate_limit.get('rateLimitType') == 'ORDERS' and _rate_limit.get('interval')== 'DAY':
                        
                        _key                    = f"Max Orders for {_rate_limit.get('intervalNum')} {_rate_limit.get('interval').lower().capitalize()}"
                        _output_verbose[_key]   = _rate_limit.get('limit')
                    
                    _response_tuple = ('OK', _output_verbose)
                    
            else:
                _response_tuple = ('NOK',  f"{ my_log('Error','get_rate_limits',_inputs,'_rate_limits is None')}")
                
        else:
            _response_tuple = ('NOK',  f"{ my_log('Error','get_rate_limits',_inputs,'_exchange_info is None')}")
        
    except Exception as e:
        _response_tuple = ('NOK',  f"{ my_log('Exception','get_rate_limits',_inputs,traceback.format_exc(2))}")
    
    return(_response_tuple)
    
# Get My Wallet Balance
def get_my_wallet_balance(_binance_client_obj):
    
    # Prepare
    _response_tuple = None
    _my_wallet      = []
    _my_asset       = {}
    _place          = 0
    _account        = None
    _inputs         = None
    
    try:
        _account = _binance_client_obj.get_account()

        # Costruisco il Wallet, cioè un dict con gli asset > 0 posseduti 
        if "balances" in _account:
            for bal in _account['balances']:
                if float(bal.get('free')) > 0.00000000:
                    _my_asset = {'Asset' : bal.get('asset') , 'Amount Free' : bal.get('free'), 'Amount Locked' : bal.get('locked')}
                    _my_wallet.insert( _place, _my_asset )       
                    _place = _place+1
                    
            _response_tuple = ('OK', _my_wallet)
            
        else:
            _response_tuple = ('NOK',  f"{ my_log('Error','get_wallet_balance',_inputs,'balances not in _account')}")
    
    except Exception as e:
        _response_tuple = ('NOK',  f"{ my_log('Exception','get_wallet_balance',_inputs,traceback.format_exc(2))}")
            
    return(_response_tuple)

# Get Symbol Info LOT_SIZE
def get_symbol_info_filter_LOT_SIZE(_binance_client_obj,_symbol):
    
    # Prepare
    _response_tuple     = None
    _symbol_info        = None    
    _output_lot_size    = {}
    _inputs             = _symbol
    
    try:
        _symbol_info = _binance_client_obj.get_symbol_info(_symbol)
        
        if _symbol_info is not None:
            
            filters = _symbol_info.get('filters')
        
            if filters is not None:
                
                for f in filters:
                    
                    if f.get('filterType') == 'LOT_SIZE':
                        _output_lot_size["LOT_SIZE_symbol"]     = _symbol
                        _output_lot_size["LOT_SIZE_maxQty"]     = Decimal(f.get('maxQty'))
                        _output_lot_size["LOT_SIZE_minQty"]     = Decimal(f.get('minQty'))
                        _output_lot_size["LOT_SIZE_step_size"]  = Decimal(f.get('stepSize'))
                        _response_tuple                         = ('OK', _output_lot_size)
                        break
            
            else:
                _response_tuple = ('NOK',  f"{ my_log('Error','get_symbol_info_filter_LOT_SIZE',_inputs,'filters is None')}")
            
        else:
            _response_tuple = ('NOK',  f"{ my_log('Error','get_symbol_info_filter_LOT_SIZE',_inputs,'_symbol_info is None')}")
        
    except Exception as e:
        _response_tuple = ('NOK',  f"{ my_log('Exception','get_symbol_info_filter_LOT_SIZE',_inputs,traceback.format_exc(2))}")
            
    return(_response_tuple)

# Get Symbol Fee Cost
# https://binance.zendesk.com/hc/en-us/articles/360007720071-Maker-vs-Taker
def get_fee_cost(_binance_client_obj,_symbol, _what='taker'):
    
    # Prepare
    _response_tuple     = None    
    _fee                = None
    _trade_fee_response = None
    _inputs             = f"{_symbol}|{_what}"
    
    try:
        _trade_fee_response = _binance_client_obj.get_trade_fee(symbol=_symbol)
        
        if _trade_fee_response is not None:
            if (_trade_fee_response.get('success')):
                _trade_fee = _binance_client_obj.get_trade_fee(symbol=_symbol).get('tradeFee')
                if bool(_trade_fee): # Checking if dictionary _trade_fee is empty
                    for t in _trade_fee:
                        if t.get('symbol') == _symbol:
                            if _what == 'taker':
                                _fee = Decimal(t.get('taker'))
                            elif _what == 'maker':
                                _fee = Decimal(t.get('maker'))
                            else:
                                _response_tuple = ('NOK',  f"{ my_log('Error','get_fee_cost',_inputs,'_what unknown')}")
                                return(_response_tuple)
                                
                            _response_tuple = ('OK', _fee)
                else:
                    _response_tuple = ('NOK',  f"{ my_log('Error','get_fee_cost',_inputs,'_trade_fee is Empty')}")
            else:
                _response_tuple = ('NOK',  f"{ my_log('Error','get_fee_cost',_inputs,'_trade_fee insuccess')}")
        else:
            _response_tuple = ('NOK',  f"{ my_log('Error','get_fee_cost',_inputs,'_trade_fee_response is None')}")
        
    except Exception as e:
        _response_tuple = ('NOK',  f"{ my_log('Exception','get_fee_cost',_inputs,traceback.format_exc(2))}")

    return(_response_tuple)
    
# Get Prezzo medio degli ultimi 5 minuti
def get_avg_price(_binance_client_obj,_symbol):

    # Prepare
    _response_tuple     = None    
    _price              = None
    _avg_price_response = None
    _inputs             = _symbol
    
    try:
        _avg_price_response = _binance_client_obj.get_avg_price(symbol=_symbol)
    
        if _avg_price_response is not None:
            _price = Decimal(_avg_price_response.get('price'))
            _response_tuple = ('OK', _price)
        else:
            _response_tuple = ('NOK',  f"{ my_log('Error','get_avg_price',_inputs,'_avg_price_response is None')}")            
            
    except Exception as e:
        _response_tuple = ('NOK',  f"{ my_log('Exception','get_avg_price',_inputs,traceback.format_exc(2))}")

    return(_response_tuple)

# Get Asset Free
def get_my_asset_balance(_binance_client_obj,_symbol_first, _symbol_second, _what = 'buy'):
    
    # Prepare
    _response_tuple         = None    
    _asset_balance_response = None
    _bal                    = None
    _my_asset               = None
    _inputs                 = f"{_symbol_first}|{_symbol_second}|{_what}"
    
    if _what == 'buy':
        _my_asset = _symbol_second
    elif _what == 'sell':
        _my_asset = _symbol_first
    else:
        _response_tuple = ('NOK',  f"{ my_log('Error','get_my_asset_balance',_inputs,'_what unknown')}")
        return(_response_tuple)
        
    try:
        _asset_balance_response = _binance_client_obj.get_asset_balance(asset=_my_asset)
    
        if _asset_balance_response is not None:
            _bal = Decimal(_asset_balance_response.get('free'))
            _response_tuple = ('OK', _bal)
        else:
            _response_tuple = ('NOK',  f"{ my_log('Error','get_my_asset_balance',_inputs,'_asset_balance_response is None')}")
            
    except Exception as e:
        _response_tuple = ('NOK',  f"{ my_log('Exception','get_my_asset_balance',_inputs,traceback.format_exc(2))}")

    return(_response_tuple)

# Tronco _tot_start al più grande multimo di _step_size
def truncate_by_step_size(_tot_start, _step_size):
    
    # Prepare
    _response_tuple     = None
    _digits_decimal     = None
    _tot_start_decimal  = Decimal(_tot_start)
    _tot_end            = None
    _inputs             = f"{_tot_start}|{_step_size}"
    
    # Calculate Digits
    try:
        _digits_decimal = int( round( -math.log(_step_size, 10) , 0 ) )
    except Exception as e:
        _response_tuple = ('NOK',  f"{ my_log('Exception','truncate_by_step_size',_inputs,traceback.format_exc(2))}")
        return(_response_tuple)
         
    # By default rounding setting in python is ROUND_HALF_EVEN
    getcontext().rounding = ROUND_DOWN
    
    # Calculate Tot End
    try:
        _tot_end = round( _tot_start_decimal , _digits_decimal )
        _response_tuple = ('OK',_tot_end)
    except Exception as e:
        _response_tuple = ('NOK',  f"{ my_log('Exception','truncate_by_step_size',_inputs,traceback.format_exc(2))}")
    
    return(_response_tuple)
    
# Calculate exact Quantity to BUY
def get_my_quantity_to_buy(_binance_client_obj,_symbol_first, _symbol_second, _what_fee, _size=100):
    
    # Prepate
    _symbol                 = f"{_symbol_first}{_symbol_second}".upper()
    _response_tuple         = None
    _inputs                 = f"{_symbol_first}|{_symbol_second}|{_what_fee}|{_size}"
    
    symbol_bal_second       = None
    symbol_step_size        = None
    symbol_fee              = None
    symbol_avg_price        = None
    symbol_bal_second_size  = None
    symbol_fee_perc         = None
    quantity_start          = None
    quantity_end            = None
    
    # Get Owned Asset Balance
    _symbol_bal_second  = get_my_asset_balance(_binance_client_obj,_symbol_first, _symbol_second, 'buy')
    
    # Get Symbol Step Size
    if _symbol_bal_second[0] == 'OK':
        _symbol_step_size = get_symbol_info_filter_LOT_SIZE(_binance_client_obj,_symbol)
    else:
        _response_tuple = ('NOK',  f"{ my_log('Error','get_my_quantity_to_buy',_inputs,_symbol_bal_second[1])}")
        return(_response_tuple)
    
    # Get Symbol Fee Cost
    if _symbol_step_size[0] == 'OK':
        _symbol_fee = get_fee_cost(_binance_client_obj,_symbol, _what_fee)
    else:
        _response_tuple = ('NOK',  f"{ my_log('Error','get_my_quantity_to_buy',_inputs,_symbol_step_size[1])}")
        return(_response_tuple)
    
    # Get Symbol Avg Price
    if _symbol_fee[0] == 'OK':
        _symbol_avg_price = get_avg_price(_binance_client_obj,_symbol)
    else:
        _response_tuple = ('NOK',  f"{ my_log('Error','get_my_quantity_to_buy',_inputs,_symbol_fee[1])}")
        return(_response_tuple)
    
    # Calculate Quantity End
    if _symbol_avg_price[0] == 'OK':
        
        symbol_bal_second   = _symbol_bal_second[1]
        symbol_step_size    = _symbol_step_size[1].get('LOT_SIZE_step_size')
        symbol_fee          = _symbol_fee[1]        
        symbol_avg_price    = _symbol_avg_price[1]
        
        symbol_bal_second_size  = symbol_bal_second / 100 *  Decimal(_size)
        symbol_fee_perc         = (100 - symbol_fee) / 100 
        quantity_start          = (symbol_bal_second_size / symbol_avg_price) * symbol_fee_perc
        quantity_end            = truncate_by_step_size(quantity_start, symbol_step_size)
        if quantity_end[0] == 'OK':
            _response_tuple = ('OK', quantity_end[1])
    else:
        _response_tuple = ('NOK',  f"{ my_log('Error','get_my_quantity_to_buy',_inputs,_symbol_avg_price[1])}")

    return(_response_tuple)

# Calculate exact Quantity to SELL
def get_my_quantity_to_sell(_binance_client_obj,_symbol_first, _symbol_second, _size=100):
    
    # Prepate
    _symbol                 = f"{_symbol_first}{_symbol_second}".upper()
    _response_tuple         = None
    _inputs                 = f"{_symbol_first}|{_symbol_second}|{_size}"

    symbol_step_size        = None
    symbol_bal_first        = None
    symbol_bal_first_size   = None
    quantity_start          = None
    quantity_end            = None

    # Get Owned Asset Balance
    _symbol_bal_first   = get_my_asset_balance(_binance_client_obj,_symbol_first, _symbol_second, 'sell')

    # Get Symbol Step Size
    if _symbol_bal_first[0] == 'OK':
        _symbol_step_size = get_symbol_info_filter_LOT_SIZE(_binance_client_obj,_symbol)
    else:
        _response_tuple = ('NOK',  f"{ my_log('Error','get_my_quantity_to_sell',_inputs,_symbol_bal_first[1])}")
        return(_response_tuple)

    # Calculate Quantity End
    if _symbol_step_size[0] == 'OK':
        
        symbol_bal_first        = _symbol_bal_first[1]
        symbol_step_size        = _symbol_step_size[1].get('LOT_SIZE_step_size')
        
        symbol_bal_first_size   = symbol_bal_first / 100 *  Decimal(_size)
        quantity_start          = Decimal(symbol_bal_first_size)
        quantity_end            = truncate_by_step_size(quantity_start, symbol_step_size)
        if quantity_end[0] == 'OK':
            _response_tuple = ('OK', quantity_end[1])
    else:
        _response_tuple = ('NOK',  f"{ my_log('Error','get_my_quantity_to_sell',_inputs,_symbol_step_size[1])}")

    return(_response_tuple)
    
"""""""""""""""""""""
Binance Order Functions
"""""""""""""""""""""
# Create a Order Spot Market
def create_order_spot_market(_type, _side, _symbol_first, _symbol_second, _size):
    
    # Prepare
    _symbol         = f"{_symbol_first}{_symbol_second}".upper()
    _response_tuple = None
    _inputs         = f"{_type}|{_side}|{_symbol_first}|{_symbol_second}|{_size}"
    
    _what_fee       = 'taker' # --> vado a Market ergo è un taker
    _quantity       = None
    
    # Instance Binance Client
    _binance_client_obj = Client(config_env.API_KEY, config_env.API_SECRET)
    
    # Choose SIDE
    if _side == 'sell':

        _client_side    = _binance_client_obj.SIDE_SELL
        _quantity       = get_my_quantity_to_sell(_binance_client_obj, _symbol_first, _symbol_second, _size)
        if _quantity[0] == 'NOK':
            _response_tuple = ('NOK',  f"{ my_log('Error','create_order_spot_market',_inputs,_quantity[1])}")
            return(_response_tuple)
            
    elif _side == 'buy':
        
        _client_side    = _binance_client_obj.SIDE_BUY      
        _quantity       = get_my_quantity_to_buy(_binance_client_obj,_symbol_first, _symbol_second, _what_fee, _size)
        if _quantity[0] == 'NOK':
            _response_tuple = ('NOK',  f"{ my_log('Error','create_order_spot_market',_inputs,_quantity[1])}")
            return(_response_tuple)
    else:
        _response_tuple = ('NOK',  f"{ my_log('Error','create_order_spot_market',_inputs,'_side unknown')}")
        return(_response_tuple)

    # Choose TYPE
    if _type == 'market':
        _client_type = _binance_client_obj.ORDER_TYPE_MARKET
    else:
        _response_tuple = ('NOK',  f"{ my_log('Error','create_order_spot_market',_inputs,'_type unknown')}")
        return(_response_tuple)
    
    print(_quantity)
    

    # Create ORDER
    try:
        _order = _binance_client_obj.create_order(  symbol      = _symbol,
                                                    side        = _client_side,
                                                    type        = _client_type,
                                                    quantity    = _quantity[1])
        _response_tuple = ('OK', _order)
        
    except Exception as e:
        _response_tuple = ('NOK',  f"{ my_log('Exception','create_order_spot_market',_inputs,traceback.format_exc())}")

    return(_response_tuple)

    """
    OUTPUT --> _order
    
    minimize: {'symbol': 'BNBUSDT', 'orderId': 537197438, 'orderListId': -1, 'clientOrderId': 'qZkxUqi4qLnbNrlhEQDEmN', 'transactTime': 1590848036857, 'price': '0.00000000', 'origQty': '1.00000000', 'executedQty': '1.00000000', 'cummulativeQuoteQty': '17.44210000', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'fills': [{'price': '17.44210000', 'qty': '1.00000000', 'commission': '0.00075000', 'commissionAsset': 'BNB', 'tradeId': 61069267}]}
    
    Leggibile
    {   'symbol': 'BNBUSDT', 
        'orderId': 537197438, 
        'orderListId': -1, 
        'clientOrderId': 'qZkxUqi4qLnbNrlhEQDEmN', 
        'transactTime': 1590848036857, 
        'price': '0.00000000', 
        'origQty': '1.00000000', 
        'executedQty': '1.00000000', 
        'cummulativeQuoteQty': '17.44210000', 
        'status': 'FILLED', 
        'timeInForce': 'GTC', 
        'type': 'MARKET', 
        'side': 'BUY', 
        'fills': [  {   'price': '17.44210000', 
                        'qty': '1.00000000', 
                        'commission': '0.00075000', 
                        'commissionAsset': 'BNB', 
                        'tradeId': 61069267 }   ]
    }
    """

