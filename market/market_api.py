import requests

from exchanges import Gate, BitMart, LBank


from helper.formatter import price_formatter

import random

transactions_bnb = [0]
transactions = [0]
BITQUERY = "KEY"
BITQUERY2 = "KEY"


async def get_pcs_price():
    API_KEY = "KEY"

    try:
        bnb_lq = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress"
                              "=0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c&address"
                              "=0x87D7fd8c446Cb5D3da3CA23f429e7b7504d1931C"
                              "&tag=latest&apikey=" + API_KEY).json()

        bnb_lq = bnb_lq['result'][:len(str(bnb_lq['result'])) - 18]

        sfm_bnb_lq = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress"
                                  "=0x42981d0bfbAf196529376EE702F2a9Eb9092fcB5&address"
                                  "=0x87D7fd8c446Cb5D3da3CA23f429e7b7504d1931C"
                                  "&tag=latest&apikey=" + API_KEY).json()['result']

        ind = 11 - (20 - len(str(sfm_bnb_lq)))

        sfm_bnb_lq = sfm_bnb_lq[:ind]

        price = (float(bnb_lq) / float(sfm_bnb_lq)) * float(await get_bnb_price("wbnb"))

        return float(str(price)[:9]), ""

    except ValueError:
        return "", ""


# BNB PAIRING SFS
async def get_bnb_sms_price():
    global transactions_bnb

    trend = ""
    API_KEY = ""
    bnb_lq, _, _ = await get_liquidity()
    try:
        sfm_bnb_lq = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress"
                                  "=0x42981d0bfbAf196529376EE702F2a9Eb9092fcB5&address"
                                  "=0x856a1c95bef293de7367b908df2b63ba30fbdd59"
                                  "&tag=latest&apikey=" + API_KEY).json()['result']

        ind = 11 - (20 - len(str(sfm_bnb_lq)))

        sfm_bnb_lq = sfm_bnb_lq[:ind]

        price = float(bnb_lq) / float(sfm_bnb_lq) * await get_bnb_price("wbnb")

        if transactions_bnb[len(transactions_bnb) - 1] > price:
            trend = "<:downtrend:838351636820394004>"
        elif transactions_bnb[len(transactions_bnb) - 1] < price:
            trend = "<:uptrend:838343716276142080>"

        transactions_bnb.append(price)

        return str(price)[:9], trend

    except ValueError:
        return "", ""

    except TypeError:
        return "", ""


# BUSD PAIRING (DEFAULT)
async def get_sms_price():
    global transactions
    trend = ""
    API_KEY = ""
    _, _, busd_lq = await get_liquidity()
    try:
        sfm_busd_lq = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress"
                                   "=0x42981d0bfbAf196529376EE702F2a9Eb9092fcB5&address"
                                   "=0xc223A5cEecd9088C92C76504755507D18913A944"
                                   "&tag=latest&apikey=" + API_KEY).json()['result']

        ind = 11 - (20 - len(str(sfm_busd_lq)))

        sfm_busd_lq = sfm_busd_lq[:ind]

        price = float(busd_lq) / float(sfm_busd_lq)

        if transactions[len(transactions) - 1] > price:
            trend = "<:downtrend:838351636820394004>"
        elif transactions[len(transactions) - 1] < price:
            trend = "<:uptrend:838343716276142080>"

        transactions.append(price)

        return str(price)[:9], trend

    except ValueError:
        return "", ""




async def get_generic_reflection():
    try:
        safemoonswap = await get_sms_price()
        safemoonswap = safemoonswap[0]
        supply = await get_supply()
        return (await get_dex_total_vol(True) * 1000000) / (25 * supply[0]), (
                (await get_dex_total_vol(True) * 1000000) / (25 * supply[0])) * float(
            (safemoonswap))

    except ValueError as e:
        print(e)
        return "", ""

    except TypeError as e:
        print(e)
        return "", ""


# used to limit api calls on cmc
async def get_safemoon_percent():
    try:
        json = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=safemoon-2&order=market_cap_desc"
            "&per_page=100&page=1&sparkline=false").json()

        return str(json[0]['price_change_percentage_24h']) + "%"
    except Exception as e:

        return ""


async def get_sfm_to_bnb_equivalence():
    try:
        bnb_price = await get_bnb_price("wbnb")
        sfm_price = await get_bnb_sms_price()
        sfm_price = float(sfm_price[0])

        return "{:.12f}".format(sfm_price / bnb_price)
    except ValueError as e:
        print(e)
        return ""


