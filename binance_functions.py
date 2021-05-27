
from binance.client import Client

def connect_binance(key, secret):
    binance_client = Client(key, secret)
    
    return binance_client


def get_current_assets(client:Client):
    result_account = client.get_account()

    my_assets = {}
    for item in result_account['balances']:
        if float(item['free'])!= 0:
            my_assets[item['asset']] = float(item['free'])

    return my_assets

def get_assets_price(client : Client, assets, reference_asset : str):
    asset_names = list(assets.keys())

    assets_couple = [item + reference_asset for item in asset_names]
    all_tickers = client.get_all_tickers()

    all_tickers_dict = {}
    for ticker in all_tickers:
        all_tickers_dict[ticker['symbol']] = float(ticker['price'])
    
    couple = {}
    for item in assets_couple:
        asset_name = item[0:-3]
        if item in list(all_tickers_dict.keys()):
            couple[asset_name] = float(all_tickers_dict[item])
        elif asset_name+"BTC" in list(all_tickers_dict.keys()):
            couple[asset_name] = float(all_tickers_dict[asset_name+"BTC"]) * float(all_tickers_dict["BTCEUR"])
        elif "BTC" + asset_name in all_tickers_dict.keys():
            couple[asset_name] = float(all_tickers_dict["BTCEUR"]) / float(all_tickers_dict["BTC"+asset_name])

    return couple

def my_assets_price(client : Client):
    my_assets = get_current_assets(client)
    assets_price = get_assets_price(client, my_assets, "EUR")

    my_assets_price_in_EUR = {}
    for asset in list(my_assets.keys()):
        if (asset) in list(assets_price.keys()):
            my_assets_price_in_EUR[asset] = my_assets[asset] * assets_price[asset]
    
    return my_assets_price_in_EUR