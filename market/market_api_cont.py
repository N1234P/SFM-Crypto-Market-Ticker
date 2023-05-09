import requests
from market.market_api import get_sms_price

BITQUERY = "KEY"
BITQUERY2 = "KEY"


async def get_psfm_price():
    query = '''
    {
      ethereum(network: ethereum) {
        dexTrades(
          options: {desc: ["block.height","tradeIndex"], limit: 1}
          exchangeName: {in: ["Uniswap"]}
          baseCurrency: {is: "0x16631e53C20Fd2670027C6D53EfE2642929b285C"}
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

    query2 = '''{
      ethereum(network: ethereum) {
        dexTrades(
          options: {desc: ["block.height","tradeIndex"], limit: 1}
          exchangeName: {in: ["Uniswap"]}
          baseCurrency: {is: "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"}
          quoteCurrency: {is: "0xdAC17F958D2ee523a2206206994597C13D831ec7"}
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
    headers = {
        'X-API-KEY': BITQUERY
    }
    try:
        psfm_price = requests.post('https://graphql.bitquery.io/',
                                   json={'query': query}, headers=headers).json()["data"]['ethereum']['dexTrades'][0][
            'quotePrice']
        eth_price = requests.post('https://graphql.bitquery.io/',
                                  json={'query': query2}, headers=headers).json()["data"]['ethereum']['dexTrades'][0][
            'quotePrice']
        return "{:.10f}".format(psfm_price * eth_price)
    except ValueError:
        return ""


async def get_psfm_supply():
    ETH_KEY = "KEY"
    try:
        json = requests.get(
            "https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress"
            "=0x16631e53C20Fd2670027C6D53EfE2642929b285C&apikey=" + ETH_KEY).json()
    except ValueError:
        return ""

    return str(json['result'][:12])


async def arbitrage():
    try:
        psfm = float(await get_psfm_price()) * 1000
        sfs = await get_sms_price()

        sfm = float(sfs[0])

        if psfm != "":
            return "SFM -> PSFM: " + str((psfm / sfm - 1) * 100) + "% (+)"
    except ValueError:
        return ""
    except TypeError:
        return ""


async def migrate():
    try:
        API_KEY = "KEY"
        tokens = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress"
                              "=0x42981d0bfbAf196529376EE702F2a9Eb9092fcB5&address"
                              "=0x678ee23173dce625a90ed651e91ca5138149f590"
                              "&tag=latest&apikey=" + API_KEY).json()['result']
        ind = 11 - (20 - len(str(tokens)))
        migrate_amount = str(tokens)[:ind]
        return migrate_amount

    except ValueError:
        return ""
