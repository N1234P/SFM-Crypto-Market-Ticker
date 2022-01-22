import asyncio
import datetime
from datetime import datetime, time

from discord.ext.commands import bot
from helper.setup import bot

import display_stats
from helper import formatter

from commands import user_commands
from whale_wallet_data import wallet

from market.market_api import get_sms_price
from market.market_api import get_bnb_sms_price
from alerts.subscription import alert

TOKEN_AUTH = "OTM0NTQyODQ5NjcwNzgzMDQ5.Yexm2g.9ZnLgApqoVLFXS37pnQUhQ4RKEg"

whales = []


@bot.event
async def on_ready():
    print("bot is ready...")


@bot.event
async def on_message(message):
    await user_commands.cmds(message)



async def price_update():
    countdown = 0
    await bot.wait_until_ready()

    channel = bot.get_channel(870391088723157072)
    channel2 = bot.get_channel(839116448675922011)
    channel3 = bot.get_channel(875196762682437682)

    while not bot.is_closed():

        p, trend = await get_bnb_sms_price()
        description = "$" + p + " " + trend

        p, trend = await get_sms_price()
        description2 = "$" + p + " " + trend

        await channel.send("SFM/BNB " +
                           description + "| SFM/BUSD " + description2)

        await channel3.send("SFM/BNB " +
                            description + " SFM/BUSD " + description2)

        # ---------------international channel posting
        description = "$" + str(p) + " "
        if "uptrend" in trend:
            description += "<:uptrend:896236524000129064>"
        elif "downtrend" in trend:
            description += "<:downtrend:896236538642464820>"

        await channel3.send(
            embed=formatter.embedder("V2 Price (SFS/BUSD)", description).set_footer(
                text=str(datetime.now()) + " (UTC)"))
        # ----------------------------------------------
        await asyncio.sleep(60)

        if countdown == 0:
            await display_stats.display_all_stats(channel, channel2, channel3)
            countdown = 6

        countdown -= 1
        await asyncio.sleep(5)


async def daily_report():
    await bot.wait_until_ready()

    channel = bot.get_channel(877923487015137320)
    WHEN = time(23, 0, 0)

    await asyncio.sleep(3600)
    while not bot.is_closed():

        now = datetime.utcnow()

        if now.time() >= WHEN:
            if await user_commands.display_nonembedded_stats(channel):
                await alert()
                await asyncio.sleep(86400)

        await asyncio.sleep(60)


bot.loop.create_task(price_update())
bot.loop.create_task(wallet.whale_processing())
bot.loop.create_task(daily_report())

bot.run(TOKEN_AUTH)
