from helper.setup import bot

from helper.formatter import embedder
from market.market_api import get_safemoon_percent

from market.market_api import get_sms_price


def addUser(id):
    file = open("alerts/subscribers.txt", "r")
    if str(id) in file.read():
        file.close()
        return "you already exist on here"

    file.close()

    file = open("alerts/subscribers.txt", "a")

    file.write("\n" + str(id) + "\n")

    file.close()
    return "added user"


def removeUser(id):
    file = open("alerts/subscribers.txt", "r")
    lines = file.readlines()
    file.close()
    ret = "you weren't found on here"
    with open("alerts/subscribers.txt", "w") as updated_file:
        for line in lines:
            if line.strip("\n") != str(id):
                updated_file.write(line)
            else:
                ret = "REMOVED USER"
    updated_file.close()
    return ret


def change_to_arr():
    file = open("alerts/subscribers.txt", "r")
    return file.read().splitlines()


async def view_subscribers(message):
    subscribers = "Subscription List (IDs)  -- \n" + "\n".join(change_to_arr())

    await message.channel.send(subscribers)


async def alert():
    sfm_percent = float((await get_safemoon_percent()).replace("%", ""))
    channel = bot.get_channel(870391088723157072)

    if sfm_percent > 10:
        price = await get_sms_price()
        price = price[0]
        await channel.send(embed=embedder("ALERT!!!",
                                          "SafeMoon is up by " + str(sfm_percent) + "% " + "at a price of $" + str(
                                              price)))

        subscribers, users = change_to_arr(), ""
        for id in subscribers:
            users += "<@" + id + "> \n"

        await channel.send(users)


    elif sfm_percent < -10:
        price = await get_sms_price()
        price = price[0]

        await channel.send(embed=embedder("ALERT!!!",
                                          "SafeMoon is Down by " + str(sfm_percent) + "% " + "at a price of $" + str(
                                              price)))

        subscribers, users = change_to_arr(), ""
        for id in subscribers:
            users += "<@" + id + "> \n"

        await channel.send(users)
