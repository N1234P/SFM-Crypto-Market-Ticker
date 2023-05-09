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
from display_stats import display_nonembedded_stats

TOKEN_AUTH = ""

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

    # these channels are specific channels on the safemooon discord. modify them as your own to post on other
    # channels, or completely comment out this function for commands only.
    channel = bot.get_channel(870391088723157072)
    channel2 = bot.get_channel(875196762682437682)

    while not bot.is_closed():

        p1, trend = await get_bnb_sms_price()
        description = "$" + p1 + " " + trend

        p2, trend = await get_sms_price()
        description2 = "$" + p2 + " " + trend
        try:
            await channel.send(embed=formatter.embedder("V2 SFS Price (BNB)", description # + "| "
                                                    # + description2
        ).set_footer(text=str(datetime.now()) + " (UTC)"))

            # ---------------international channel posting

            description = "$" + p1
            description2 = "$" + p2

            await channel2.send(embed=formatter.embedder("V2 SFS Price (BNB)", description # + "| "+ description2
        ).set_footer(text=str(datetime.now()) + " (UTC)"))
        # ----------------------------------------------
            await asyncio.sleep(60)
        except:
            await asyncio.sleep(60)

        if countdown == 0:
            await display_stats.display_all_stats(channel, channel2)
            countdown = 6

        countdown -= 1
        await asyncio.sleep(5)


# comment this out. this is specifically for alerts on sfm discord and fb feed.
async def daily_report():
    await bot.wait_until_ready()

    channel = bot.get_channel(877923487015137320)
    WHEN = time(23, 0, 0)

    await asyncio.sleep(3600)
    while not bot.is_closed():

        now = datetime.utcnow()

        if now.time() >= WHEN:
            if await display_nonembedded_stats(channel):
                 await alert()
                 await asyncio.sleep(86400)

        await asyncio.sleep(60)


bot.loop.create_task(price_update())
bot.loop.create_task(wallet.whale_processing())
bot.loop.create_task(daily_report())

bot.run(TOKEN_AUTH)
