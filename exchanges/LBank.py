import requests

def get_price():
    params = {
        "symbol": "all"
    }
    json = requests.get("https://api.lbkex.com/v1/ticker.do", params=params).json()
    for x in json:
        if x['symbol'] == "sfm_usdt":
            value = float(x['ticker']['latest'])
            return "{:.10f}".format(value)