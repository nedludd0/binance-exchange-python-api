from my_class import BinanceAPIClass
from pprint import pprint


def run(choose):

    # Prepare
    symbol_first       = 'ADA'
    symbol_second      = 'BTC'
    symbol             = f"{symbol_first}{symbol_second}"
    size               = 100
    binance_client_obj = BinanceAPIClass(symbol_first, symbol_second, size)

    # General Endpoints
    
    if choose == 'AvgPriceSymbol':
        
        # Print Avg Price of Symbol
        _out = binance_client_obj.get_avg_price(symbol)
        if _out[0] == 'OK':
            print(symbol)
            pprint(f"OK --> {_out[1]}")
        elif _out[0] == 'NOK':
            print(f"NOK --> {_out[1]}")


    # Account Endpoints
    
    elif choose == 'PrintMyWallet':
        
        # Print My Wallet
        _out = binance_client_obj.get_my_wallet_balance()
        if _out[0] == 'OK':
            binance_client_obj.print_my_wallet_balance_result(_out[1])
        elif _out[0] == 'NOK':
            print(f"NOK --> {_out[1]}")
        
    elif choose == 'MakeOrderMarketSymbol':
        
        # Make a Order
        _out = binance_client_obj.create_order_spot('market', 'sell')

        if _out[0] == 'OK':
            pprint(f"OK --> {_out[1]}")
        elif _out[0] == 'NOK':
            print(f"NOK --> {_out[1]}")
        
    else:
        
        print(f"{chr(10)}?? But what did you choose ?? --> choose = {choose}{chr(10)}")


if __name__ == "__main__":
    
    choose = input("Choose what to do (AvgPriceSymbol, PrintMyWallet, MakeOrderMarketSymbol): ") 
    
    run(choose)