async def get_dex_total_vol_cg(tokens):
    try:

        json = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=safemoon-2&order"
                            "=market_cap_desc&per_page=100&page=1&sparkline=false").json()

        if tokens:
            sfs = await get_sms_price()
            sfs = sfs[0]
            dex_vol = int(json[0]['total_volume']) / float(sfs)
            return dex_vol

        return "$" + price_formatter(json[0]['total_volume'])

    except ValueError:
        return ""

    except KeyError:
        return ""

    except requests.exceptions.ConnectionError as e:
        print(e)
        return ""



async def get_dex_total_vol(tokens):
    query = '''{
        ethereum(network: bsc) {
        dexTrades(
        options: {limit: 24, desc: "timeInterval.hour"}
        date: {since: "2021-06-03"}


        baseCurrency: {is: "0x42981d0bfbaf196529376ee702f2a9eb9092fcb5"}
        ) {
        count
        tradeAmount(in: USD)
        timeInterval {
        hour(count: 1)
          }
          }
        }
        }'''

    headers = {
        'X-API-KEY': BITQUERY
    }

    try:
        v1 = \
            requests.post("https://graphql.bitquery.io", json={'query': query}, headers=headers).json()['data'][
                'ethereum'][
                'dexTrades']

        dex_vol = 0
        for q in v1:
            dex_vol += q['tradeAmount']

        if tokens:
            sfs = await get_sms_price()
            sfs = sfs[0]
            dex_vol = int(dex_vol) / float(sfs)
            return dex_vol

        return "$" + price_formatter(dex_vol)
    except:
        return ""


async def get_supply():
    try:
        API_KEY = "KEY"
        json = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress"
                            "=0x42981d0bfbaf196529376ee702f2a9eb9092fcb5&address=0x0000000000000000000000000000000000000001"
                            "&tag=latest&apikey=" + API_KEY).json()
        ind = 11 - (20 - len(str(json.get('result'))))
        bw = json['result'][:ind]

        return 1000000000000 - float(bw), float(bw)
    except Exception as e:
        print(e)
        return "", ""


async def get_burn():
    try:
        return await get_dex_total_vol(True) * .02
    except TypeError:
        return ""


async def get_mc():
    try:
        API_KEY = "KEY"
        supply, unused = await get_supply()
        sfs = await get_sms_price()
        sfs = sfs[0]
        price = float(sfs)
        return supply * price
    except Exception as e:
        print(e)
        return ""


async def other_coins(coin_name):
    API_KEY = await choose_key()

    headers = {
        'X-CMC_PRO_API_KEY': API_KEY,
        'Accepts': 'application/json'
    }

    params = {
        'start': '1',
        'limit': '90',
        'convert': 'USD'
    }
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    json = requests.get(url, params=params, headers=headers).json()
    coins = json['data']

    for x in coins:
        if x['name'] == coin_name:
            return x['quote']['USD']['price']


# used to limit api calls on cmc
async def get_bitcoin_price(coin_name):
    try:
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=' + coin_name + '&vs_currencies=usd'
        json = requests.get(url).json()
        return json['bitcoin']['usd']
    except ValueError:
        return ""


# used to limit api calls on cmc
async def get_bnb_price(coin_name):
    try:
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=' + coin_name + '&vs_currencies=usd'
        json = requests.get(url).json()
        print(json)
        return json['wbnb']['usd']
    except Exception as e:
        print(e)
        return ""


async def exchanges(name):
    exchange_arr = [BitMart, LBank, Gate]

    for exchange in exchange_arr:
        try:
            if name in str(exchange):
                return exchange.get_price()
        except requests.exceptions.ConnectionError:
            continue


# last longer
async def choose_key():
    # API_KEY1 = "KEY"
    # API_KEY2 = "KEY"
    # API_KEY3 = "KEY"
    val = random.randint(1, 2)
    if val % 2 == 0:
        API_KEY = "KEY"
    else:
        API_KEY = "KEY"

    return API_KEY


async def get_liquidity():
    API_KEY = "KEY"

    try:

        sms_bnb = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress"
                           "=0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c&address"
                           "=0x856a1c95bef293de7367b908df2b63ba30fbdd59"
                           "&tag=latest&apikey=" + API_KEY).json()

        sms_busd = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress"
                                "=0xe9e7cea3dedca5984780bafc599bd69add087d56&address"
                                "=0xc223A5cEecd9088C92C76504755507D18913A944"
                                "&tag=latest&apikey=" + API_KEY).json()

        sms_bnb = sms_bnb['result'][:len(str(sms_bnb['result'])) - 18]
        sms_busd = sms_busd['result'][:len(str(sms_busd['result'])) - 18]

        usdsms = float(sms_bnb) * await get_bnb_price("wbnb")

        return sms_bnb, usdsms, sms_busd

    except:
        return "", "", ""
