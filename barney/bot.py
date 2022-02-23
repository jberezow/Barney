import discord
import asyncio

from barney.actions.messages import process_message
from barney.actions.questions import process_question

barney = discord.Client()

event_dict = {
    '!': process_message,
    '?': process_question
}

@barney.event
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

@barney.event
async def on_ready():
    print("{} is now online".format(barney.user.name))
    print("Client user id: {}".format(barney.user.id))