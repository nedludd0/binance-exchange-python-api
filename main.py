from my_class import BinanceAPIClass
from pprint import pprint


def run(choose):

    # Prepare
    symbol_first       = 'BTC'
    symbol_second      = 'USDT'
    symbol             = f"{symbol_first}{symbol_second}"
    binance_client_obj = BinanceAPIClass(symbol_first, symbol_second)

    # General Endpoints
    
    if choose == '1':
        
        # Print Avg Price of Symbol
        _out = binance_client_obj.get_avg_price(symbol)
        if _out[0] == 'OK':
            print(symbol)
            pprint(f"OK --> {_out[1]}")
        elif _out[0] == 'NOK':
            print(f"NOK --> {_out[1]}")


    # Account Endpoints
    
    elif choose == '2':
        
        # Print My Wallet
        _out = binance_client_obj.get_my_wallet_balance()
        if _out[0] == 'OK':
            binance_client_obj.print_my_wallet_balance_result(_out[1])
        elif _out[0] == 'NOK':
            print(f"NOK --> {_out[1]}")
        
        print('-------------')
        print('- Info RUN --')
        print('-------------')        
        print(f"symbol  : {symbol}")      
        
    elif choose == '3':
        
        _choose             = input("Choose buy or sell: ")
        _size               = input("Choose size %: ")        
        _binance_client_obj = BinanceAPIClass(symbol_first, symbol_second, _size)
        
        # Make a Order
        _out = _binance_client_obj.create_order_spot('market', _choose)

        if _out[0] == 'OK':
            pprint(f"OK --> {_out[1]}")
        elif _out[0] == 'NOK':
            print(f"NOK -->  {_out[1]}")
        
    else:
        
        _out = binance_client_obj.get_symbol_info_filter('LOT_SIZE',symbol)
        if _out[0] == 'OK':
            pprint(f"OK lot_size {chr(10)}{_out[1]}")
        elif _out[0] == 'NOK':
            print(f"NOK lot_size {chr(10)}{_out[1]}")
        
        print(chr(10))
        
        _out = binance_client_obj.get_symbol_info_filter('MIN_NOTIONAL',symbol)
        if _out[0] == 'OK':
            pprint(f"OK min_notional {chr(10)}{_out[1]}")
        elif _out[0] == 'NOK':
            print(f"NOK min_notional {chr(10)}{_out[1]}")

        #print(f"{chr(10)}?? But what did you choose ?? --> choose = {choose}{chr(10)}")


if __name__ == "__main__":
    
    choose = input("Choose what to do (AvgPriceSymbol 1 , PrintMyWallet 2 , MakeOrderMarketSymbol 3): ") 
    
    run(choose)
