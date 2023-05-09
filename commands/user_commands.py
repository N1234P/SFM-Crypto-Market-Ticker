import discord
from helper.setup import bot

from market.market_api import get_sms_price
from market.market_api import get_bnb_sms_price

from whale_wallet_data import wallet
from commands.other_commands import custom_commands

from market import market_api, market_api_cont

from helper.formatter import price_formatter
from helper.formatter import embedder

from display_stats import help


async def cmds(message):
    if "$" not in message.content:
        # await appearance(message)
        return

    channels = ["📈│price-watch"]  # add your own channel here to enable commands at any given channel
    arr = ["$percent", "$psupply", "$psfm", "$ppos", "$pos", "$pwallpos"]
    if str(message.channel) in channels:
        if "$wallet" in message.content:
            await message.channel.send("Dm me! This command is not allowed here.")
            return

    if str(message.channel) in channels or (
            isinstance(message.channel, discord.channel.DMChannel) and message.author != bot.user):

        if "$p" in message.content and all(words not in message.content for words in arr) or "$v2" in message.content:
            sms, sms2 = await get_bnb_sms_price(), await get_sms_price()

            description = "$" + str(sms[0]) + " " + sms[1] #+ "| $" + str(sms2[0]) + " " + sms2[1]

            await message.channel.send(
                embed=embedder("V2 cmd (BNB)", description))

        if "$pcs" in message.content:
            pcs = await market_api.get_pcs_price()

            description = "$" + str(pcs[0]) + " " + pcs[1]

            await message.channel.send(embed=embedder("V2 (PCS)", description).set_footer(text="DISCLAIMER: Pancake"
                                                                                               "LQ is low & not "
                                                                                               "supported by "
                                                                                               "SafeMoon"))
        elif "$btc" in message.content or "$bitcoin" in message.content or "$ohshit" in message.content:

            description = "$" + price_formatter(await market_api.other_coins("Bitcoin"))
            await message.channel.send(
                embed=embedder("BTC", description))

        elif "$ada" in message.content or "$cardano" in message.content:

            description = "$" + price_formatter(await market_api.other_coins("Cardano"))
            await message.channel.send(
                embed=embedder("ADA", description))

        elif "$bnb" in message.content:

            description = "$" + price_formatter(await market_api.get_bnb_price("wbnb"))
            await message.channel.send(
                embed=embedder("BNB", description))

        elif "$eth" in message.content or "$ethereum" in message.content or "$ether" in message.content:

            description = "$" + price_formatter(await market_api.other_coins("Ethereum"))
            await message.channel.send(
                embed=embedder("ETH", description))

        elif "$doge" in message.content:

            description = "$" + price_formatter(await market_api.other_coins("Dogecoin"))
            await message.channel.send(
                embed=embedder("DOGE", description))

        elif "$xrp" in message.content:

            description = "$" + price_formatter(await market_api.other_coins("XRP"))
            await message.channel.send(
                embed=embedder("XRP", description))

        elif "$xlm" in message.content:

            description = "$" + price_formatter(await market_api.other_coins("Stellar"))
            await message.channel.send(
                embed=embedder("XLM", description))

        elif "$one" in message.content or "$harmony" in message.content:

            description = "$" + price_formatter(await market_api.other_coins("Harmony"))
            await message.channel.send(
                embed=embedder("Harmony One", description))


        elif "$supply" in message.content:

            supply, bw = await market_api.get_supply()
            supply, bw = price_formatter(supply), price_formatter(bw)
            supply += " tokens"
            bw += " tokens"

            await message.channel.send(
                embed=embedder("Circulating Supply & Burn Wallet Size", "Supply: " + supply + "\nBurn Wallet: " + bw))

        elif "$burn" in message.content:
            description = price_formatter(await market_api.get_burn())
            if description == "":
                await message.channel.send("Burn/DEXVol/Reflections Command was used to soon, wait a little")
            else:
                description += " tokens"
                await message.channel.send(
                    embed=embedder("24 Hour Total Burn: ", description))

        elif "$mc" in message.content or "$marketcap" in message.content:

            description = "$" + price_formatter(await market_api.get_mc())
            await message.channel.send(
                embed=embedder("MarketCap", description))

        elif '$ratio' in message.content or "$equiv" in message.content:
            description = str(await market_api.get_sfm_to_bnb_equivalence())
            await message.channel.send(
                embed=embedder("SFM to BNB", "1 SFM = " + description + " BNB")
            )

        elif "$bm" in message.content or "$bitmart" in message.content:
            description = "$" + await market_api.exchanges("BitMart")

            await message.channel.send(
                embed=embedder("BitMart", description))

        elif "$gate" in message.content:
            description = "$" + await market_api.exchanges("Gate")

            await message.channel.send(
                embed=embedder("Gate.io", description)
            )

        elif "$lbank" in message.content or "lb" in message.content:
            description = "$" + await market_api.exchanges("LBank")

            await message.channel.send(
                embed=embedder("LBank", description)
            )


        elif "$evolve" in message.content or "$injection" in message.content:
            remaining = price_formatter(await wallet.liquidity_wallet_transfer())
            await message.channel.send(
                embed=embedder("Remaining BNB For Swap & Evolve", remaining + " BNB")
            )

        elif "$dexvol" in message.content or "$vol" in message.content:
            description = await market_api.get_dex_total_vol(False)
            if description == "":
                await message.channel.send("Burn/PcsVol/Reflections Command was used to soon, wait a little")
            else:
                await message.channel.send(
                    embed=embedder("Total DEX 24HR Volume", description)
                )

        elif "$wallet" in message.content:
            await wallet.import_wallet_args(message)

        elif "$reflection" in message.content:

            tokens, dollar_equivalent = await market_api.get_generic_reflection()
            if tokens == "":
                await message.channel.send("Burn/DEXVol/Reflections Command was used to soon, wait a little")
            else:
                tokens = price_formatter(tokens)
                dollar_equivalent = price_formatter(dollar_equivalent)
                em = embedder("Daily Reflection",
                              "Every 1M tokens: " + tokens + " (" + "$" + dollar_equivalent + ")")
                em.set_footer(text="For more information, dm me with $wallet <address>")
                await message.channel.send(
                    embed=em
                )

        elif "$arb" in message.content:
            description = await market_api_cont.arbitrage()
            if description == "":
                await message.channel.send("psfm returned empty string, try again later")
                return

            await message.channel.send(embed=embedder("ARBITRAGE", description))

        elif "$psupply" in message.content:
            description = price_formatter(await market_api_cont.get_psfm_supply()) + " tokens"
            await message.channel.send(embed=embedder("pSFM Supply", description))

        elif "$psfm" in message.content:
            description = str(await market_api_cont.get_psfm_price())
            if description == None:
                await message.channel.send("empty string returned, try again later")
                return

            await message.channel.send(embed=embedder("pSFM Price", "$" + description))

        elif "$ppos" in message.content:
            await wallet.get_psfm_holder_position(message)

        elif "$pwallpos" in message.content:
            await wallet.get_psfm_wallet_position(message)

        elif "$liquidity" in message.content or "$lq" in message.content:

            sms, usd_sms, sms_busd = await market_api.get_liquidity()
            if sms == "":
                await message.channel.send(
                    "BSC API may be down, so everything that uses BSC data will likely also be down")
                return

            sms = price_formatter(sms)
            usd_sms = price_formatter(usd_sms)
            sms_busd = price_formatter(sms_busd)
            description = "SafeMoon " \
                          "Swap: " + sms \
                          + " BNB ($" + usd_sms + ") \n" + "BUSD: " + sms_busd
            await message.channel.send(embed=embedder("Liquidity", description))

        elif "$dom" in message.content or "$whale" in message.content:

            try:
                data = await wallet.get_whale_dominance()

                if data == "currently processing whale data, give it a minute or two":
                    await message.channel.send(data)
                    return

                list_whales, text_whales = data[2], []

                for i in range(len(list_whales)):
                    text_whales.append(
                        "Whale " + str(len(list_whales) - i) + ": " + price_formatter(str(list_whales[i])) + " tokens")

                text_whales = "\n".join(reversed(text_whales))

                dominance_ten = str(data[0]) + " %"
                dominance_twenty = str(data[1]) + " %"

                await message.channel.send(
                    embed=embedder("Whale Dominance", text_whales + "\n\n" + "Top 10 Whales own __"
                                   + dominance_ten + "__ of the circulating supply.\n" + "Top 25 Whales own __" + dominance_twenty
                                   + "__ of the circulating supply.").set_footer(
                        text="Updates Every 30 minutes (MIGRATED V2 WHALES ONLY)"))
            except Exception as e:
                print(e)
                await message.channel.send("Processing data, give it a min or two")


        elif "$migrate" in message.content:
            migrate_amount = price_formatter(await market_api_cont.migrate())
            if migrate_amount != "":
                await message.channel.send(embed=embedder("Tokens Left For Migration", str(migrate_amount)))


        elif "$help" in message.content:
            await help(message.channel)

        await custom_commands(message)
