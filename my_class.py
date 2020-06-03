# Time
from datetime import datetime
from pytz import timezone

# Mathematical
from decimal import getcontext, ROUND_DOWN, Decimal
import math
import traceback

# Python Binance Lib
import config_api
from binance.client import Client, BinanceAPIException

class BinanceAPIClass:
    
    def __init__(self, _size = 100, _symbol_first = None, _symbol_second = None):
        
        # Instance Binance Client
        self.binance_client_obj = Client(config_api.API_KEY, config_api.API_SECRET)
        
        # Size
        self.size = _size
        # Symbol
        if _symbol_first is not None:
            self.symbol_first   = _symbol_first.upper()
        if _symbol_second is not None:
            self.symbol_second  = _symbol_second.upper()
        if _symbol_first is not None and _symbol_second is not None:
            self.symbol         = f"{_symbol_first}{_symbol_second}".upper()
        # Working
        self.response_tuple = None

    """""""""""""""""""""
    Utility
    """""""""""""""""""""
    
    # Time Formatter
    def my_time_now(self):
        _tz     = timezone('Europe/Rome') # Default Timezone
        _now    = datetime.now(_tz).strftime("%Y-%m-%d %H:%M:%S")
        return(_now)
        
    # Log Formatter
    def my_log(self, _type, _func, _inputs ,_msg):

        if _inputs is not None:
            _msg_error = f"{self.my_time_now()} {_type} on function {_func} with inputs {_inputs} --> MSG {_msg} | "
        else:
            _msg_error = f"{self.my_time_now()} {_type} on function {_func} --> MSG {_msg} | "
            
        return(_msg_error)
        
    # Tronco _tot_start al più grande multimo di _step_size
    def truncate_by_step_size(self, _tot_start, _step_size):
        
        # Prepare
        _digits_decimal     = None
        _tot_start_decimal  = Decimal(_tot_start)
        _tot_end            = None
        _inputs             = f"{_tot_start}|{_step_size}"
        
        # Calculate Digits
        try:
            _digits_decimal = int( round( -math.log(_step_size, 10) , 0 ) )
        except Exception as e:
            self.response_tuple = ('NOK',  f"{ self.my_log('Exception','truncate_by_step_size',_inputs,traceback.format_exc(2))}")
            return(self.response_tuple)
            
        # By default rounding setting in python is ROUND_HALF_EVEN
        getcontext().rounding = ROUND_DOWN
        
        # Calculate Tot End
        try:
            _tot_end = round( _tot_start_decimal , _digits_decimal )
            self.response_tuple = ('OK',_tot_end)
        except Exception as e:
            self.response_tuple = ('NOK',  f"{ self.my_log('Exception','truncate_by_step_size',_inputs,traceback.format_exc(2))}")
        
        return(self.response_tuple)
    
    """""""""""""""""""""
    Binance Base Functions
    """""""""""""""""""""
    # Get Binance Rate Limits
    def get_rate_limits(self):
        
        # Prepare
        _rate_limits    = None
        _exchange_info  = None
        _output_verbose = {}
        _inputs         = None
        
        try:
    
            _exchange_info  = self.binance_client_obj.get_exchange_info()
            
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
                        
                        self.response_tuple = ('OK', _output_verbose)
                        
                else:
                    self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_rate_limits',_inputs,'_rate_limits is None')}")
                    
            else:
                self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_rate_limits',_inputs,'_exchange_info is None')}")
            
        except Exception as e:
            self.response_tuple = ('NOK',  f"{ self.my_log('Exception','get_rate_limits',_inputs,traceback.format_exc(2))}")
        
        return(self.response_tuple)
    
    # Get My Wallet Balance
    def get_my_wallet_balance(self):
        
        # Prepare
        _my_wallet      = []
        _my_asset       = {}
        _place          = 0
        _account        = None
        _inputs         = None
        
        try:
            _account = self.binance_client_obj.get_account()
    
            # Costruisco il Wallet, cioè un dict con gli asset > 0 posseduti 
            if "balances" in _account:
                for bal in _account['balances']:
                    if float(bal.get('free')) > 0.00000000:
                        _my_asset = {'Asset' : bal.get('asset') , 'Amount Free' : bal.get('free'), 'Amount Locked' : bal.get('locked')}
                        _my_wallet.insert( _place, _my_asset )       
                        _place = _place+1
                        
                self.response_tuple = ('OK', _my_wallet)
                
            else:
                self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_wallet_balance',_inputs,'balances not in _account')}")
        
        except Exception as e:
            self.response_tuple = ('NOK',  f"{ self.my_log('Exception','get_wallet_balance',_inputs,traceback.format_exc(2))}")
                
        return(self.response_tuple)
    
    # Get Symbol Info LOT_SIZE
    def get_symbol_info_filter_LOT_SIZE(self):
        
        # Prepare
        _symbol_info        = None    
        _output_lot_size    = {}
        _inputs             = self.symbol
        
        try:
            _symbol_info = self.binance_client_obj.get_symbol_info(self.symbol)
            
            if _symbol_info is not None:
                
                filters = _symbol_info.get('filters')
            
                if filters is not None:
                    
                    for f in filters:
                        
                        if f.get('filterType') == 'LOT_SIZE':
                            _output_lot_size["LOT_SIZE_symbol"]     = self.symbol
                            _output_lot_size["LOT_SIZE_maxQty"]     = Decimal(f.get('maxQty'))
                            _output_lot_size["LOT_SIZE_minQty"]     = Decimal(f.get('minQty'))
                            _output_lot_size["LOT_SIZE_step_size"]  = Decimal(f.get('stepSize'))
                            self.response_tuple                     = ('OK', _output_lot_size)
                            break
                
                else:
                    self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_symbol_info_filter_LOT_SIZE',_inputs,'filters is None')}")
                
            else:
                self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_symbol_info_filter_LOT_SIZE',_inputs,'_symbol_info is None')}")
            
        except Exception as e:
            self.response_tuple = ('NOK',  f"{ self.my_log('Exception','get_symbol_info_filter_LOT_SIZE',_inputs,traceback.format_exc(2))}")
                
        return(self.response_tuple)
        
    # Get Symbol Fee Cost
    # https://binance.zendesk.com/hc/en-us/articles/360007720071-Maker-vs-Taker
    def get_fee_cost(self, _what_fee='taker'):
        
        # Prepare
        _fee                = None
        _trade_fee_response = None
        _inputs             = f"{self.symbol}|{_what_fee}"
        
        try:
            _trade_fee_response = self.binance_client_obj.get_trade_fee(symbol=self.symbol)
            
            if _trade_fee_response is not None:
                if (_trade_fee_response.get('success')):
                    _trade_fee = self.binance_client_obj.get_trade_fee(symbol=self.symbol).get('tradeFee')
                    if bool(_trade_fee): # Checking if dictionary _trade_fee is empty
                        for t in _trade_fee:
                            if t.get('symbol') == self.symbol:
                                if _what_fee == 'taker':
                                    _fee = Decimal(t.get('taker'))
                                elif _what_fee == 'maker':
                                    _fee = Decimal(t.get('maker'))
                                else:
                                    self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_fee_cost',_inputs,'_what_fee unknown')}")
                                    return(self.response_tuple)
                                    
                                self.response_tuple = ('OK', _fee)
                    else:
                        self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_fee_cost',_inputs,'_trade_fee is Empty')}")
                else:
                    self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_fee_cost',_inputs,'_trade_fee insuccess')}")
            else:
                self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_fee_cost',_inputs,'_trade_fee_response is None')}")
            
        except Exception as e:
            self.response_tuple = ('NOK',  f"{ self.my_log('Exception','get_fee_cost',_inputs,traceback.format_exc(2))}")
    
        return(self.response_tuple)
    
    # Get Prezzo medio degli ultimi 5 minuti
    def get_avg_price(self):
    
        # Prepare
        _price              = None
        _avg_price_response = None
        _inputs             = self.symbol
        
        try:
            _avg_price_response = self.binance_client_obj.get_avg_price(symbol=self.symbol)
        
            if _avg_price_response is not None:
                _price = Decimal(_avg_price_response.get('price'))
                self.response_tuple = ('OK', _price)
            else:
                self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_avg_price',_inputs,'_avg_price_response is None')}")            
                
        except Exception as e:
            self.response_tuple = ('NOK',  f"{ self.my_log('Exception','get_avg_price',_inputs,traceback.format_exc(2))}")
    
        return(self.response_tuple)
    
    # Get Asset Free
    def get_my_asset_balance(self, _what_bal):
        
        # Prepare 
        _asset_balance_response = None
        _bal                    = None
        _my_asset               = None
        _inputs                 = f"{self.symbol_first}|{self.symbol_second}|{_what_bal}"
        
        if _what_bal == 'buy':
            _my_asset = self.symbol_second
        elif _what_bal == 'sell':
            _my_asset = self.symbol_first
        else:
            self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_my_asset_balance',_inputs,'_what_bal unknown')}")
            return(self.response_tuple)
            
        try:
            _asset_balance_response = self.binance_client_obj.get_asset_balance(asset=_my_asset)
        
            if _asset_balance_response is not None:
                _bal = Decimal(_asset_balance_response.get('free'))
                self.response_tuple = ('OK', _bal)
            else:
                self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_my_asset_balance',_inputs,'_asset_balance_response is None')}")
                
        except Exception as e:
            self.response_tuple = ('NOK',  f"{ self.my_log('Exception','get_my_asset_balance',_inputs,traceback.format_exc(2))}")
    
        return(self.response_tuple)
    
    # Calculate exact Quantity to BUY
    def get_my_quantity_to_buy(self, _what_fee):
        
        # Prepate
        _inputs                 = f"{self.symbol_first}|{self.symbol_second}|{_what_fee}|{self.size}"
        _what_bal               = 'buy'
        
        symbol_bal_second       = None
        symbol_step_size        = None
        symbol_fee              = None
        symbol_avg_price        = None
        symbol_bal_second_size  = None
        symbol_fee_perc         = None
        quantity_start          = None
        quantity_end            = None
        
        # Get Owned Asset Balance
        _symbol_bal_second  = self.get_my_asset_balance(_what_bal)
        
        # Get Symbol Step Size
        if _symbol_bal_second[0] == 'OK':
            _symbol_step_size = self.get_symbol_info_filter_LOT_SIZE()
        else:
            self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_my_quantity_to_buy',_inputs,_symbol_bal_second[1])}")
            return(self.response_tuple)
        
        # Get Symbol Fee Cost
        if _symbol_step_size[0] == 'OK':
            _symbol_fee = self.get_fee_cost(_what_fee)
        else:
            self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_my_quantity_to_buy',_inputs,_symbol_step_size[1])}")
            return(self.response_tuple)
        
        # Get Symbol Avg Price
        if _symbol_fee[0] == 'OK':
            _symbol_avg_price = self.get_avg_price()
        else:
            self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_my_quantity_to_buy',_inputs,_symbol_fee[1])}")
            return(self.response_tuple)
        
        # Calculate Quantity End
        if _symbol_avg_price[0] == 'OK':
            
            symbol_bal_second   = _symbol_bal_second[1]
            symbol_step_size    = _symbol_step_size[1].get('LOT_SIZE_step_size')
            symbol_fee          = _symbol_fee[1]        
            symbol_avg_price    = _symbol_avg_price[1]
            
            symbol_bal_second_size  = symbol_bal_second / 100 *  Decimal(self.size)
            symbol_fee_perc         = (100 - symbol_fee) / 100 
            quantity_start          = (symbol_bal_second_size / symbol_avg_price) * symbol_fee_perc
            quantity_end            = self.truncate_by_step_size(quantity_start, symbol_step_size)
            if quantity_end[0] == 'OK':
                self.response_tuple = ('OK', quantity_end[1])
        else:
            self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_my_quantity_to_buy',_inputs,_symbol_avg_price[1])}")
    
        return(self.response_tuple)

    # Calculate exact Quantity to SELL
    def get_my_quantity_to_sell(self):
        
        # Prepate
        _inputs                 = f"{self.symbol_first}|{self.symbol_second}|{self.size}"
        _what_bal               = 'sell'
        
        symbol_step_size        = None
        symbol_bal_first        = None
        symbol_bal_first_size   = None
        quantity_start          = None
        quantity_end            = None
    
        # Get Owned Asset Balance
        _symbol_bal_first   = self.get_my_asset_balance(_what_bal)
    
        # Get Symbol Step Size
        if _symbol_bal_first[0] == 'OK':
            _symbol_step_size = self.get_symbol_info_filter_LOT_SIZE()
        else:
            self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_my_quantity_to_sell',_inputs,_symbol_bal_first[1])}")
            return(self.response_tuple)
    
        # Calculate Quantity End
        if _symbol_step_size[0] == 'OK':
            
            symbol_bal_first        = _symbol_bal_first[1]
            symbol_step_size        = _symbol_step_size[1].get('LOT_SIZE_step_size')
            
            symbol_bal_first_size   = symbol_bal_first / 100 *  Decimal(self.size)
            quantity_start          = Decimal(symbol_bal_first_size)
            quantity_end            = truncate_by_step_size(quantity_start, symbol_step_size)
            if quantity_end[0] == 'OK':
                self.response_tuple = ('OK', quantity_end[1])
        else:
            self.response_tuple = ('NOK',  f"{ self.my_log('Error','get_my_quantity_to_sell',_inputs,_symbol_step_size[1])}")
    
        return(self.response_tuple)

    """""""""""""""""""""
    Binance Order Functions
    """""""""""""""""""""
    # Create a Order Spot Market
    def create_order_spot_market(self, _type, _side):
        
        # Prepare
        _inputs         = f"{_type}|{_side}|{self.symbol_first}|{self.symbol_second}|{self.size}"
        _what_fee       = 'taker' # --> vado a Market ergo è un taker
        
        _quantity       = None

        # Choose TYPE
        if _type == 'market':
            _client_type = self.binance_client_obj.ORDER_TYPE_MARKET
        else:
            self.response_tuple = ('NOK',  f"{ self.my_log('Error','create_order_spot_market',_inputs,'_type unknown')}")
            return(self.response_tuple)

        # Choose SIDE and calculate QUANTITY
        if _side == 'sell':
    
            _client_side    = self.binance_client_obj.SIDE_SELL
            _quantity       = self.get_my_quantity_to_sell(self.size)
            if _quantity[0] == 'NOK':
                self.response_tuple = ('NOK',  f"{ self.my_log('Error','create_order_spot_market',_inputs,_quantity[1])}")
                return(self.response_tuple)
                
        elif _side == 'buy':
            
            _client_side    = self.binance_client_obj.SIDE_BUY      
            _quantity       = self.get_my_quantity_to_buy(_what_fee, self.size)
            if _quantity[0] == 'NOK':
                self.response_tuple = ('NOK',  f"{ self.my_log('Error','create_order_spot_market',_inputs,_quantity[1])}")
                return(self.response_tuple)
        else:
            self.response_tuple = ('NOK',  f"{ self.my_log('Error','create_order_spot_market',_inputs,'_side unknown')}")
            return(self.response_tuple)
        
        
        # Create ORDER
        try:
            _order = self.binance_client_obj.create_order(  symbol      = self.symbol,
                                                            side        = _client_side,
                                                            type        = _client_type,
                                                            quantity    = _quantity[1])
            self.response_tuple = ('OK', _order)
            
        except Exception as e:
            self.response_tuple = ('NOK',  f"{ self.my_log('Exception','create_order_spot_market',_inputs,traceback.format_exc())}")
    
        return(self.response_tuple)
    
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
    