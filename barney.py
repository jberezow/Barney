from actions.messages import it_begins
import discord
import asyncio
from actions import *

TOKEN = 'NDg1ODYxNzIzNjczNDYwNzQ4.XlBNig.9oH5OsJfyifj88ETvQgdAtxq2l4'

client = discord.Client()

@client.event
async def on_message(message):

    #Barney won't reply to himself
    if message.author == client.user:
        return

    #Classic Halo Starting Bell
    if message.content.startswith('It Begins'):
        loop = asyncio.get_event_loop()
        task = loop.create_task(it_begins(message))


@client.event
async def on_ready():
    print("{} is now online".format(client.user.name))
    print("Client user id: {}".format(client.user.id))

client.run(TOKEN)

print("Test")