from actions.messages import it_begins
import discord
import asyncio
import time
from actions import *
from discord.ext import tasks
from webscraping.scrape import komplett, microsoft, microsoft_halo

TOKEN = 'NDg1ODYxNzIzNjczNDYwNzQ4.XlBNig.9oH5OsJfyifj88ETvQgdAtxq2l4'

client = discord.Client()

@client.event
async def on_message(message):

    # Barney won't reply to himself
    if message.author == client.user:
        return

    # Classic Halo Starting Bell
    if message.content.startswith('It Begins'):
        loop = asyncio.get_event_loop()
        task = loop.create_task(it_begins(message))

@tasks.loop(seconds=30)
async def stock_check():
    await client.wait_until_ready()
    channel = client.get_channel(703969989652381718)
    jon_id = "<@365628982319906816>"

    push, notification = komplett()
    if push:
        await channel.send(f"Alert {jon_id}")
        await channel.send(notification)
    else:
        pass
        #await channel.send(f"Test alert {jon_id}")
        #await channel.send(notification)

    push, notification = microsoft()
    if push:
        await channel.send(f"Alert {jon_id}")
        await channel.send(notification)
    else:
        pass
        #await channel.send(f"Test alert {jon_id}")
        #await channel.send(notification)

    push, notification = microsoft_halo()
    if push:
        await channel.send(f"Alert {jon_id}")
        await channel.send(notification)
    else:
        pass
        #await channel.send(f"Test alert {jon_id}")
        #await channel.send(notification)

@client.event
async def on_ready():
    print("{} is now online".format(client.user.name))
    print("Client user id: {}".format(client.user.id))

stock_check.start()
client.run(TOKEN)

print("Test")