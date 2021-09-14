import discord
import asyncio
from webscraping.scrape import process_scrape, start_stock_check
from actions.messages import process_message
from actions.questions import process_question

with open('token.txt', 'r') as file:
    TOKEN = file.read()

client = discord.Client()

event_dict = {
    '!': process_message,
    '#': process_scrape,
    '?': process_question
}

@client.event
async def on_message(message):

    # Barney won't reply to himself
    if message.author == client.user:
        return

    if message.content[0] == '!':
        loop = asyncio.get_event_loop()
        task = loop.create_task(process_message(client, message))

    if message.content[0] == '#':
        loop = asyncio.get_event_loop()
        task = loop.create_task(process_scrape(client, message))

    if message.content[0] == '?':
        loop = asyncio.get_event_loop()
        task = loop.create_task(process_question(client,message))

@client.event
async def on_ready():
    print("{} is now online".format(client.user.name))
    print("Client user id: {}".format(client.user.id))

start_stock_check(client, None)
client.run(TOKEN)