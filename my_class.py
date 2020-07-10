# Mathematical
from decimal import getcontext, ROUND_DOWN, Decimal
import math

# Logs
import traceback

# Python Binance Lib
from binance.client import Client, BinanceAPIException

# My
import utility

class BinanceAPIClass:
    
    def __init__(self, _api_key = None, _api_secret = None, _symbol_first = None, _symbol_second = None):

        # Instance Binance Client
        if _api_key is not None and _api_secret is not None:
            self.binance_client_obj = Client(_api_key, _api_secret)
        else:
            self.binance_client_obj = Client()
        
        # Symbol
        if _symbol_first is not None:
            self.symbol_first = _symbol_first.upper()
        if _symbol_second is not None:
            self.symbol_second = _symbol_second.upper()
        if _symbol_first is not None and _symbol_second is not None:
            self.symbol = f"{_symbol_first}{_symbol_second}".upper()
        # Working
        self.response_tuple = None


    """""""""""""""""""""
    MY UTILITY
    """""""""""""""""""""
    # Truncate _qta_start to the largest multiple of _step_size for LOT_SIZE
    def truncate_by_step_size(self, _qta_start, _step_size):
        
        # Prepare
        _digits_decimal     = None
        _qta_start_decimal  = Decimal(_qta_start)
        _qta_end            = None
        _inputs             = f"{_qta_start}|{_step_size}"
        
        # Calculate Digits
        try:
            _digits_decimal = int( round( -math.log(_step_size, 10) , 0 ) )
        except Exception as e:
            self.response_tuple = ('NOK',  f"{ utility.my_log('Exception','truncate_by_step_size',_inputs,traceback.format_exc(2))}")
            return(self.response_tuple)
            
        # By default rounding setting in python is ROUND_HALF_EVEN
        getcontext().rounding = ROUND_DOWN
        
        # Calculate Tot End
        try:
            _qta_end = round( _qta_start_decimal , _digits_decimal )
            self.response_tuple = ('OK',_qta_end)
        except Exception as e:
            self.response_tuple = ('NOK',  f"{ utility.my_log('Exception','truncate_by_step_size',_inputs,traceback.format_exc(2))}")
        
        return(self.response_tuple)
    
    """""""""""""""""""""
    GENERAL ENDPOINTS
    """""""""""""""""""""
    # Check if Symbol Exists
    def check_if_symbol_exists(self, _symbol_input = None):
        
        # Prepare
        _symbol_info    = None    
        _inputs         = None 
        
        try:
            
            if _symbol_input is None:
                _inputs         = f"{self.symbol}"
                _symbol_info    = self.binance_client_obj.get_symbol_info(symbol=self.symbol)
            else:
                _inputs         = f"{_symbol_input}"
                _symbol_info    = self.binance_client_obj.get_symbol_info(symbol=_symbol_input)
            
            if _symbol_info is not None:
                self.response_tuple = ('OK', f"Symbol {_inputs} exist")
            else:
                self.response_tuple = ('NOK', f"Symbol {_inputs} does not exist")

        except BinanceAPIException as e:
            
            _error = str(e).split(":")[1]
            self.response_tuple = ('NOK',  _error)

        except Exception as e:
            
            self.response_tuple = ('NOK',  f"{ utility.my_log('Exception','check_if_symbol_exists',_inputs,traceback.format_exc(2))}")
        
        return(self.response_tuple)
    
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
                    self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_rate_limits',_inputs,'_rate_limits is None')}")
                    
            else:
                self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_rate_limits',_inputs,'_exchange_info is None')}")

        except BinanceAPIException as e:
            
            _error = str(e).split(":")[1]
            self.response_tuple = ('NOK',  _error)

        except Exception as e:
            self.response_tuple = ('NOK',  f"{ utility.my_log('Exception','get_rate_limits',_inputs,traceback.format_exc(2))}")
        
        return(self.response_tuple)


    """""""""""""""""""""""""""
    ACCOUNT ENDPOINTS - GENERIC
    """""""""""""""""""""""""""
    # Get My Dust Logs
    def get_my_dust_log(self):
        
        # Prepare
        _inputs = None
        _dust   = None
        
        try:
            _dust = self.binance_client_obj.get_dust_log()
            self.response_tuple = ('OK', _dust)
            
        except BinanceAPIException as e:
            
            _error = str(e).split(":")[1]
            self.response_tuple = ('NOK',  _error)
            
        except:
            
            self.response_tuple = ('NOK',  f"{ utility.my_log('Exception','get_my_dust',_inputs,traceback.format_exc(2))}")

        """
        {'success': True, 'results': {'rows': [{'transfered_total': '0.00312182', 'service_charge_total': '0.00006371', 'tran_id': 8605174939, 'logs': [{'tranId': 8605174939, 'serviceChargeAmount': '0.00006046', 'uid': '41168199', 'amount': '0.599', 'operateTime': '2020-06-04 09:51:38', 'transferedAmount': '0.00296269', 'fromAsset': 'ADA'}, {'tranId': 8605174939, 'serviceChargeAmount': '0.00000325', 'uid': '41168199', 'amount': '0.00281376', 'operateTime': '2020-06-04 09:51:38', 'transferedAmount': '0.00015913', 'fromAsset': 'USDT'}], 'operate_time': '2020-06-04 09:51:38'}, {'transfered_total': '0.00205088', 'service_charge_total': '0.00004185', 'tran_id': 8665577173, 'logs': [{'tranId': 8665577173, 'serviceChargeAmount': '0.00004185', 'uid': '41168199', 'amount': '0.03642189', 'operateTime': '2020-06-08 09:29:46', 'transferedAmount': '0.00205088', 'fromAsset': 'USDT'}], 'operate_time': '2020-06-08 09:29:46'}, 'total': 3}}
        
        {   'success': True, 
            'results':  {   'rows': [  {    'transfered_total': '0.00312182', 
                                            'service_charge_total': '0.00006371', 
                                            'tran_id': 8605174939, 
                                            'logs': [   {   'tranId': 8605174939, 
                                                            'serviceChargeAmount': '0.00006046', 
                                                            'uid': '41168199', 
                                                            'amount': '0.599', 
                                                            'operateTime': '2020-06-04 09:51:38', 
                                                            'transferedAmount': '0.00296269', 
                                                            'fromAsset': 'ADA'  }   ,
                                                         
                                                        {   'tranId': 8605174939, 
                                                            'serviceChargeAmount': '0.00000325', 
                                                            'uid': '41168199', 
                                                            'amount': '0.00281376', 
                                                            'operateTime': '2020-06-04 09:51:38', 
                                                            'transferedAmount': '0.00015913', 
                                                            'fromAsset': 'USDT' }   ]   ,
                                            'operate_time': '2020-06-04 09:51:38'   }  , 
                                        
                                        {   'transfered_total': '0.00205088', 
                                            'service_charge_total': '0.00004185', 
                                            'tran_id': 8665577173, 
                                            'logs': [   {   'tranId': 8665577173, 
                                                            'serviceChargeAmount': '0.00004185', 
                                                            'uid': '41168199', 
                                                            'amount': '0.03642189', 
                                                            'operateTime': '2020-06-08 09:29:46', 
                                                            'transferedAmount': '0.00205088', 
                                                            'fromAsset': 'USDT' }   ]   , 
                                            'operate_time': '2020-06-08 09:29:46'   }   , 
                                        
                                        {   'transfered_total': '0.0006857', 
                                            'service_charge_total': '0.00001399', 
                                            'tran_id': 8849418754, 
                                            'logs': [   {   'tranId': 8849418754, 
                                                            'serviceChargeAmount': '0.00001399', 
                                                            'uid': '41168199', 
                                                            'amount': '0.0112302', 
                                                            'operateTime': '2020-06-19 08:47:35', 
                                                            'transferedAmount': '0.0006857', 
                                                            'fromAsset': 'USDT' }   ]   , 
                                            'operate_time': '2020-06-19 08:47:35'   }
                                        
                                      ]  , 
                                     
                                'total': 3  
                            }
         }
         
        """


        return(self.response_tuple)

    # Get My Open Orders
    def get_my_openorders(self, _symbol_input = None):

        # Prepare
        _inputs = f"{_symbol_input}"
        
        try:
            if _symbol_input is None:
                _my_openorders  = self.binance_client_obj.get_open_orders()
                self.response_tuple = ('OK', _my_openorders)
            else:
                _my_openorders  = self.binance_client_obj.get_open_orders(symbol=_symbol_input)
                self.response_tuple = ('OK', _my_openorders)
                
        except BinanceAPIException as e:
            
            _error = str(e).split(":")[1]
            self.response_tuple = ('NOK',  _error)
            
        except:
            self.response_tuple = ('NOK',  f"{ utility.my_log('Exception','get_my_openorders',_inputs,traceback.format_exc(2))}")
            
            
        return(self.response_tuple)

    # Get My Balance Total (free & locked)
    def get_my_balance_total(self, _what_based = 'ALL'):
        
        # Prepare
        _my_balance     = []
        _my_asset       = {}
        _account        = None
        _inputs         = None
        
        _symbol_temp_btc        = None
        _symbol_temp_usdt       = None
        _avg_price_temp_btc     = 0
        _avg_price_temp_usdt    = 0
        
        _tot_btc_free       = 0
        _tot_btc_locked     = 0
        _tot_usdt_free      = 0
        _tot_usdt_locked    = 0
        _tot_btc            = 0
        _tot_usdt           = 0                       
        
        try:
            _account = self.binance_client_obj.get_account()
    
            if "balances" in _account:
                
                for bal in _account['balances']: # For every Balances
                    
                    if ( float(bal.get('free')) + float(bal.get('locked')) ) > 0: # Only Asset with something
                        
                        """""""""""""""""""""""""""""""""
                         Build Wallet with List Assets Dict
                        """""""""""""""""""""""""""""""""
                        # Build Asset Dict
                        _my_asset = {   'asset'     : bal.get('asset'), 
                                        'free'      : Decimal(bal.get('free')), 
                                        'locked'    : Decimal(bal.get('locked'))    }
                                        
                        # Build List Assets Dict
                        _my_balance.append(_my_asset)
                        
                        """""""""""""""""""""""""""""""""
                         Build Estimated Value BTC & USDT
                        """""""""""""""""""""""""""""""""
                        # First Asset BTC
                        if _my_asset.get('asset') == 'BTC':
                            
                            # Tot Btc
                            if _what_based.upper() == 'BTC' or _what_based.upper() == 'ALL':
                                _tot_btc_free   = _tot_btc_free + _my_asset.get('free')
                                _tot_btc_locked = _tot_btc_locked + _my_asset.get('locked')

                            # Tot Usdt                            
                            if _what_based.upper() == 'USDT' or _what_based.upper() == 'ALL':                            
                                _avg_price_temp = self.get_avg_price('BTCUSDT')
                                if _avg_price_temp[0] == 'OK':
                                    _tot_usdt_free      = _tot_usdt_free + (_avg_price_temp[1] * _my_asset.get('free'))
                                    _tot_usdt_locked    = _tot_usdt_locked + (_avg_price_temp[1] * _my_asset.get('locked'))                                
                                else:
                                    self.response_tuple = ('NOK',  _avg_price_temp[1])
                        
                        # First Asset USDT
                        elif _my_asset.get('asset') == 'USDT':
                            
                            # Tot Btc
                            if _what_based.upper() == 'BTC' or _what_based.upper() == 'ALL':
                                _avg_price_temp = self.get_avg_price('BTCUSDT')
                                if _avg_price_temp[0] == 'OK':
                                    _tot_btc_free   = _tot_btc_free + _my_asset.get('free') / _avg_price_temp[1]
                                    _tot_btc_locked = _tot_btc_locked + _my_asset.get('locked') / _avg_price_temp[1]                                
                                else:
                                    self.response_tuple = ('NOK', _avg_price_temp[1])
                            
                            # Tot Usdt
                            if _what_based.upper() == 'USDT' or _what_based.upper() == 'ALL':                            
                                _tot_usdt_free      = _tot_usdt_free + _my_asset.get('free')
                                _tot_usdt_locked    = _tot_usdt_locked + _my_asset.get('locked')                            
                        
                        # Others First Asset
                        else:
                            
                            # Tot Btc & Tot Usdt
                            _symbol_temp_btc        = f"{_my_asset.get('asset')}BTC"
                            _symbol_temp_usdt       = f"{_my_asset.get('asset')}USDT"
                            
                            if _what_based.upper() == 'BTC' or _what_based.upper() == 'ALL':
                                
                                _avg_price_temp_btc     = self.get_avg_price(_symbol_temp_btc)
                                if _avg_price_temp_btc[0] == 'OK':
                                    _tot_btc_free   = _tot_btc_free + (_avg_price_temp_btc[1] * _my_asset.get('free'))
                                    _tot_btc_locked = _tot_btc_locked + (_avg_price_temp_btc[1] * _my_asset.get('locked'))
                                else:
                                    self.response_tuple = ('NOK', _avg_price_temp_btc[1])                            
                            
                            
                            if _what_based.upper() == 'USDT' or _what_based.upper() == 'ALL': 
                                
                                _avg_price_temp_usdt    = self.get_avg_price(_symbol_temp_usdt)

                                if _avg_price_temp_usdt[0] == 'OK':
                                    _tot_usdt_free      = _tot_usdt_free + _avg_price_temp_usdt[1] * _my_asset.get('free')
                                    _tot_usdt_locked    = _tot_usdt_locked + _avg_price_temp_usdt[1] * _my_asset.get('locked')                                
                                else:
                                    self.response_tuple = ('NOK',  _avg_price_temp_usdt[1])
                        
                        
                 # Add Estimated Value BTC & USDT at the first position of the list
                _tot_btc    = _tot_btc_free + _tot_btc_locked
                _tot_usdt   = _tot_usdt_free + _tot_usdt_locked
                 
                _my_balance.insert( 0 , { 'totals' : {  'tot_btc_free': _tot_btc_free, 
                                                        'tot_btc_locked': _tot_btc_locked, 
                                                        'tot_usdt_free': _tot_usdt_free, 
                                                        'tot_usdt_locked': _tot_usdt_locked,                                        
                                                        'tot_btc': _tot_btc,
                                                        'tot_usdt': _tot_usdt   }   }   )
                
                self.response_tuple = ('OK', _my_balance)
                
            else:
                self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_my_balance',_inputs,'balances not in _account')}")

        except BinanceAPIException as e:
            
            _error = str(e).split(":")[1]
            self.response_tuple = ('NOK',  _error)
        
        except Exception as e:
            
            self.response_tuple = ('NOK',  f"{ utility.my_log('Exception','get_my_balance',_inputs,traceback.format_exc(2))}")
                
        return(self.response_tuple)
        
    # Get Symbol Info 
    # LOT_SIZE      --> It is used for both buy and sell
    # MIN_NOTIONAL  --> It is used for both buy and sell and it is applied on the symbol_second in the following way: quantity symbol_first * avg price symbol > minNotional of symbol
    def get_symbol_info_filter(self, _what_filter, _symbol_input = None):
        
        # Prepare
        _symbol_info            = None    
        _output_lot_size        = {}
        _output_min_notional    = {}
        _inputs                 = None      
        
        try:

            if _symbol_input is None:
                _inputs         = f"{_what_filter}|{self.symbol}"
                _symbol_info    = self.binance_client_obj.get_symbol_info(symbol=self.symbol)
            else:
                _inputs         = f"{_what_filter}|{_symbol_input}"
                _symbol_info    = self.binance_client_obj.get_symbol_info(symbol=_symbol_input)
            
            if _symbol_info is not None:
                
                filters = _symbol_info.get('filters')
            
                if filters is not None:
                    
                    for f in filters:
                        
                        if _what_filter == 'LOT_SIZE':
                            
                            if f.get('filterType') == _what_filter:
                                _output_lot_size["LOT_SIZE_symbol"]     = self.symbol
                                _output_lot_size["LOT_SIZE_maxQty"]     = Decimal(f.get('maxQty'))
                                _output_lot_size["LOT_SIZE_minQty"]     = Decimal(f.get('minQty'))   # quantity to buy or sell > symbol minQty
                                _output_lot_size["LOT_SIZE_step_size"]  = Decimal(f.get('stepSize')) # the quantity to buy or sell must be an exact multiple of symbol stepSize
                                self.response_tuple                     = ('OK', _output_lot_size)
                                break
                                
                        elif _what_filter == 'MIN_NOTIONAL':
                        
                            if f.get('filterType') == 'MIN_NOTIONAL':
                                _output_min_notional["LOT_SIZE_symbol"]         = self.symbol
                                _output_min_notional["LOT_SIZE_minNotional"]    = Decimal(f.get('minNotional'))
                                _output_min_notional["LOT_SIZE_applyToMarket"]  = f.get('applyToMarket')
                                _output_min_notional["LOT_SIZE_avgPriceMins"]   = f.get('avgPriceMins')
                                self.response_tuple                             = ('OK', _output_min_notional)
                                break
                        else:
                            self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_symbol_info_filter',_inputs,'what_filter is unknown')}")
                
                else:
                    self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_symbol_info_filter',_inputs,'filters is None')}")
                
            else:
                self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_symbol_info_filter',_inputs,'_symbol_info is None')}")

        except BinanceAPIException as e:
            
            _error = str(e).split(":")[1]
            self.response_tuple = ('NOK',  _error)
            
        except Exception as e:
            
            self.response_tuple = ('NOK',  f"{ utility.my_log('Exception','get_symbol_info_filter',_inputs,traceback.format_exc(2))}")
                
        return(self.response_tuple)
    
    # Get Symbol Fee Cost
    # https://binance.zendesk.com/hc/en-us/articles/360007720071-Maker-vs-Taker
    def get_fee_cost(self, _what_fee='taker', _symbol_input = None):
        
        # Prepare
        _fee                = None
        _trade_fee_response = None
        _symbol_exists      = None
        
        try:

            if _symbol_input is None:
                _inputs = f"{self.symbol}|{_what_fee}"
                
                # Check if Symbol Exists
                _symbol_exists  = self.check_if_symbol_exists()
                if _symbol_exists[0] == 'NOK':
                    self.response_tuple = ('NOK', _symbol_exists[1])
                    return(self.response_tuple)             
                
                _trade_fee_response = self.binance_client_obj.get_trade_fee(symbol=self.symbol)
            else:
                _inputs = f"{_symbol_input}|{_what_fee}"
                
                # Check if Symbol Exists
                _symbol_exists = self.check_if_symbol_exists(_symbol_input)
                if _symbol_exists[0] == 'NOK':
                    self.response_tuple = ('NOK',  _symbol_exists[1])
                    return(self.response_tuple)

                _trade_fee_response = self.binance_client_obj.get_trade_fee(symbol=_symbol_input)

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
                                    self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_fee_cost',_inputs,'_what_fee unknown')}")
                                    return(self.response_tuple)
                                    
                                self.response_tuple = ('OK', _fee)
                    else:
                        self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_fee_cost',_inputs,'_trade_fee is Empty')}")
                else:
                    self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_fee_cost',_inputs,'_trade_fee insuccess')}")
            else:
                self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_fee_cost',_inputs,'_trade_fee_response is None')}")

        except BinanceAPIException as e:
            
            _error = str(e).split(":")[1]
            self.response_tuple = ('NOK',  _error)
            
        except Exception as e:
            
            self.response_tuple = ('NOK',  f"{ utility.my_log('Exception','get_fee_cost',_inputs,traceback.format_exc(2))}")
    
        return(self.response_tuple)
    
    # Get Average price in the last 5 minutes
    def get_avg_price(self, _symbol_input = None):
    
        # Prepare
        _price              = None
        _avg_price_response = None
        _symbol_exists      = None
        
        try:
            if _symbol_input is None:
                _inputs = self.symbol
                
                # Check if Symbol Exists
                _symbol_exists  = self.check_if_symbol_exists()
                if _symbol_exists[0] == 'NOK':
                    self.response_tuple = ('NOK', _symbol_exists[1])
                    return(self.response_tuple)               
                
                _avg_price_response = self.binance_client_obj.get_avg_price(symbol=self.symbol)
            else:
                _inputs = _symbol_input
                
                # Check if Symbol Exists
                _symbol_exists = self.check_if_symbol_exists(_symbol_input)
                if _symbol_exists[0] == 'NOK':
                    self.response_tuple = ('NOK',  _symbol_exists[1])
                    return(self.response_tuple)                
                
                _avg_price_response = self.binance_client_obj.get_avg_price(symbol=_symbol_input)
            
            if _avg_price_response is not None:
                _price = Decimal(_avg_price_response.get('price'))
                self.response_tuple = ('OK', _price)
            else:
                self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_avg_price',_inputs,'_avg_price_response is None')}")            

        except BinanceAPIException as e:
            
            _error = str(e).split(":")[1]
            self.response_tuple = ('NOK',  _error)
                
        except Exception as e:
            
            self.response_tuple = ('NOK',  f"{ utility.my_log('Exception','get_avg_price',_inputs,traceback.format_exc(2))}")
    
        return(self.response_tuple)
    
    # Get Asset Free
    def get_my_asset_balance_free(self, _what_symbol_partial):
        
        # Prepare 
        _asset_balance_response = None
        _bal                    = None
        _my_asset               = None
        _inputs                 = f"{self.symbol_first}|{self.symbol_second}|{_what_symbol_partial}"
        
        try:
            _asset_balance_response = self.binance_client_obj.get_asset_balance(asset=_what_symbol_partial)
        
            if _asset_balance_response is not None:
                if _asset_balance_response.get('free') is not None:
                    #_bal = round( Decimal(_asset_balance_response.get('free')) , 5 )
                    _bal = Decimal(_asset_balance_response.get('free'))
                self.response_tuple = ('OK', _bal)
            else:
                self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_my_asset_balance_free',_inputs,'_asset_balance_response is None')}")

        except BinanceAPIException as e:
            
            _error = str(e).split(":")[1]
            self.response_tuple = ('NOK',  _error)
                
        except Exception as e:
            
            self.response_tuple = ('NOK',  f"{ utility.my_log('Exception','get_my_asset_balance_free',_inputs,traceback.format_exc(2))}")
    
        return(self.response_tuple)

    # Calculate exact Quantity to BUY
    def get_my_quantity_to_buy(self, _what_fee, _type, _size, _price = None):
        
        # Prepare
        _inputs                         = f"{_what_fee}|{_type}|{_size}|{_price}|{self.symbol_first}|{self.symbol_second}"
        _get_tot_symbol                 = f"tot_{self.symbol_second.lower()}" # build Wallet Dict Key
        
        symbol_bal_second_free          = None       
        symbol_bal_second_tot_estimated = None
        symbol_bal_to_use               = None
        symbol_bal_to_use_size          = None                
        symbol_step_size                = None
        symbol_min_qty                  = None
        symbol_min_notional             = None        
        symbol_fee                      = None
        symbol_price                    = None
        symbol_fee_perc                 = None
        quantity_start                  = None
        quantity_end                    = None

        # By default rounding setting in python is ROUND_HALF_EVEN
        getcontext().rounding = ROUND_DOWN
        
        # Get Owned Asset Balance Free
        _symbol_bal_second_free = self.get_my_asset_balance_free(self.symbol_second)
        
        # Get Owned Asset Balance Tot Estimated
        if _symbol_bal_second_free[0] == 'OK':
            _symbol_bal_second_tot_estimated    = self.get_my_balance_total(_what_based = self.symbol_second.upper() )
        else:
            self.response_tuple = ('NOK', _symbol_bal_second_free[1])
            return(self.response_tuple)
        
        # Build bal to use & size
        symbol_bal_to_use       = _symbol_bal_second_tot_estimated[1][0].get('totals').get(_get_tot_symbol)
        symbol_bal_to_use_size  = round( symbol_bal_to_use / 100 *  Decimal(_size) , 5 )
        
        # CHECK SIZE
        # The size provided like input is wrong IF the qta 
        # to be used is greater than the one available for that second symbol
        if symbol_bal_to_use_size > _symbol_bal_second_free[1]:
            
            # STOP Qta to sell TO Real Free Qta
            symbol_bal_to_use_size = _symbol_bal_second_free[1]
            
            #_msg                = f"The input Size ( = {_size}) is wrong because the second symbol qta to use to buy ( = {symbol_bal_to_use_size}) > qta available ( = {_symbol_bal_second_free[1]})"
            #self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_my_quantity_to_buy',_inputs,_msg)}")
            #return(self.response_tuple)        
        
        # Get Symbol Filter LOT_SIZE
        if _symbol_bal_second_tot_estimated[0] == 'OK':
            _symbol_lot_size = self.get_symbol_info_filter('LOT_SIZE')
        else:
            self.response_tuple = ('NOK',  _symbol_bal_second_tot_estimated[1])
            return(self.response_tuple)

        # Get Symbol Filter MIN_NOTIONAL
        if _symbol_lot_size[0] == 'OK':
            _symbol_min_notional = self.get_symbol_info_filter('MIN_NOTIONAL')
        else:
            self.response_tuple = ('NOK',  _symbol_lot_size[1])
            return(self.response_tuple)

        # Get Symbol Fee Cost
        if _symbol_min_notional[0] == 'OK':
            _symbol_fee = self.get_fee_cost(_what_fee)
        else:
            self.response_tuple = ('NOK', _symbol_min_notional[1])
            return(self.response_tuple)

        # Get Symbol Price or Symbol Avg Price
        if _type == 'market':
            
            # Get Symbol Avg Price
            if _symbol_fee[0] == 'OK':
                _symbol_price = self.get_avg_price()
            else:
                self.response_tuple = ('NOK',  _symbol_fee[1])
                return(self.response_tuple)
                
        elif (_type == 'limit' or _type == 'stop_limit') and _price is not None:
            
            # SET OK only for the following if 
            # -> in case of order limit the price is a input so it is useless to calculate the average price 
            _symbol_price = tuple( ( 'OK' , Decimal(_price) ) )
        
        # Calculate Quantity End
        if _symbol_price[0] == 'OK':
            
            symbol_step_size        = _symbol_lot_size[1].get('LOT_SIZE_step_size')
            symbol_min_qty          = _symbol_lot_size[1].get('LOT_SIZE_minQty')
            symbol_min_notional     = _symbol_min_notional[1].get('LOT_SIZE_minNotional')
            symbol_fee              = _symbol_fee[1]        
            symbol_price            = _symbol_price[1]
                           
            symbol_fee_perc         = (100 - symbol_fee) / 100 
            quantity_start          = (symbol_bal_to_use_size / symbol_price) * symbol_fee_perc
            quantity_end            = self.truncate_by_step_size(quantity_start, symbol_step_size)
            
            if quantity_end[0] == 'OK':
                
                quantity_temp = quantity_end[1]
                if quantity_temp > symbol_min_qty:
                    
                    if (symbol_price * quantity_temp) > symbol_min_notional:
                        
                        if _size == 100:
                            quantity_temp = quantity_temp - symbol_step_size # To avoid "Account has insufficient balance for requested action" if there is a pump in progress
                    
                        self.response_tuple = ('OK', quantity_temp)
                    
                    else:
                        _msg                = f"Quantity * Price (= {quantity_start*symbol_price:.10f}) to make BUY is not > Symbol Min Notional Qty (= {symbol_min_notional})"
                        self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_my_quantity_to_buy',_inputs,_msg)}")

                else:
                    _msg                = f"Quantity (= {quantity_start:.10f}) to make BUY is not > Symbol Min Qty (= {symbol_min_qty})"
                    self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_my_quantity_to_buy',_inputs,_msg)}")

        else:
            self.response_tuple = ('NOK',  _symbol_price[1])
    
        return(self.response_tuple)

    # Calculate exact Quantity to SELL
    def get_my_quantity_to_sell(self, _type, _size, _price = None):
        
        # Prepare
        _inputs                 = f"{_type}|{_size}|{_price}|{self.symbol_first}|{self.symbol_second}"

        symbol_bal_to_use       = None
        symbol_bal_to_use_size  = None        
        symbol_step_size        = None
        symbol_min_qty          = None
        symbol_min_notional     = None
        symbol_price            = None        
        quantity_start          = None
        quantity_end            = None

        # Get Owned Asset Balance Free
        _symbol_bal_first_free = self.get_my_asset_balance_free(self.symbol_first)       

        # Build bal to use & size
        symbol_bal_to_use       = _symbol_bal_first_free[1]
        symbol_bal_to_use_size  = symbol_bal_to_use / 100 *  Decimal(_size)

        # Get Symbol LOT SIZE
        if _symbol_bal_first_free[0] == 'OK':
            _symbol_lot_size = self.get_symbol_info_filter('LOT_SIZE')
        else:
            self.response_tuple = ('NOK',  _symbol_bal_first_free[1])
            return(self.response_tuple)

        # Get Symbol Filter MIN_NOTIONAL
        if _symbol_lot_size[0] == 'OK':
            _symbol_min_notional = self.get_symbol_info_filter('MIN_NOTIONAL')
        else:
            self.response_tuple = ('NOK',  _symbol_lot_size[1])
            return(self.response_tuple)
        
        # Get Symbol Price or Symbol Avg Price
        if _type == 'market':
            
            # Get Symbol Avg Price
            if _symbol_min_notional[0] == 'OK':
                _symbol_price = self.get_avg_price()
            else:
                self.response_tuple = ('NOK',  _symbol_min_notional[1])
                return(self.response_tuple)
                
        elif (_type == 'limit' or _type == 'stop_limit') and _price is not None:
            
            # SET OK only for the following if 
            # -> in case of order limit the price is a input so it is useless to calculate the average price 
            _symbol_price = tuple( ( 'OK' , Decimal(_price) ) )

        else:
            self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_my_quantity_to_sell',_inputs,'_type unknown or _price is None')}")
            return(self.response_tuple)

        # Calculate Quantity End
        if _symbol_price[0] == 'OK':
            
            symbol_step_size    = _symbol_lot_size[1].get('LOT_SIZE_step_size')
            symbol_min_qty      = _symbol_lot_size[1].get('LOT_SIZE_minQty')
            symbol_min_notional = _symbol_min_notional[1].get('LOT_SIZE_minNotional')
            symbol_price        = _symbol_price[1]
                        
            quantity_start      = Decimal(symbol_bal_to_use_size)
            quantity_end        = self.truncate_by_step_size(quantity_start, symbol_step_size)
            
            if quantity_end[0] == 'OK':
                
                quantity_temp = quantity_end[1]
                if quantity_temp > symbol_min_qty:
                    
                    if (symbol_price * quantity_temp) > symbol_min_notional:
                        self.response_tuple = ('OK', quantity_temp)
                    else:
                        _msg                = f"Quantity * Price (= {quantity_start*symbol_price:.10f}) to make SELL is not > Symbol Min Notional Qty (= {symbol_min_notional})"
                        self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_my_quantity_to_sell',_inputs,_msg)}")
                        
                else:
                    _msg                = f"Quantity (= {quantity_start:.10f}) to make SELL is not > Symbol Min Qty (= {symbol_min_qty})"
                    self.response_tuple = ('NOK',  f"{ utility.my_log('Error','get_my_quantity_to_sell',_inputs,_msg)}")

        else:
            self.response_tuple = ('NOK',  _symbol_price[1])
    
        return(self.response_tuple)


    """""""""""""""""""""""""""
    ACCOUNT ENDPOINTS - ORDER
    """""""""""""""""""""""""""    
    # Create a Order Spot
    def create_order_spot(self, _type, _side, _size, _price, _stop):
        
        # Prepare
        _inputs         = f"{_type}|{_side}|{_size}|{_price}|{_stop}|{self.symbol_first}|{self.symbol_second}"
        _quantity       = None
        _symbol_exists  = None
        
        # Check if Symbol Exists
        _symbol_exists = self.check_if_symbol_exists()
        if _symbol_exists[0] == 'NOK':
            self.response_tuple = ('NOK', _symbol_exists[1])
            return(self.response_tuple)

        # Choose TYPE & FEE
        if _type == 'market':
            _client_type        = self.binance_client_obj.ORDER_TYPE_MARKET
            _what_fee           = 'taker' # --> I'm going to Market so it's a taker
        elif _type == 'limit':
            _client_type        = self.binance_client_obj.ORDER_TYPE_LIMIT
            _client_timeinforce = self.binance_client_obj.TIME_IN_FORCE_GTC            
            _what_fee           = 'maker' # --> I'm going to Price so it's a maker
        elif _type == 'stop_limit':
            _client_type        = self.binance_client_obj.ORDER_TYPE_STOP_LOSS_LIMIT
            _client_timeinforce = self.binance_client_obj.TIME_IN_FORCE_GTC            
            _what_fee           = 'maker' # --> I'm going to Price so it's a maker  
        else:
            self.response_tuple = ('NOK',  f"{ utility.my_log('Error','create_order_spot',_inputs,'_type unknown')}")
            return(self.response_tuple)

        # Choose SIDE and calculate QUANTITY
        if _side == 'sell':
    
            _client_side    = self.binance_client_obj.SIDE_SELL
            _quantity       = self.get_my_quantity_to_sell(_type, _size, _price)
            if _quantity[0] == 'NOK':
                self.response_tuple = ('NOK',  _quantity[1])
                return(self.response_tuple)
            
        elif _side == 'buy':
            
            _client_side    = self.binance_client_obj.SIDE_BUY      
            _quantity       = self.get_my_quantity_to_buy(_what_fee, _type, _size, _price)
            if _quantity[0] == 'NOK':
                self.response_tuple = ('NOK',  _quantity[1])
                return(self.response_tuple)
            
        else:
            self.response_tuple = ('NOK', _minQty_temp[1])
            return(self.response_tuple)
        

        # Create ORDER
        if _type == 'market':

            try:
                _order = self.binance_client_obj.create_order(  symbol      = self.symbol,
                                                                side        = _client_side,
                                                                type        = _client_type,
                                                                quantity    = _quantity[1])
                self.response_tuple = ('OK', _order)
            
            except BinanceAPIException as e:
            
                _error = str(e).split(":")[1]
                self.response_tuple = ('NOK',  _error)                
            
            except:
                
                self.response_tuple = ('NOK',  f"{ utility.my_log('Exception','create_order_spot',_inputs,traceback.format_exc())}")
            
        elif _type == 'limit':   
            
            if _price is None:
                self.response_tuple = ('NOK',  f"{ utility.my_log('Error','create_order_spot',_inputs,'Order Limit without price input')}")
                return(self.response_tuple)
            
            try:
                _order = self.binance_client_obj.create_order(  symbol      = self.symbol,
                                                                side        = _client_side,
                                                                type        = _client_type,
                                                                timeInForce = _client_timeinforce,
                                                                quantity    = _quantity[1],
                                                                price       = _price)
                self.response_tuple = ('OK', _order)
                
            except BinanceAPIException as e:
            
                _error = str(e).split(":")[1]
                self.response_tuple = ('NOK',  _error)                
            
            except:
                
                self.response_tuple = ('NOK',  f"{ utility.my_log('Exception','create_order_spot',_inputs,traceback.format_exc())}")

        elif _type == 'stop_limit':   
            
            if _price is None:
                self.response_tuple = ('NOK',  f"{ utility.my_log('Error','create_order_spot',_inputs,'Order Stop Limit without LIMIT input')}")
                return(self.response_tuple)
                
            if _stop is None:
                self.response_tuple = ('NOK',  f"{ utility.my_log('Error','create_order_spot',_inputs,'Order Stop Limit without STOP input')}")
                return(self.response_tuple)
                
            try:
                
                _order = self.binance_client_obj.create_order(  symbol      = self.symbol,
                                                                side        = _client_side,
                                                                type        = _client_type,
                                                                timeInForce = _client_timeinforce,
                                                                quantity    = _quantity[1],
                                                                price       = _price,
                                                                stopPrice   = _stop)

                self.response_tuple = ('OK', _order)
                
            except BinanceAPIException as e:
            
                _error = str(e).split(":")[1]
                self.response_tuple = ('NOK',  _error)                
            
            except:
                
                self.response_tuple = ('NOK',  f"{ utility.my_log('Exception','create_order_spot',_inputs,traceback.format_exc())}")

        else:
            
            self.response_tuple = ('NOK',  f"{ utility.my_log('Error','create_order_spot',_inputs,'_type unknown')}")


        return(self.response_tuple)


    
        """
        
        >>> OUTPUT MARKET <<<<
        
        Minimize: 
        
        {'symbol': 'BNBUSDT', 'orderId': 537197438, 'orderListId': -1, 'clientOrderId': 'qZkxUqi4qLnbNrlhEQDEmN', 'transactTime': 1590848036857, 'price': '0.00000000', 'origQty': '1.00000000', 'executedQty': '1.00000000', 'cummulativeQuoteQty': '17.44210000', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'fills': [{'price': '17.44210000', 'qty': '1.00000000', 'commission': '0.00075000', 'commissionAsset': 'BNB', 'tradeId': 61069267}]}
        
        Readable:
        
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
        
        >>> OUTPUT LIMIT <<<<
        
        Minimize:
        
        {'symbol': 'BTCUSDT', 'orderId': 2499415863, 'orderListId': -1, 'clientOrderId': 'RLVk6VD4oVuSJA0Ooc1h43', 'transactTime': 1592390815808, 'price': '9488.00000000', 'origQty': '0.00176300', 'executedQty': '0.00000000', 'cummulativeQuoteQty': '0.00000000', 'status': 'NEW', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'SELL', 'fills': []}

        Readable:

        {   'symbol': 'BTCUSDT', 
            'orderId': 2499415863, 
            'orderListId': -1, 
            'clientOrderId': 'RLVk6VD4oVuSJA0Ooc1h43', 
            'transactTime': 1592390815808, 
            'price': '9488.00000000', 
            'origQty': '0.00176300', 
            'executedQty': '0.00000000', 
            'cummulativeQuoteQty': '0.00000000', 
            'status': 'NEW', 
            'timeInForce': 'GTC', 
            'type': 'LIMIT', 
            'side': 'SELL', 
            'fills': []
        }

        >>> OUTPUT STOP LIMIT <<<<
        
        Minimize:
        
        {'symbol': 'BTCUSDT', 'orderId': 2501977468, 'orderListId': -1, 'clientOrderId': 'lZSYY2UqSg64vc50Rrjkjq', 'transactTime': 1592413901290}

        Readable:

        {   'symbol': 'BTCUSDT', 
            'orderId': 2501977468, 
            'orderListId': -1, 
            'clientOrderId': 'lZSYY2UqSg64vc50Rrjkjq', 
            'transactTime': 1592413901290   }
        
        """

    # Cancel a Order Spot
    def cancel_order_spot(self, _symbol_input, _orderid):

        # Prepare
        _inputs         = f"{_symbol_input}|{_orderid}"
        _result_raw     = None
        
        try:
            
            _result_raw = self.binance_client_obj.cancel_order( symbol = _symbol_input, orderId =_orderid)
            
            self.response_tuple = ('OK', _result_raw)

        except BinanceAPIException as e:
            
            _error = str(e).split(":")[1]
            self.response_tuple = ('NOK',  _error)
            return(self.response_tuple)
        
        except:
        
            self.response_tuple = ('NOK',  f"{ utility.my_log('Exception','cancel_order_spot',_inputs,traceback.format_exc())}")
            return(self.response_tuple)

        """
        RESULT OK
        
        {'symbol': 'BTCUSDT', 'origClientOrderId': '85bZyckxB9uqsuXABcFIVG', 'orderId': 2514621522, 'orderListId': -1, 'clientOrderId': 'fVIz5sOrkLaWxn0BvM2GEs', 'price': '9385.00000000', 'origQty': '0.00376400', 'executedQty': '0.00000000', 'cummulativeQuoteQty': '0.00000000', 'status': 'CANCELED', 'timeInForce': 'GTC', 'type': 'STOP_LOSS_LIMIT', 'side': 'BUY', 'stopPrice': '9380.00000000'}

        
        {   'symbol': 'BTCUSDT', 
            'origClientOrderId': '85bZyckxB9uqsuXABcFIVG', 
            'orderId': 2514621522, 
            'orderListId': -1, 
            'clientOrderId': 'fVIz5sOrkLaWxn0BvM2GEs', 
            'price': '9385.00000000', 
            'origQty': '0.00376400', 
            'executedQty': '0.00000000', 
            'cummulativeQuoteQty': '0.00000000', 
            'status': 'CANCELED', 
            'timeInForce': 'GTC', 
            'type': 'STOP_LOSS_LIMIT', 
            'side': 'BUY', 
            'stopPrice': '9380.00000000'    }

        
        """
        
        return(self.response_tuple)
    
    # Convert Dust to BNB
    def convert_my_dust_to_bnb(self, _symbol_input):

        # Prepare
        _inputs             = f"{_symbol_input}"
        _result_raw         = None
        _result_nice        = None
        _transfer_result    = None
        _symbol_input_clean = _symbol_input.upper()
        _tot_gross          = 0
        _fee                = 0
        _tot_net            = 0
        _asset_qta          = 0
        
        try:
            _result_raw = self.binance_client_obj.transfer_dust(asset=_symbol_input_clean)
            
        except BinanceAPIException as e:
            
            _error = str(e).split(":")[1]
            self.response_tuple = ('NOK',  _error)
            return(self.response_tuple)
            
        except:
            
            self.response_tuple = ('NOK',  f"{ utility.my_log('Exception','convert_my_dust_to_bnb',_inputs,traceback.format_exc(2))}")
            return(self.response_tuple)
        
        if _result_raw is not None:
            
            _tot_gross  = Decimal(_result_raw.get('totalTransfered'))
            _fee        = Decimal(_result_raw.get('totalServiceCharge'))
            _tot_net    = _tot_gross - _fee
            
            for _transfer_result in _result_raw.get('transferResult'):
                if _transfer_result is not None:
                    _asset_qta  = _asset_qta + Decimal(_transfer_result.get('amount'))
            
            _result_nice  = f"Dust Asset: {_symbol_input_clean} {chr(10)}"\
                            f"Dust Qta  : {_asset_qta} {chr(10)}"\
                            f"--------{chr(10)}"\
                            f"BNB Gross: {_tot_gross} {chr(10)}"\
                            f"BNB Fee  : {_fee}{chr(10)}"\
                            f"BNB Net  : {_tot_net} {chr(10)}"        
        
            self.response_tuple = ('OK', _result_nice)
        
        else:
            
            self.response_tuple = ('NOK',  f"{ utility.my_log('Error','convert_my_dust_to_bnb',_inputs,'_result_raw is None')}")
            
        """
        RESULT OK
        
        {'totalServiceCharge': '0.00001399','totalTransfered': '0.00069969','transferResult': [{'amount': '0.01123020','fromAsset': 'USDT','operateTime': 1592556454726,'serviceChargeAmount': '0.00001399','tranId': 8849418754,'transferedAmount': '0.00069969'}]}
        
        {'totalServiceCharge': '0.00001399',
        'totalTransfered': '0.00069969',
        'transferResult': [{'amount': '0.01123020',
                            'fromAsset': 'USDT',
                            'operateTime': 1592556454726,
                            'serviceChargeAmount': '0.00001399',
                            'tranId': 8849418754,
                            'transferedAmount': '0.00069969'}]}
        
        RESULT NOK
        
        binance.exceptions.BinanceAPIException: APIError(code=-5002): Insufficient balance
        
        """
        
        return(self.response_tuple)


    """""""""""""""""""""
    FORMAT BINANCE RESULT
    """""""""""""""""""""
    # Format My Open Orders Results
    def format_my_openorders_result(self, _result):

        # Prepare
        _inputs         = f"{_result}"
        _dict           = {}
        _list_result    = []
        _type_result    = None
        _date           = None        
        
        # Build Output --> for each order found
        for _dict in _result:
            
            if _dict.get('time') is not None:
                _date = utility.timestamp_formatter(_dict.get('time')) 
            
            # Common
            _row0   = f"Date: {_date}"             
            _row1   = f"Order Id: {_dict.get('orderId')}"
            _row3   = f"Symbol: {_dict.get('symbol')}"
            _row4   = f"Side: {_dict.get('side')}" 
            _row5   = f"Quantity: {_dict.get('origQty')}"  
        
            _type_result = _dict.get('type').upper()
            
            if _type_result == 'MARKET': # Market Type Order
                
                _row_m_2    =   f"Type: Market"
                
                _message    =   f"{_row0} {chr(10)}"\
                                f"{_row1} {chr(10)}"\
                                f"{_row_m_2} {chr(10)}"\
                                f"{_row3} {chr(10)}"\
                                f"{_row4} {chr(10)}"\
                                f"{_row5}"
        
            elif _type_result == 'LIMIT': # Limit Type Order
                
                _row_l_2    =   f"Type: Limit"
                _row_l_6    =   f"Price: {_dict.get('price')}"
        
                _message    =   f"{_row0} {chr(10)}"\
                                f"{_row1} {chr(10)}"\
                                f"{_row_l_2} {chr(10)}"\
                                f"{_row3} {chr(10)}"\
                                f"{_row4} {chr(10)}"\
                                f"{_row5} {chr(10)}"\
                                f"{_row_l_6}"                                
        
            elif _type_result == 'STOP_LOSS_LIMIT': # Stop Limit Type Order
                
                _row_sl_2   =   f"Type: Stop-Limit"
                _row_sl_6   =   f"Price: {_dict.get('price')}"                    
                _row_sl_7   =   f"Stop: {_dict.get('stopPrice')}"          
        
                _message    =   f"{_row0} {chr(10)}"\
                                f"{_row1} {chr(10)}"\
                                f"{_row_sl_2} {chr(10)}"\
                                f"{_row3} {chr(10)}"\
                                f"{_row4} {chr(10)}"\
                                f"{_row5} {chr(10)}"\
                                f"{_row_sl_6} {chr(10)}"\
                                f"{_row_sl_7}"
                                                        
            else:
                
                self.response_tuple = ('NOK',  f"{ utility.my_log('Error','format_my_openorders_result',_inputs,'_type_result unknown ')}")
                return(self.response_tuple)
            
            # Add Message on List
            _list_result.append(_message) 
        
        self.response_tuple = ('OK', _list_result)
            
        return(self.response_tuple)
    
    # Format Order Spot Result
    def format_order_spot_result(self, _result, _type = None):
        
        # Prepare
        _inputs             = f"{_result}"        
        getcontext().prec   = 8
        _type_result        = None
        _date               = None
        
        # Get useful values
        if _type == 'stop_limit': # --> The type is not written on the output of a STOP_LOSS_LIMIT Order
            _type_result = 'STOP_LOSS_LIMIT'
        else:
            _type_result = _result.get('type').upper()
        
        if _result.get('transactTime') is not None:
            _date = utility.timestamp_formatter(_result.get('transactTime')) 
                    
        # If Filled Build Price & Fee
        _price          = 0
        _qty            = 0
        _price_qty      = 0
        _price_qty_tot  = 0
        _qty_tot        = 0
        _price_avg      = 0
        _fee            = 0
        _fee_symbol     = None
                
        if _result.get('status') == 'FILLED':
            
            for _fill in _result.get('fills'):
            
                # Get & Trasform & Cumulate
                if _fill.get('price') is not None:
                    _price = Decimal(_fill.get('price'))
                if _fill.get('qty') is not None:
                    _qty = Decimal(_fill.get('qty'))
                if _fill.get('commission') is not None:
                    _fee = _fee + Decimal(_fill.get('commission'))
                _fee_symbol = _fill.get('commissionAsset')
            
                # Calculate
                _price_qty      = _price * _qty
                _price_qty_tot  = _price_qty + _price_qty
                _qty_tot        = _qty + _qty
        
            # Weighted average - Media Ponderata
            if _price_qty_tot != 0 and _qty_tot != 0:
                _price_avg = _price_qty_tot / _qty_tot 


        # Common
        _row1   = f"Date: {_date}"
        _row2   = f"Status: {_result.get('status')}"        
        _row3   = f"Order Id: {_result.get('orderId')}"              
        _row5   = f"Symbol: {_result.get('symbol')}" 

        # Build Output
        if _type_result == 'MARKET': # Market Type Order
            
            # Build Rows
            if _result.get('side').upper() == 'BUY':
                _temp1 = "Quantity Buyed"
                _temp2 = "Cost"
            elif _result.get('side').upper() == 'SELL':
                _temp1 = "Quantity Sold"
                _temp2 = "Revenue"
            else:
                self.response_tuple = ('NOK',  f"{ utility.my_log('Error','format_order_spot_result',_inputs,'Side unknown')}")
                return(self.response_tuple)

            _row_m_4 = f"Type: Market"
            _row_m_6 = f"Side: {_result.get('side')}"            
            _row_m_7 = f"Price: {_price_avg}"
            _row_m_8 = f"Fee paid in {_fee_symbol}: {_fee}"

            if _result.get('executedQty') is not None:
                _row_m_9    = f"{_temp1}: {Decimal(_result.get('executedQty'))}"
            else:
                _row_m_9    = f"{_temp1}: {_result.get('executedQty')}"
            if _result.get('cummulativeQuoteQty') is not None:
                _row_m_10   = f"{_temp2}: {Decimal(_result.get('cummulativeQuoteQty'))}"            
            else:
                _row_m_10   = f"{_temp2}: {_result.get('cummulativeQuoteQty')}"
            
            # Build Message
            _message =  f"{_row1} {chr(10)}"\
                        f"{_row2} {chr(10)}"\
                        f"{_row3} {chr(10)}"\
                        f"{_row_m_4} {chr(10)}"\
                        f"{_row5} {chr(10)}"\
                        f"{_row_m_6} {chr(10)}"\
                        f"{_row_m_7} {chr(10)}"\
                        f"{_row_m_8} {chr(10)}"\
                        f"{_row_m_9} {chr(10)}"\
                        f"{_row_m_10}"

        elif _type_result == 'LIMIT': # Limit Type Order
            
            # Build Rows            
            _row_l_4 = f"Type: Limit"
            _row_l_6 = f"Side: {_result.get('side')}"                        
            _row_l_7 = f"Price: {_result.get('price')}"
            _row_l_8 = f"Quantity: {_result.get('origQty')}"
            
            # Build Message
            _message =  f"{_row1} {chr(10)}"\
                        f"{_row2} {chr(10)}"\
                        f"{_row3} {chr(10)}"\
                        f"{_row_l_4} {chr(10)}"\
                        f"{_row5} {chr(10)}"\
                        f"{_row_l_6} {chr(10)}"\
                        f"{_row_l_7} {chr(10)}"\
                        f"{_row_l_8}" 

        elif _type_result == 'STOP_LOSS_LIMIT': # Stop Limit Type Order

            # Build Rows
            _row_sl_4   =   f"Type: Stop-Limit"

            # Build Message
            _message    =   f"{_row1} {chr(10)}"\
                            f"{_row2} {chr(10)}"\
                            f"{_row3} {chr(10)}"\
                            f"{_row_sl_4} {chr(10)}"\
                            f"{_row5}"
        else:
            
            self.response_tuple = ('NOK',  f"{ utility.my_log('Error','format_order_spot_result',_inputs,'_type_result unknown')}")
            return(self.response_tuple)
        
        
        self.response_tuple = ('OK', _message)
        
        return(self.response_tuple)
