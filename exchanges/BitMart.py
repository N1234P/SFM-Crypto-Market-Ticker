import requests


def get_price():
    json = requests.get("https://api-cloud.bitmart.com/spot/v1/ticker").json()

    for x in json['data']['tickers']:
        if x['symbol'] == "SAFEMOON_USDT":
            return x['last_price']