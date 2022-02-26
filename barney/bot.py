import discord
import asyncio
from discord.ext import commands

from barney.actions.messages import process_message
from barney.actions.questions import process_question
from barney.data.api import moe

#barney_bot = discord.Client()
intents = discord.Intents.default()
intents.members = True
discord.MemberCacheFlags.all()
barney_bot = commands.Bot("$", intents=intents)

event_dict = {
    '!': process_message,
    '?': process_question
}

@barney_bot.event
async def on_message(message):

    # Barney won't reply to himself
    if message.author == barney_bot.user:
        return

    if message.content[0] == '!':
        loop = asyncio.get_event_loop()
        task = loop.create_task(process_message(message))

    if message.content[0] == '?':
        loop = asyncio.get_event_loop()
        task = loop.create_task(process_question(message))

async def sync_users():
    for user in barney_bot.get_all_members():
        id = str(user.id)
        name = str(user.name)
        await moe.upsertUser(id,name)
        print(f"User {name} updated in database")

async def sync_channels():
    for channel in barney_bot.get_all_channels():
        id = str(channel.id)
        name = str(channel.name)
        await moe.upsertChannel(id,name)

@barney_bot.event
async def on_ready():
    print("{} is now online".format(barney_bot.user.name))
    print("Client user id: {}".format(barney_bot.user.id))
    loop = asyncio.get_event_loop()
    task = loop.create_task(sync_users())
    #task2 = loop.create_task(sync_channels())
    