from my_class import BinanceAPIClass
from pprint import pprint


def run(choose):

    # Prepare
    symbol_first       = 'BTC'
    symbol_second      = 'USDT'
    symbol             = f"{symbol_first}{symbol_second}"

    ## GENERAL ENDPOINTS ##
    
    # AvgPriceSymbol
    if choose == 1:
        
        _binance_client_obj = BinanceAPIClass(symbol_first, symbol_second)
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
        
        _binance_client_obj = BinanceAPIClass()
        _out                = _binance_client_obj.get_my_balance()
        
        if _out[0] == 'OK':
            _binance_client_obj.print_my_balance_result(_out[1])
        elif _out[0] == 'NOK':
            print(f"{chr(10)}-----------")
            print(f"-- ERROR --")
            print(f"-----------") 
            print(f"{_out[1]}")
            print(f"{chr(10)}")
        
        print('-------------')
        print('- Info RUN --')
        print('-------------')        
        print(f"symbol  : {symbol}")   
    
    # MakeOrder
    elif choose == 4:

        _price = None
        
        # Inputs
        print(f"{chr(10)}------------")        
        print(f"-- INPUTs --")
        print(f"------------")        
        _type               = input("Choose TYPE (market or limit): ")
        if _type == 'limit':
            _price          = input("Choose PRICE (None if Market or value if Limit): ")        
        _side               = input("Choose SIDE (buy or sell): ")
        _size               = input("Choose SIZE %: ")        
        print(f"{chr(10)}")
        
        # Make Order
        _binance_client_obj = BinanceAPIClass(symbol_first, symbol_second, _size)
        _out                = _binance_client_obj.create_order_spot(_type, _side, _price)

        if _out[0] == 'OK':
            _formatted_output_temp = binance_client_obj.format_order_spot_result(_type, _out[1])
            _formatted_output      = _formatted_output_temp[1] 
            #_formatted_output       = _out[1]
            print(f"{chr(10)}------------")
            print(f"-- RESULT --")
            print(f"------------")            
            print(f"{_formatted_output}")
            print(f"{chr(10)}")            
        elif _out[0] == 'NOK':
            print(f"{chr(10)}-----------")
            print(f"-- ERROR --")
            print(f"-----------") 
            print(f"{_out[1]}")
            print(f"{chr(10)}")


    # GetOpenOrders
    elif choose == 5:
        
        _binance_client_obj = BinanceAPIClass()
        _out                = _binance_client_obj.get_my_openorders()

        if _out[0] == 'OK':
            print(f"{chr(10)}------------")
            print(f"-- RESULT --")
            print(f"------------{chr(10)}")  
            for _dict in _out[1]:          
                print(f"{_dict}{chr(10)}")
                              
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
        _binance_client_obj = BinanceAPIClass()
        _out                = _binance_client_obj.cancel_order_spot(_symbol, _orderid)

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

        print(f"{chr(10)}?? But what did you choose ?? --> choose = {choose}{chr(10)}")


if __name__ == "__main__":
    
    choose = input(f"{chr(10)}CHOOSE WHAT TO DO (AvgPriceSymbol 1, RateLimits 2 , MyBalance 3 , MakeOrder 4, GetOpenOrders 5, CancelOrder 6): ") 
    
    run(int(choose))
