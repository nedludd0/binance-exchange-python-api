from my_class import BinanceAPI
from pprint import pprint

# My Binance API Keys
import config_api

# My
import utility

def run(choose, symbol):

    # Prepare
    api_key = config_api.API_KEY
    api_sec = config_api.API_SECRET

    #### GENERAL ENDPOINTS + SPOT DUST ####
    
    # Avg Price Symbol
    if choose == 1:
        
        _binance_obj = BinanceAPI(p_symbol_first = symbol_first, p_symbol_second = symbol_second)

        if _binance_obj.check_client_build_ok(): 
                   
            _out = _binance_obj.general_get_symbol_avg_price()
            
            if _out[0] == 'OK':
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------") 
                print(f"Symbol: {symbol}")
                print(f"Avg Price: {_out[1]}")            
                print(f"{chr(10)}")
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")

        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}") 

    # Mark Price Symbol
    elif choose == 2:
                
        _binance_obj = BinanceAPI(p_symbol_first = symbol_first, p_symbol_second = symbol_second)
        
        if _binance_obj.check_client_build_ok():
                    
            _out = _binance_obj.general_get_symbol_mark_price()
    
            if _out[0] == 'OK':
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------") 
                print(f"Symbol: {symbol}")
                print(f"Mark Price: {_out[1]}")            
                print(f"{chr(10)}")
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}") 

        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}") 

    # Get Symbol Info
    elif choose == 3:
        
        #_wallet = 'spot'
        #_wallet = 'margin'        
        _wallet = 'futures'        
        
        _binance_obj = BinanceAPI(p_wallet = _wallet)
        
        if _binance_obj.check_client_build_ok():
                    
            _out = _binance_obj.general_get_symbol_info_filter('MAX_NUM_ORDERS', symbol)
    
            if _out[0] == 'OK':
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------")             
                pprint(_out[1])
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")  

        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}") 

    # RateLimits
    elif choose == 4:

        _binance_obj = BinanceAPI()
        
        if _binance_obj.check_client_build_ok():
                    
            _out = _binance_obj.general_get_rate_limits()
    
            if _out[0] == 'OK':
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------")             
                pprint(_out[1])
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")  

        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}") 

    # TestConnectivity
    elif choose == 5:
        
        # Test connectivity to the Rest API getting the current server time
        _binance_obj = BinanceAPI()

        if _binance_obj.check_client_build_ok():    
                    
            _out = _binance_obj.general_get_system_status()
    
            if _out[0] == 'OK':
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------")             
                print(_out[1])           
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(_out[1])
                print(f"{chr(10)}")
                
        else:
            
            print(f"-- MY ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}")

    # ConvertMyDust Spot
    elif choose == 6:

        _wallet = 'spot'

        # Inputs
        print(f"{chr(10)}------------")        
        print(f"-- INPUTs --")
        print(f"------------")        
        _symbol = input("Choose Symbol: ")  
        print(f"{chr(10)}")
        
        # Convert My Dust to BNB
        _binance_obj = BinanceAPI(p_api_pub_key = api_key, p_api_secret_key = api_sec, p_wallet = _wallet)

        if _binance_obj.check_client_build_ok():    
                    
            _out = _binance_obj.account_convert_dust2bnb(_symbol)
    
            if _out[0] == 'OK':
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------")             
                print(_out[1])           
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(_out[1])
                print(f"{chr(10)}")

        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}") 

    #### ACCOUNT ENDPOINTS SPOT ####
    
    # MyBalance Spot
    elif choose == 71:
            
        _wallet = 'spot'
        
        _binance_obj = BinanceAPI(p_api_pub_key = api_key, p_api_secret_key = api_sec, p_wallet = _wallet)
        
        if _binance_obj.check_client_build_ok():

            _out = _binance_obj.account_get_balance_total()
    
            if _out[0] == 'OK':
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------")          
                for _dict in _out[1]:
                    
                    if _dict.get('asset') is not None:          
                        print(f"{_dict.get('asset')} free:   {_dict.get('free')     :.8f}")
                        print(f"{_dict.get('asset')} locked: {_dict.get('locked')   :.8f}")
                        print("--------")
                
                print(f"Tot Estimated BTC: {_out[1][0].get('totals').get('tot_btc')   :.8f}")
                print(f"Tot Estimated USD: {_out[1][0].get('totals').get('tot_usd')   :.8f}")
                
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")
            
        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}")
                        
    # MakeOrder Spot
    elif choose == 72:
        
        _wallet = 'spot'
        
        _limit  = None
        _stop   = None
        _price  = None       
        
        # Inputs
        print(f"{chr(10)}------------")        
        print(f"-- INPUTs --")
        print(f"------------")
        print(f"Symbol: {symbol}")
        _type = input("Choose TYPE (market 1, limit 2, stop_limit 3 or oco 4): ")
        if int(_type) == 1:
            _type_str = 'market'
        elif int(_type) == 2:
            _type_str   = 'limit'
            _limit      = input("Choose LIMIT: ")
        elif int(_type) == 3:
            _type_str   = 'stop_limit'
            _stop       = input("Choose STOP: ")             
            _limit      = input("Choose LIMIT: ")                        
        elif int(_type) == 4:
            _type_str   = 'oco'
            _stop       = input("Choose STOP  (sl) : ")            
            _limit      = input("Choose LIMIT (sl) : ")                                                 
            _price      = input("Choose PRICE (tp) : ")                                                       
        _side = input("Choose SIDE (buy 1 or sell 2): ")
        _size = input("Choose SIZE %: ")        
        print(f"{chr(10)}")
        
        if _side == '1':
            _side = 'buy'
        elif _side == '2':
            _side = 'sell'
        
        # Make Order
        _binance_obj = BinanceAPI(p_api_pub_key = api_key, p_api_secret_key = api_sec, p_symbol_first = symbol_first, p_symbol_second = symbol_second, p_wallet = _wallet)

        if _binance_obj.check_client_build_ok():
                    
            _out = _binance_obj.account_create_order(_type_str, _side, _size, _limit, _stop, _price)
    
            if _out[0] == 'OK':
                _formatted_output_temp = _binance_obj.account_format_create_order_result( p_result = _out[1][0], p_type = _type_str)
                _formatted_output      = _formatted_output_temp[1] 
                #_formatted_output      = _out[1][0]
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------")            
                print(f"{_formatted_output}")          
                print(f"{chr(10)}------------")
                print(f"Qta Total: {_out[1][1]}")    
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")
        
        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}") 

    # GetOpenOrders Spot
    elif choose == 73:
        
        _wallet = 'spot'
        
        _binance_obj = BinanceAPI(p_api_pub_key = api_key, p_api_secret_key = api_sec, p_wallet = _wallet)

        if _binance_obj.check_client_build_ok(): 
                 
            _out = _binance_obj.account_get_open_orders()
    
            if _out[0] == 'OK':
                _formatted_output_temp = _binance_obj.account_format_open_orders_result(_out[1])
                _formatted_output      = _formatted_output_temp[1]
                #_formatted_output      =_out[1]             
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------{chr(10)}")  
                for _dict in _formatted_output:          
                    print(f"{_dict}{chr(10)}")
                #print(_formatted_output)
                                  
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")

        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}") 

    # CancelOrder Spot
    elif choose == 74:
        
        _wallet = 'spot'
        
        # Inputs
        print(f"{chr(10)}------------")        
        print(f"-- INPUTs --")
        print(f"------------")        
        _symbol     = input("Choose Symbol: ")
        _orderid    = input("Choose OrderID: ")  
        print(f"{chr(10)}")
        
        # Cancel Order
        _binance_obj = BinanceAPI(p_api_pub_key = api_key, p_api_secret_key = api_sec, p_wallet = _wallet)
        
        if _binance_obj.check_client_build_ok():      
        
            _out = _binance_obj.account_cancel_order(_symbol, _orderid)
    
            if _out[0] == 'OK':
                _formatted_output_temp = _binance_obj.account_format_create_order_result( p_result = _out[1], p_cancel = True)
                _formatted_output      = _formatted_output_temp[1] 
                #_formatted_output      = _out[1]            
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------")             
                print(f"{_formatted_output}")
                #print(_formatted_output)            
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")

        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}") 

    #### ACCOUNT ENDPOINTS MARGIN ####

    # MyBalance Margin
    elif choose == 81:

        _wallet = 'margin'
    
        _binance_obj = BinanceAPI(p_api_pub_key = api_key, p_api_secret_key = api_sec, p_wallet = _wallet)
        
        if _binance_obj.check_client_build_ok():

            _out = _binance_obj.account_get_balance_total()

            if _out[0] == 'OK':
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------")          
                for _dict in _out[1]:
                    
                    if _dict.get('asset') is not None:          
                        print(f"{_dict.get('asset')} free:   {_dict.get('free')     :.8f}")
                        print(f"{_dict.get('asset')} locked: {_dict.get('locked')   :.8f}")
                        print("--------")
                
                print(f"Tot Estimated BTC: {_out[1][0].get('totals').get('tot_btc')   :.8f}")
                print(f"Tot Estimated USD: {_out[1][0].get('totals').get('tot_usd')   :.8f}")
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")
            
        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}")

    # MakeOrder Margin
    elif choose == 82:
        
        _wallet = 'margin'
        
        _limit  = None
        _stop   = None
        _price  = None       
        
        # Inputs
        print(f"{chr(10)}------------")        
        print(f"-- INPUTs --")
        print(f"------------")
        print(f"Symbol: {symbol}")
        _type = input("Choose TYPE (market 1, limit 2, stop_limit 3 or oco 4): ")
        if int(_type) == 1:
            _type_str = 'market'
        elif int(_type) == 2:
            _type_str   = 'limit'
            _limit      = input("Choose LIMIT: ")
        elif int(_type) == 3:
            _type_str   = 'stop_limit'
            _stop       = input("Choose STOP: ")             
            _limit      = input("Choose LIMIT: ")                        
        elif int(_type) == 4:
            _type_str   = 'oco'
            _stop       = input("Choose STOP  (sl) : ")            
            _limit      = input("Choose LIMIT (sl) : ")                                                 
            _price      = input("Choose PRICE (tp) : ")                                                       
        _side = input("Choose SIDE (buy 1 or sell 2): ")
        _size = input("Choose SIZE %: ")        
        print(f"{chr(10)}")

        if _side == '1':
            _side = 'buy'
        elif _side == '2':
            _side = 'sell'

        # Make Order
        _binance_obj = BinanceAPI(p_api_pub_key = api_key, p_api_secret_key = api_sec, p_symbol_first = symbol_first, p_symbol_second = symbol_second, p_wallet = _wallet)

        if _binance_obj.check_client_build_ok():
                    
            _out = _binance_obj.account_create_order(_type_str, _side, _size, _limit, _stop, _price)
    
            if _out[0] == 'OK':
                _formatted_output_temp = _binance_obj.account_format_create_order_result( p_result = _out[1][0], p_type = _type_str)
                _formatted_output      = _formatted_output_temp[1] 
                #_formatted_output      = _out[1][0]
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------")            
                print(f"{_formatted_output}")          
                print(f"{chr(10)}------------")
                print(f"Qta Total: {_out[1][1]}")    
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")
        
        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}") 
            
    # GetOpenOrders Margin
    elif choose == 83:
        
        _wallet = 'margin'        

        _binance_obj = BinanceAPI(p_api_pub_key = api_key, p_api_secret_key = api_sec, p_wallet = _wallet)
        
        if _binance_obj.check_client_build_ok():  
                 
            _out = _binance_obj.account_get_open_orders()
    
            if _out[0] == 'OK':
                _formatted_output_temp = _binance_obj.account_format_open_orders_result(_out[1])
                _formatted_output      = _formatted_output_temp[1]
                #_formatted_output      =_out[1]             
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------{chr(10)}")  
                for _dict in _formatted_output:          
                    print(f"{_dict}{chr(10)}")
                #print(_formatted_output)
                                  
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")

        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}") 

    # CancelOrder Margin
    elif choose == 84:
        
        _wallet = 'margin'
        
        # Inputs
        print(f"{chr(10)}------------")        
        print(f"-- INPUTs --")
        print(f"------------")        
        _symbol     = input("Choose Symbol: ")
        _orderid    = input("Choose OrderID: ")  
        print(f"{chr(10)}")
        
        # Cancel Order
        _binance_obj = BinanceAPI(p_api_pub_key = api_key, p_api_secret_key = api_sec, p_wallet = _wallet)
        
        if _binance_obj.check_client_build_ok():         
        
            _out = _binance_obj.account_cancel_order(_symbol, _orderid)
    
            if _out[0] == 'OK':
                _formatted_output_temp = _binance_obj.account_format_create_order_result( p_result = _out[1], p_cancel = True)
                _formatted_output      = _formatted_output_temp[1] 
                #_formatted_output      = _out[1]            
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------")             
                print(f"{_formatted_output}")
                #print(_formatted_output)            
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")

        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}") 

    #### ACCOUNT ENDPOINTS FUTURES ####

    # MyBalance Futures
    elif choose == 91:

        _wallet = 'futures'
    
        _binance_obj = BinanceAPI(p_api_pub_key = api_key, p_api_secret_key = api_sec, p_wallet = _wallet)
        
        if _binance_obj.check_client_build_ok():

            _out = _binance_obj.account_get_balance_total()
    
            if _out[0] == 'OK':
                pprint(_out[1])
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------")          
                for _dict in _out[1]:
                    if _dict.get('asset') is not None:          
                        print(f"{_dict.get('asset')} free:   {_dict.get('free')     :.8f}")
                        print(f"{_dict.get('asset')} locked: {_dict.get('locked')   :.8f}")
                        print("--------")
                print(f"Tot Estimated USD: {_out[1][0].get('totals').get('tot_usd')   :.8f}")
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")
            
        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}")

    # MakeOrder Futures
    elif choose == 92:
                
        _wallet = 'futures'
        
        _limit  = None
        _stop   = None
        _price  = None       
        
        # Inputs
        print(f"{chr(10)}------------")        
        print(f"-- INPUTs --")
        print(f"------------")
        print(f"Symbol: {symbol}")
        _type = input("Choose TYPE (market 1, limit 2, stop_limit 3 or oco 4): ")
        if int(_type) == 1:
            _type_str = 'market'
        elif int(_type) == 2:
            _type_str   = 'limit'
            _limit      = input("Choose LIMIT: ")
        elif int(_type) == 3:
            _type_str   = 'stop_limit'
            _stop       = input("Choose STOP: ")             
            _limit      = input("Choose LIMIT: ")                        
        elif int(_type) == 4:
            _type_str   = 'oco'
            _stop       = input("Choose STOP  (sl) : ")            
            _limit      = input("Choose LIMIT (sl) : ")                                                 
            _price      = input("Choose PRICE (tp) : ")                                                                     
        _side = input("Choose SIDE (buy 1 or sell 2): ")
        _size = input("Choose SIZE %: ")
                        
        # Decode Side
        if _side == '1':
            _side = 'buy'
        elif _side == '2':
            _side = 'sell'
        
        _size = 0.045
        
        # Make Order
        _binance_obj = BinanceAPI(p_api_pub_key = api_key, p_api_secret_key = api_sec, p_symbol_first = symbol_first, p_symbol_second = symbol_second, p_wallet = _wallet)

        if _binance_obj.check_client_build_ok():
                    
            _out = _binance_obj.account_create_order(_type_str, _side, _size, _limit, _stop, _price)
    
            if _out[0] == 'OK':
                #_formatted_output_temp = _binance_obj.account_format_create_order_result( p_result = _out[1][0], p_type = _type_str)
                #_formatted_output      = _formatted_output_temp[1] 
                _formatted_output      = _out[1]
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------")            
                print(f"{_formatted_output}")          
                print(f"{chr(10)}------------")   
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")
        
        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}") 
            
    # GetOpenOrders Futures
    elif choose == 93:

        # LIMIT         --> OK
        # STOP LIMIT    --> ??
        # STOP MARKET   --> ??
        # TRALING STOP  --> ??

        _wallet = 'futures'        

        _binance_obj = BinanceAPI(p_api_pub_key = api_key, p_api_secret_key = api_sec, p_wallet = _wallet)
        
        if _binance_obj.check_client_build_ok():  
                 
            _out = _binance_obj.account_get_open_orders()
    
            if _out[0] == 'OK':
                _formatted_output_temp = _binance_obj.account_format_open_orders_result(_out[1])
                if _formatted_output_temp[0] == 'OK':
                    _formatted_output = _formatted_output_temp[1]         
                    print(f"{chr(10)}------------")
                    print(f"-- RESULT --")
                    print(f"------------{chr(10)}")  
                    for _dict in _formatted_output:          
                        print(f"{_dict}{chr(10)}")
                else:
                    print(f"{chr(10)}-----------")
                    print(f"-- ERROR formatted output --")
                    print(f"-----------") 
                    print(f"{_formatted_output_temp[1]}")
                    print(f"{chr(10)}")
            else:
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")
        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}") 
        
    # CancelOrder Futures
    elif choose == 94:
        
        _wallet = 'futures'        
       
        # Inputs
        print(f"{chr(10)}------------")        
        print(f"-- INPUTs --")
        print(f"------------")        
        _symbol     = input("Choose Symbol: ")
        _orderid    = input("Choose OrderID: ")  
        print(f"{chr(10)}")
        
        # Cancel Order
        _binance_obj = BinanceAPI(p_api_pub_key = api_key, p_api_secret_key = api_sec, p_wallet = _wallet)
        
        if _binance_obj.check_client_build_ok():         
        
            _out = _binance_obj.account_cancel_order(_symbol, _orderid)
    
            if _out[0] == 'OK':
                _formatted_output_temp = _binance_obj.account_format_create_order_result( p_result = _out[1], p_cancel = True)
                if _formatted_output_temp[0] == 'OK':
                    _formatted_output = _formatted_output_temp[1]         
                    print(f"{chr(10)}------------")
                    print(f"-- RESULT --")
                    print(f"------------{chr(10)}")  
                    print(f"{_formatted_output}")
                else:
                    print(f"{chr(10)}-----------")
                    print(f"-- ERROR formatted output --")
                    print(f"-----------") 
                    print(f"{_formatted_output_temp[1]}")
                    print(f"{chr(10)}")
            else:
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")

        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}") 

    # GetOpenPositions Futures
    elif choose == 95:
        
        _wallet = 'futures'        

        _binance_obj = BinanceAPI(p_api_pub_key = api_key, p_api_secret_key = api_sec, p_wallet = _wallet)
        
        if _binance_obj.check_client_build_ok():  
                 
            _out = _binance_obj.account_get_open_position_information()
    
            if _out[0] == 'OK':
                _formatted_output_temp = _binance_obj.account_format_open_position_result(_out[1])
                if _formatted_output_temp[0] == 'OK':
                    _formatted_output = _formatted_output_temp[1]         
                    print(f"{chr(10)}------------")
                    print(f"-- RESULT --")
                    print(f"------------{chr(10)}")  
                    for _dict in _formatted_output:          
                        print(f"{_dict}{chr(10)}")
                else:
                    print(f"{chr(10)}-----------")
                    print(f"-- ERROR formatted output --")
                    print(f"-----------") 
                    print(f"{_formatted_output_temp[1]}")
                    print(f"{chr(10)}")
            else:
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")

        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.get_client_msg_nok()}") 

    else:
        
        print(f"{chr(10)}?? But what did you choose ?? --> choose = {choose}{chr(10)}")


