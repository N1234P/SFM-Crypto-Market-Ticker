import requests

def get_price():
    return requests.get("https://data.gateapi.io/api2/1/tickers").json()['sfm_usdt']['last']