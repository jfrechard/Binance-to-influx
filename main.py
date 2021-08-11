import influxData as influx
from binance_functions import *
from datetime import datetime
import time
from credential import *

influx_writer = influx.connect_InfluxDB(influx_token, influx_url)

binance_client = connect_binance(binance_api_key,binance_api_secret)

while True:
    my_crypto_price = my_assets_price(binance_client)
    sum_crypto = 0
    for crypto in my_crypto_price:
        data = influx.data("my_crypto","cryptoineuro",{"asset": crypto},my_crypto_price[crypto],datetime.utcnow())
        data.write_datas(influx_writer)

        sum_crypto += my_crypto_price[crypto]
    
    data_sum = data = influx.data("sum_crypto","cryptoineuro",{},sum_crypto,datetime.utcnow())
    data_sum.write_datas(influx_writer)
    print("request OK")
    time.sleep(300)
