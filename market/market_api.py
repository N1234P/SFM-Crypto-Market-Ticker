import requests

from exchanges import Gate, BitMart, LBank
import asyncio

from helper.formatter import price_formatter

import random

transactions_bnb = [0]
transactions = [0]
BITQUERY = "signupforbitquery"
BITQUERY2 = "if BITQUERY runs out"


async def get_pcs_price():
    API_KEY = "MJYCR4Q2Z98ZDHTWAMFFCTJXTEKEDPKFQQ"

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

        price = (float(bnb_lq) / float(sfm_bnb_lq)) * float(await get_bnb_price("binancecoin"))

        return float(str(price)[:9]), ""

    except ValueError:
        return "", ""


# BNB PAIRING SFS
async def get_bnb_sms_price():
    global transactions_bnb

    trend = ""
    API_KEY = "MJYCR4Q2Z98ZDHTWAMFFCTJXTEKEDPKFQQ"
    bnb_lq, _, _ = await get_liquidity()
    try:
        sfm_bnb_lq = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress"
                                  "=0x42981d0bfbAf196529376EE702F2a9Eb9092fcB5&address"
                                  "=0x8fb9bbfd97fff7bba69c0162a9632c9503b29cd4"
                                  "&tag=latest&apikey=" + API_KEY).json()['result']

        ind = 11 - (20 - len(str(sfm_bnb_lq)))

        sfm_bnb_lq = sfm_bnb_lq[:ind]

        price = float(bnb_lq) / float(sfm_bnb_lq) * await get_bnb_price("binancecoin")

        if transactions_bnb[len(transactions_bnb) - 1] > price:
            trend = "<:downtrend:838351636820394004>"
        elif transactions_bnb[len(transactions_bnb) - 1] < price:
            trend = "<:uptrend:838343716276142080>"

        transactions_bnb.append(price)

        return str(price)[:9], trend

    except ValueError:
        return "", ""


# BUSD PAIRING (DEFAULT)
async def get_sms_price():
    global transactions
    trend = ""
    API_KEY = "MJYCR4Q2Z98ZDHTWAMFFCTJXTEKEDPKFQQ"
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


async def get_sms_price_alt():
    global transactions

    query = '''{
  ethereum(network: bsc) {
    dexTrades(
      options: {desc: ["block.height","tradeIndex"], limit: 3}
      exchangeName: {notIn: ["Pancake", "Pancake v2"]}
      baseCurrency: {is: "0x42981d0bfbaf196529376ee702f2a9eb9092fcb5"}
      quoteCurrency: {is: "0xe9e7cea3dedca5984780bafc599bd69add087d56"}
      date: {after: "2021-04-28"}
    ) {
      transaction {
        hash
      }
      tradeIndex
      smartContract {
        address {
          address
        }
        contractType
        currency {
          name
        }
      }
      tradeIndex
      block {
        height
      }
      baseCurrency {
        symbol
        address
      }
      quoteCurrency {
        symbol
        address
      }
      quotePrice

    }
  }
}
'''
    trend = ""
    headers = {
        'X-API-KEY': BITQUERY
    }
    limit = 3  # too many calls may lead to memory issues and other underlying issues. resort to the most recent
    # gotten price after 1 attempt(s).
    while True:

        if limit == 0:
            print("limit exceeded")

            return str("{:.10f}".format(transactions[len(transactions) - 1])), ""
        try:
            arr = requests.post('https://graphql.bitquery.io/',
                                json={'query': query}, headers=headers).json()['data']['ethereum']['dexTrades']
            break

        except ValueError as e:
            print(e)
            limit -= 1
            await asyncio.sleep(.2)
            pass

    list_prices = []
    if arr is not None:
        for transaction in arr:
            list_prices.append(float(transaction['quotePrice']))

        price = sorted(list_prices)[1]
        if transactions[len(transactions) - 1] > price:
            trend = "<:downtrend:838351636820394004>"
        elif transactions[len(transactions) - 1] < price:
            trend = "<:uptrend:838343716276142080>"

        transactions.append(price)

        return str("{:.10f}".format(price))[:9], trend

    return "", ""


