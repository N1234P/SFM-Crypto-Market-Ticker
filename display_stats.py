from market import market_api
from helper.formatter import price_formatter
from whale_wallet_data import wallet
from market.market_api import get_sms_price
import discord
from datetime import datetime
from market.market_api import get_bnb_sms_price


async def display_all_stats(ctx, ctx2):
    sfm_swap = await get_sms_price()
    sfm_swap_bnb = await get_bnb_sms_price()

    dex_vol = await market_api.get_dex_total_vol(False)
    supply, bw = await market_api.get_supply()
    supply, bw = price_formatter(supply), price_formatter(bw)
    market_cap = price_formatter(await market_api.get_mc())

    transfer = price_formatter(await wallet.liquidity_wallet_transfer())
    sms, usd_sms, sms_busd = await market_api.get_liquidity()
    percent = (await market_api.get_safemoon_percent())

    reflections, reflections_USD = await market_api.get_generic_reflection()
    burn = price_formatter(await market_api.get_burn())

    data = [sfm_swap, sfm_swap_bnb, dex_vol, supply, bw, market_cap, transfer, sms, usd_sms, percent, reflections,
            reflections_USD
        , burn]
    if any(data[i] is None or data[i] == "" for i in range(len(data))):
        return

    supply += " tokens"
    burn += " tokens"
    bw += " tokens"
    market_cap = "$" + market_cap
    transfer += " BNB"

    em = discord.Embed(title="🔥 All Stats - V2 🔥", colour=discord.Colour.blue())

    em.add_field(name="<:sfm:824031099402321961> SFM V2 Price (SFS BNB)",
                 value="$" + sfm_swap_bnb[0]) # + " | $" + sfm_swap[0])
    em.add_field(name="🔥 24 Hour Burn", value=burn)
    em.add_field(name="💥 Total DEX Volume", value=dex_vol)
    em.add_field(name="🏛️ MarketCap", value=market_cap)
    em.add_field(name="Circulating Supply & Burn Wallet", value="Supply: " + supply + "\nBurn Wallet: " + bw)
    em.add_field(name="💰 Reflections (Per Million Tokens - Estimate)",
                 value=price_formatter(reflections) + " tokens ($" +
                       price_formatter(reflections_USD) + ")")
    em.add_field(name="Liquidity", value="SFS: " + price_formatter(sms) + " BNB ($" + price_formatter(
        usd_sms) + ")")
    em.add_field(name="<:uptrend:838343716276142080> 24HR Percentage Change", value=percent)
    em.add_field(name="<:pandaBags:840623325909745674> Remaining BNB For Swap & Evolve",
                 value=transfer)
    em.add_field(name="Other Coins",
                 value="$" + price_formatter(
                     await market_api.get_bitcoin_price("bitcoin")) + " (Bitcoin)\n" + "$" + price_formatter(
                     await market_api.get_bnb_price("wbnb")) + " (BNB)")

    em.set_footer(
        text="There are a lot more features, use $help command to find out. \n" + str(datetime.now()) + " UTC")

    await ctx.send(embed=em)
    await ctx2.send(embed=em)


# misc ------------------------------------------------------------

# Used to link to Facebook feed

async def display_nonembedded_stats(ctx):
    sfm_swap = await get_sms_price()
    sfm_swap_bnb = await get_bnb_sms_price()

    if sfm_swap[0] == "" or sfm_swap_bnb[0] == "":
        return False

    dex_vol = await market_api.get_dex_total_vol(False)
    supply, bw = await market_api.get_supply()
    supply, bw = price_formatter(supply) + " tokens", price_formatter(bw) + " tokens"

    market_cap = "$" + price_formatter(await market_api.get_mc())
    transfer = price_formatter(await wallet.liquidity_wallet_transfer()) + " BNB"
    percent = (await market_api.get_safemoon_percent())

    if transfer == "":
        return False

    if dex_vol == "":
        return False
    else:
        reflections, reflections_USD = await market_api.get_generic_reflection()
        dex_token_vol = await market_api.get_dex_total_vol(True)
        if dex_token_vol == "":
            return False
        burn = price_formatter(.02 * dex_token_vol) + " tokens"

    await ctx.send(
        "🌙 SFM Price V2 SFS (BNB) | " + "$" + sfm_swap_bnb[0] # + "|" + sfm_swap[
            #0]
        + "\n\n🔥 24 Hour Burn | " + burn
        + "\n\n Total DEX Volume | " + dex_vol + "\n\n🏛️ MarketCap | " + market_cap + "\n\n🌀 Circulating Supply | " + supply
        + "\n\n💰 Reflections (Per Million Tokens) | " + price_formatter(reflections) + " tokens"
        + "\n\n📈 24HR Percentage Change | " + percent
        + "\n\n😁 Remaining BNB For Swap & Evolve | " + transfer
        + "\n\n🪙 $" + price_formatter(
            await market_api.get_bitcoin_price("bitcoin")) + " (Bitcoin)" + "\n\n🪙 $" + price_formatter(
            await market_api.get_bnb_price("wbnb")) + " (BNB)")
    return True


async def help(ctx):
    em = discord.Embed(title="Help", description="A full summary of usable commands", colour=discord.Colour.blue())

    em.add_field(name="$p or $v2", value="PancakeSwap's v2 price or SafeMoonSwap price")
    em.add_field(name="$btc, $eth, $bnb, $ada, $doge, $xrp, $xlm, $one", value="View different coin prices")
    em.add_field(name="$mc/$marketcap, $vol/$volume/$dexvol, $burn, $supply, $lq/liquidity, $equiv/$ratio",
                 value="View SafeMoon's statistics")
    em.add_field(name="$bitmart/$bm, $lb/$lbank, $gate", value="Exchange's price")
    em.add_field(name="$wallet <wallet address>",
                 value="Dm this bot in this format and you'll get the wallet's total tokens, USD equivalent, and "
                       "24 hour reflections")
    em.add_field(name="$evolve", value="Used to get the remaining  BNB left for a swap and evolve!")
    em.add_field(name="$dom, $whale",
                 value="Tracks the current top whale's wallet and whale dominance")
    em.add_field(name="$reflection", value="Gives you a 24hr reflection estimate for every 1B tokens you hold")

    em.add_field(name="$psfm, $psupply, $ppos <position number>, $pwallpos <wallet_address>", value="psfm statistics")
    em.add_field(name="$pos <number>", value="sfm holder ranking")
    em.add_field(name="$arb", value="View price differences in sfm and psfm")

    em.add_field(name="$countdown", value="Occasionally applicable, used to countdown for events")

    em.add_field(name="$subscribe, $unsubscribe, $viewsubs", value="sign up for sfm price alerts and view who is "
                                                                   "subscribed (Currently Offline)")
    em.add_field(name="Custom Commands", value="currently not adding more")

    em.set_footer(text='Help Manual')
    await ctx.send(embed=em, delete_after=30)
