from my_class import BinanceAPIClass
from pprint import pprint

# My Binance API Keys
import config_api

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
        
        _binance_client_obj = BinanceAPIClass(_symbol_first = symbol_first, _symbol_second = symbol_second)
        _out                = _binance_client_obj.get_avg_price()
        
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

    # RateLimits
    elif choose == 2:

        _binance_client_obj = BinanceAPIClass()
        _out                = _binance_client_obj.get_rate_limits()

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
    

    ## ACCOUNT ENDPOINTS ##
    
    # MyBalance
    elif choose == 3:
        
        _binance_client_obj = BinanceAPIClass(api_key, api_sec)
        _out                = _binance_client_obj.get_my_balance_total()
        
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

    # MakeOrder
    elif choose == 4:

        _price  = None
        _stop   = None
        
        # Inputs
        print(f"{chr(10)}------------")        
        print(f"-- INPUTs --")
        print(f"------------")
        print(f"Symbol: {symbol}")
        _type = input("Choose TYPE (market 1, limit 2 or stop_limit 3): ")
        if int(_type) == 1:
            _type = 'market'
        elif int(_type) == 2:
            _type   = 'limit'
            _price  = input("Choose PRICE: ")
        elif int(_type) == 3:
            _type   = 'stop_limit'
            _stop   = input("Choose STOP: ")             
            _price  = input("Choose PRICE: ")                                       
        _side = input("Choose SIDE (buy or sell): ")
        _size = input("Choose SIZE %: ")        
        print(f"{chr(10)}")
        
        # Make Order
        _binance_client_obj = BinanceAPIClass(api_key, api_sec, symbol_first, symbol_second)
        _out                = _binance_client_obj.create_order_spot(_type, _side, _size, _price, _stop)

        if _out[0] == 'OK':
            _formatted_output_temp = _binance_client_obj.format_order_spot_result( _out[1], _type)
            _formatted_output      = _formatted_output_temp[1] 
            #_formatted_output      = _out[1]
            print(f"{chr(10)}------------")
            print(f"-- RESULT --")
            print(f"------------")            
            print(f"{_formatted_output}")
            #print(_formatted_output)            
            print(f"{chr(10)}")            
        elif _out[0] == 'NOK':
            print(f"{chr(10)}-----------")
            print(f"-- ERROR --")
            print(f"-----------") 
            print(f"{_out[1]}")
            print(f"{chr(10)}")

    # GetOpenOrders
    elif choose == 5:
        
        _binance_client_obj = BinanceAPIClass(api_key, api_sec)
        _out                = _binance_client_obj.get_my_openorders()

        if _out[0] == 'OK':
            _formatted_output_temp = _binance_client_obj.format_my_openorders_result(_out[1])
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
        _binance_client_obj = BinanceAPIClass(api_key, api_sec)
        _out                = _binance_client_obj.cancel_order_spot(_symbol, _orderid)

        if _out[0] == 'OK':
            _formatted_output_temp = _binance_client_obj.format_order_spot_result( _out[1])
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

    # ConvertMyDust
    elif choose == 7:
        
        # Inputs
        print(f"{chr(10)}------------")        
        print(f"-- INPUTs --")
        print(f"------------")        
        _symbol = input("Choose Symbol: ")  
        print(f"{chr(10)}")
        
        # Convert My Dust to BNB
        _binance_client_obj = BinanceAPIClass(api_key, api_sec)
        _out                = _binance_client_obj.convert_my_dust_to_bnb(_symbol)

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
        
        print(f"{chr(10)}?? But what did you choose ?? --> choose = {choose}{chr(10)}")

if __name__ == "__main__":
    
    choose = input(f"{chr(10)}CHOOSE WHAT TO DO (AvgPriceSymbol 1, RateLimits 2 , MyBalance 3 , MakeOrder 4, GetOpenOrders 5, CancelOrder 6, ConvertMyDust 7): ") 
    
    run(int(choose))