async def get_generic_reflection():
    try:
        safemoonswap = await get_sms_price()
        safemoonswap = safemoonswap[0]
        return (await get_dex_total_vol(True) * 1000000) / (20 * 550000000000), (
                (await get_dex_total_vol(True) * 1000000) / (20 * 550000000000)) * float(
            (safemoonswap))

    except ValueError as e:
        print(e)
        return "", ""

    except TypeError as e:
        print(e)
        return "", ""


async def get_percentage_change():
    API_KEY = await choose_key()

    headers = {
        'X-CMC_PRO_API_KEY': API_KEY,
        'Accepts': 'application/json'
    }

    params = {
        'start': '1',
        'limit': '250',
        'convert': 'USD'
    }
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    json = requests.get(url, params=params, headers=headers).json()
    coins = json['data']
    btc_percent, bnb_percent, eth_percent, sfm_percent = "", "", "", await get_safemoon_percent()
    for coin in coins:
        if coin['name'] == "Bitcoin":
            btc_percent = str(coin['quote']['USD']['percent_change_24h']) + "%"
        elif coin['name'] == "Binance Coin":
            bnb_percent = str(coin['quote']['USD']['percent_change_24h']) + "%"
        elif coin['name'] == "Ethereum":
            eth_percent = str(coin['quote']['USD']['percent_change_24h']) + "%"

    return sfm_percent, btc_percent, bnb_percent, eth_percent


# used to limit api calls on cmc
async def get_safemoon_percent():
    json = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=safemoon-2&order=market_cap_desc&per_page=100&page=1&sparkline=false").json()

    return str(json[0]['price_change_percentage_24h']) + "%"


async def get_sfm_to_bnb_equivalence():
    try:
        bnb_price = await get_bnb_price("binancecoin")
        sfm_price = await get_sms_price()
        sfm_price = float(sfm_price[0])

        return "{:.12f}".format(sfm_price / bnb_price)
    except ValueError as e:
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
        requests.post("https://graphql.bitquery.io", json={'query': query}, headers=headers).json()['data']['ethereum'][
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
        API_KEY = "MJYCR4Q2Z98ZDHTWAMFFCTJXTEKEDPKFQQ"
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
        API_KEY = "MJYCR4Q2Z98ZDHTWAMFFCTJXTEKEDPKFQQ"
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
        return json['binancecoin']['usd']
    except ValueError:
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
    # API_KEY1 = "9444e442-c990-4ab4-8c2c-f12bd26e562f"
    # API_KEY2 = "3ddfb550-c326-44f2-9fd0-d875e757ccd1"
    # API_KEY3 = "7746addb-4e30-4e5a-80b0-1c3e57c56e02
    val = random.randint(1, 2)
    if val % 2 == 0:
        API_KEY = "9444e442-c990-4ab4-8c2c-f12bd26e562f"
    else:
        API_KEY = "3ddfb550-c326-44f2-9fd0-d875e757ccd1"

    return API_KEY


async def get_liquidity():
    API_KEY = "25PF5P4UENVP48TUXBXKU2T5ATPQ3J4VTQ"

    try:

        sms = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress"
                           "=0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c&address"
                           "=0x8fb9bbfd97fff7bba69c0162a9632c9503b29cd4"
                           "&tag=latest&apikey=" + API_KEY).json()

        sms_busd = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress"
                                "=0xe9e7cea3dedca5984780bafc599bd69add087d56&address"
                                "=0xc223A5cEecd9088C92C76504755507D18913A944"
                                "&tag=latest&apikey=" + API_KEY).json()

        sms = sms['result'][:len(str(sms['result'])) - 18]
        sms_busd = sms_busd['result'][:len(str(sms_busd['result'])) - 18]

        usdsms = float(sms) * await get_bnb_price("binancecoin")

        return sms, usdsms, sms_busd

    except ValueError as e:
        print(e)
        return "", "", ""
