from my_class import BinanceAPIClass
from pprint import pprint


def run(choose):

    # Prepare
    symbol_first       = 'BTC'
    symbol_second      = 'USDT'
    symbol             = f"{symbol_first}{symbol_second}"
    binance_client_obj = BinanceAPIClass(symbol_first, symbol_second)

    # General Endpoints
    
    if choose == 1:
        
        # Print Avg Price of Symbol
        _out = binance_client_obj.get_avg_price(symbol)
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


    # Account Endpoints
    
    elif choose == 2:
        
        # Print My Wallet
        _out = binance_client_obj.get_my_balance()
        if _out[0] == 'OK':
            binance_client_obj.print_my_balance_result(_out[1])
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
        
    elif choose == 3:
        
        print(f"{chr(10)}------------")        
        print(f"-- INPUTs --")
        print(f"------------")        
        _type               = input("Choose TYPE (market or limit): ")
        _price              = input("Choose PRICE (None if Market or price if Limit): ")        
        _side               = input("Choose SIDE (buy or sell): ")
        _size               = input("Choose SIZE %: ")        
        _binance_client_obj = BinanceAPIClass(symbol_first, symbol_second, _size)
        print(f"{chr(10)}")
        
        # Make a Order
        _out = _binance_client_obj.create_order_spot(_type, _side, _price)

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

    elif choose == 4:
              
        _binance_client_obj = BinanceAPIClass()
        
        # Get Rate Limits
        _out = _binance_client_obj.get_rate_limits()

        if _out[0] == 'OK':
            print(f"OK --> {_out[1]}")
        elif _out[0] == 'NOK':
            print(f"NOK -->  {_out[1]}")
            
    elif choose == 5:
              
        _binance_client_obj = BinanceAPIClass()
        
        # Get My Openorders
        _out = _binance_client_obj.get_my_openorders()

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
            
    else:

        print(f"{chr(10)}?? But what did you choose ?? --> choose = {choose}{chr(10)}")


if __name__ == "__main__":
    
    choose = input(f"{chr(10)}CHOOSE WHAT TO DO (AvgPriceSymbol 1 , PrintMyBalance 2 , MakeOrderMarketSymbol 3, SeeRateLimit 4. GetAllOpenOrders 5): ") 
    
    run(int(choose))