if __name__ == "__main__":
    
    
    symbol_first    = 'BTC'
    symbol_second   = 'USDT'
    symbol          = f"{symbol_first}{symbol_second}"    
    
    print(f"{chr(10)}Pair we are working on: {symbol}{chr(10)}")
    
    choose = input( f"CHOOSE WHAT TO DO:  {chr(10)}{chr(10)}"\
                    f"---------------------------------------------------{chr(10)}"\
                    f"----------------- GENERAL + SPOT DUST -------------{chr(10)}"\
                    f"---------------------------------------------------{chr(10)}"\
                    f"Avg Price Symbol      [1] - Mark Price Symbol [2]  {chr(10)}"\
                    f"Symbol Info           [3] - RateLimits        [4]  {chr(10)}"\
                    f"Test Connectivity     [5] - Convert Dust Spot [6]  {chr(10)}{chr(10)}"\
                    f"---------------------------------------------------{chr(10)}"\
                    f"----------------- ACCOUNT SPOT --------------------{chr(10)}"\
                    f"---------------------------------------------------{chr(10)}"\
                    f"Balance               [71] - Make Order       [72] {chr(10)}"\
                    f"Get Open Orders       [73] - Cancel Order     [74] {chr(10)}{chr(10)}"\
                    f"---------------------------------------------------{chr(10)}"\
                    f"----------------- ACCOUNT MARGIN ------------------{chr(10)}"\
                    f"---------------------------------------------------{chr(10)}"\
                    f"Balance               [81] - Make Order       [82] {chr(10)}"\
                    f"Get Open Orders       [83] - Cancel Order     [84] {chr(10)}{chr(10)}"\
                    f"---------------------------------------------------{chr(10)}"\
                    f"----------------- ACCOUNT FUTURES -----------------{chr(10)}"\
                    f"---------------------------------------------------{chr(10)}"\
                    f"Balance               [91] - Make Order       [92] {chr(10)}"\
                    f"Get Open Orders       [93] - Cancel Order     [94] {chr(10)}"\
                    f"Get Open Positions    [95] ----------------------- {chr(10)}{chr(10)}"\
                    f"CHOOSE Number: ")
    run(int(choose),symbol)
