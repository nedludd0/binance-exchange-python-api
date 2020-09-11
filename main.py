from my_class import BinanceAPIClass
from pprint import pprint

# My Binance API Keys
import config_api

# My
import utility

def run(choose):

    # Prepare
    symbol_first       = 'BTC'
    symbol_second      = 'USDT'
    symbol             = f"{symbol_first}{symbol_second}"
    api_key            = config_api.API_KEY
    api_sec            = config_api.API_SECRET

    ## GENERAL ENDPOINTS ##
    
    # AvgPriceSymbol
    if choose == 1:
        
        _binance_obj = BinanceAPIClass(_symbol_first = symbol_first, _symbol_second = symbol_second)
        
        if _binance_obj.client[0] == 'OK': 
                   
            _out = _binance_obj.get_avg_price()
            
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
            print(f"{_binance_obj.client[1]}") 

    # RateLimits
    elif choose == 2:

        _binance_obj = BinanceAPIClass()
        
        if _binance_obj.client[0] == 'OK':
                    
            _out = _binance_obj.get_rate_limits()
    
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
            print(f"{_binance_obj.client[1]}") 


    ## ACCOUNT ENDPOINTS ##
    
    # MyBalance
    elif choose == 3:
             
        _binance_obj = BinanceAPIClass(api_key, api_sec)
        
        if _binance_obj.client[0] == 'OK':

            _out = _binance_obj.get_my_balance_total()
    
            if _out[0] == 'OK':
                print(f"{chr(10)}------------")
                print(f"-- RESULT --")
                print(f"------------")          
                for _dict in _out[1]:
                    
                    if _dict.get('asset') is not None:          
                        print(f"{_dict.get('asset')} free:   {_dict.get('free')     :.8f}")
                        print(f"{_dict.get('asset')} locked: {_dict.get('locked')   :.8f}")
                        print("--------")
                
                print(f"Tot Estimated BTC:  {_out[1][0].get('totals').get('tot_btc')    :.8f}")
                print(f"Tot Estimated USDT: {_out[1][0].get('totals').get('tot_usdt')   :.8f}")
                
            elif _out[0] == 'NOK':
                print(f"{chr(10)}-----------")
                print(f"-- ERROR --")
                print(f"-----------") 
                print(f"{_out[1]}")
                print(f"{chr(10)}")
            
        else:
            
            print(f"-- ERROR --")
            print(f"{_binance_obj.client[1]}")            
        


    # MakeOrder
    elif choose == 4:

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
        _side = input("Choose SIDE (buy or sell): ")
        _size = input("Choose SIZE %: ")        
        print(f"{chr(10)}")

        # Make Order
        _binance_obj = BinanceAPIClass(api_key, api_sec, symbol_first, symbol_second)

        if _binance_obj.client[0] == 'OK':
                    
            _out = _binance_obj.create_order_spot(_type_str, _side, _size, _limit, _stop, _price)
    
            if _out[0] == 'OK':
                _formatted_output_temp = _binance_obj.format_create_order_spot_result( _result = _out[1][0], _type = _type_str)
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
            print(f"{_binance_obj.client[1]}") 
            
    # GetOpenOrders
    elif choose == 5:
        
        _binance_obj = BinanceAPIClass(api_key, api_sec)
        
        if _binance_obj.client[0] == 'OK':   
                 
            _out = _binance_obj.get_my_openorders()
    
            if _out[0] == 'OK':
                _formatted_output_temp = _binance_obj.format_open_orders_result(_out[1])
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
            print(f"{_binance_obj.client[1]}") 

    # CancelOrder
    elif choose == 6:
        
        # Inputs
        print(f"{chr(10)}------------")        
        print(f"-- INPUTs --")
        print(f"------------")        
        _symbol     = input("Choose Symbol: ")
        _orderid    = input("Choose OrderID: ")  
        print(f"{chr(10)}")
        
        # Cancel Order
        _binance_obj = BinanceAPIClass(api_key, api_sec)
        
        if _binance_obj.client[0] == 'OK':        
        
            _out = _binance_obj.cancel_order_spot(_symbol, _orderid)
    
            if _out[0] == 'OK':
                _formatted_output_temp = _binance_obj.format_create_order_spot_result( _result = _out[1], _cancel = True)
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
            print(f"{_binance_obj.client[1]}") 

    # ConvertMyDust
    elif choose == 7:
        
        # Inputs
        print(f"{chr(10)}------------")        
        print(f"-- INPUTs --")
        print(f"------------")        
        _symbol = input("Choose Symbol: ")  
        print(f"{chr(10)}")
        
        # Convert My Dust to BNB
        _binance_obj = BinanceAPIClass(api_key, api_sec)

        if _binance_obj.client[0] == 'OK':
                    
            _out = _binance_obj.convert_my_dust_to_bnb(_symbol)
    
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
            print(f"{_binance_obj.client[1]}") 

    # TestConnectivity
    elif choose == 8:
        
        # Test connectivity to the Rest API getting the current server time
        _binance_obj = BinanceAPIClass()

        if _binance_obj.client[0] == 'OK':
                    
            _out = _binance_obj.test_connectivity()
    
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
            print(f"{_binance_obj.client[1]}")

    else:
        

        print(f"{chr(10)}?? But what did you choose ?? --> choose = {choose}{chr(10)}")
        

if __name__ == "__main__":
    
    choose = input(f"{chr(10)}CHOOSE WHAT TO DO (AvgPriceSymbol 1, RateLimits 2 , MyBalance 3 , MakeOrder 4, GetOpenOrders 5, CancelOrder 6, ConvertMyDust 7, TestConnectivity 8): ") 
    
    run(int(choose))
