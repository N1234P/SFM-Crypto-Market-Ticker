import asyncio

import discord
import requests
from market import market_api
from helper import formatter
from helper.setup import bot

whales = []


async def import_wallet_args(message):
    if isinstance(message.channel, discord.channel.DMChannel):
        if "$wallet" in message.content:
            args = message.content.split()
            if len(args) < 2:
                await message.channel.send("INVALID FORMAT - $wallet <wallet_address>")
            else:
                bal = await wallet_tracker(args[1])
                try:
                    price = await market_api.get_sms_price()
                    price = price[0]
                    supply = await market_api.get_supply()
                    converted = bal * float(price)
                    reflections = ((await market_api.get_dex_total_vol(True) * bal) / (25 * supply[0]))

                    bal = formatter.price_formatter(bal)
                    converted = formatter.price_formatter(converted)
                    reflections = formatter.price_formatter(reflections)
                    await message.channel.send('```Wallet Safemoon Amount: ' + bal + ' tokens\n'
                                               + 'USD Equivalent: $' + converted + "\n" +
                                               "24 Hour Reflections: " + reflections + " tokens```")
                except TypeError:
                    await message.channel.send("Invalid Address")

                except ValueError:
                    pass


async def wallet_tracker(address):
    API_KEY = "key"

    try:
        json = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress"
                            "=0x42981d0bfbaf196529376ee702f2a9eb9092fcb5&address=" + address +
                            "&tag=latest&apikey=" + API_KEY).json()
    except ValueError:
        return ""

    ind = 11 - (20 - len(str(json.get('result'))))

    return int(str(json.get('result'))[:ind])


async def liquidity_wallet_transfer():
    API_KEY = "key"
    try:
        json = requests.get("https://api.bscscan.com/api?module=account&action=balance"
                            "&address=0x42981d0bfbAf196529376EE702F2a9Eb9092fcB5"
                            "&tag=latest&apikey=" + API_KEY).json()

        return 132.32 - int(json['result']) / 10 ** 18
    except ValueError:
        return ""


async def get_whale_dominance():
    if len(whales) != 25:
        return "currently processing whale data, give it a minute or two"
    supply, _ = await market_api.get_supply()

    dominance_tf = (sum(whales) / supply) * 100

    dominance_10 = (sum(whales[len(whales) - 10:]) / supply) * 100

    data = [dominance_10, dominance_tf, whales]

    return data


async def whale_processing():
    await bot.wait_until_ready()

    while not bot.is_closed():

        global whales
        whales = []

        file = open("whale_wallet_data/whales.txt", "r")
        API_KEY, addresses = "key", file.read().splitlines()
        try:
            for addr in addresses:
                json = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress"
                                    "=0x42981d0bfbAf196529376EE702F2a9Eb9092fcB5&address=" + addr +
                                    "&tag=latest&apikey=" + API_KEY).json()
                ind = 11 - (20 - len(str(json.get('result'))))
                if ind < len(str(json.get('result'))) and ind > 0:
                    whales.append(float(json.get('result')[:ind]))
                    await asyncio.sleep(.25)

            whales = sorted(list(map(float, whales)))[len(whales) - 25:]

            await asyncio.sleep(1800)

        except Exception:

            await asyncio.sleep(5)
            pass


async def get_psfm_wallet_position(message):
    msg_arr = message.content.split()
    if len(msg_arr) < 2:
        await message.channel.send("**Please Enter Wallet Address**")
        return

    params = {
        "key": "key",
        "token": "0x16631e53C20Fd2670027C6D53EfE2642929b285C",
        "limit": "100000"
    }
    holders = requests.get("https://api.bloxy.info/token/token_holders_list", params=params).json()

    try:
        ind = 1
        for x in holders:
            if str(msg_arr[1]).lower() in str(x['address']):
                await message.channel.send(embed=formatter.embedder("Wallet Position", ind))
                return
            ind += 1
    except:
        await message.channel.send("**Invalid Wallet Address**")


async def get_psfm_holder_position(message):
    msg_arr = message.content.split()
    if len(msg_arr) < 2:
        await message.channel.send("**Please Enter a Position**")
        return

    params = {
        "key": "key",
        "token": "0x16631e53C20Fd2670027C6D53EfE2642929b285C",
        "limit": "100000"
    }

    holders = requests.get("https://api.bloxy.info/token/token_holders_list", params=params).json()

    try:
        if int(msg_arr[1]) > len(holders) or int(msg_arr[1]) < 1:
            await message.channel.send("**Position Argument Outside of Bounds!**")
            return
    except:
        await message.channel.send("**Invalid Position**")
        return

    description = "Balance: " + str(
        formatter.price_formatter(holders[int(msg_arr[1]) - 1]['balance'])) + " tokens" + "\n" + \
                  holders[int(msg_arr[1]) - 1]['address']

    await message.channel.send(embed=formatter.embedder("pSFM Wallet Position " + str(msg_arr[1]), description))
