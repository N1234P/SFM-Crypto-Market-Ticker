from helper.formatter import embedder
from alerts import subscription
import random


async def custom_commands(message):
    if "$subscribe" in message.content:
        subscription.addUser(message.author.id)
        await message.channel.send("Added User")


    elif "$unsubscribe" in message.content:
        subscription.removeUser(message.author.id)
        await message.channel.send("Removed User")

    elif "$viewsubs" in message.content:

        await subscription.view_subscribers(message)

    elif "$roll" in message.content or "$d20" in message.content:

        await message.channel.send(embed=embedder("ROLL", str(random.randint(1, 20)) + " " + "🎲"))

    elif "$wen" in message.content:
        sayings, val = [], random.randint(0, 2)
        sayings.append("wen moon"), sayings.append(
            "wen lambo"), sayings.append("wen $1")

        await message.channel.send(
            embed=embedder("wen", sayings[val]))

    elif "$why" in message.content:

        myid = str(message.author.id)
        await message.channel.send(' <@%s> why wat ' % myid)

