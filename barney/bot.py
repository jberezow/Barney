import discord
import asyncio

from barney.actions.messages import process_message
from barney.actions.questions import process_question
from barney.data.api import moe

barney_bot = discord.Client()

event_dict = {
    '!': process_message,
    '?': process_question
}

@barney_bot.event
async def on_message(message):

    # Barney won't reply to himself
    if message.author == barney.user:
        return

    if message.content[0] == '!':
        loop = asyncio.get_event_loop()
        task = loop.create_task(process_message(message))

    if message.content[0] == '?':
        loop = asyncio.get_event_loop()
        task = loop.create_task(process_question(message))

@barney_bot.event
async def sync_users():
    for user in barney_bot.get_all_members():
        id = str(user.id)
        name = str(user.name)
        loop = asyncio.get_event_loop()
        task = loop.create_task(moe.upsertUser(id, name))

@barney_bot.event
async def on_ready():
    print("{} is now online".format(barney_bot.user.name))
    print("Client user id: {}".format(barney_bot.user.id))
    await sync_users()