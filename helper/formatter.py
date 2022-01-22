import discord


def price_formatter(price):
    if price != "":
        price = str(round(float(price), 2))
        price = "{:,}".format(float(price))
        return price
    else:
        return ""


def embedder(title, description):

    em = discord.Embed(title=title, description=description, colour=discord.Colour.blue())
    return em