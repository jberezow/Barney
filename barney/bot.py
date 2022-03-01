import discord
import asyncio
import time
from discord.ext import commands

from barney.actions.messages import process_message
from barney.actions.questions import process_question
from barney.data.api import moe

USERS = {}

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
    
    if message.content[0] == '$':
        loop = asyncio.get_event_loop()
        task = loop.create_task(payment(message))

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
        if channel.category == None:
            continue
        id = str(channel.id)
        name = str(channel.name)
        category_id = str(channel.category.id)
        await moe.upsertChannel(id,name,category_id)
        print(f"Channel {name} updated in database")
        time.sleep(5)

async def sync_categories():
    categories = {}
    for channel in barney_bot.get_all_channels():
        category = channel.category
        if category == None:
            continue
        id = str(category.id)
        name = str(category.name)
        if id not in categories.keys():
            categories[id] = name
    
    for category in categories:
        await moe.upsertCategory(category,categories[category])
        print(f"Category {categories[category]} updated in database")

async def load_users():
    response = await moe.allUsers()
    users = response.data['lads']
    for user in users:
        USERS[user['name']] = {'id': user['id'], 'wallet': user['wallet']}
    print("Users received")

async def payment(message):
    try:
        intended_payee = message.content.split(" ")[1].strip()
        intended_amount = float(message.content.split(" ")[0].strip().replace("$",""))
        intended_payer = message.author.name
        intended_payer_wallet = USERS[intended_payer]['wallet']
        intended_payer_id = USERS[intended_payer]['id']
        intended_payee_wallet = USERS[intended_payee]['wallet']
        intended_payee_id = USERS[intended_payee]['id']
        if intended_amount < 0 or intended_payer_wallet < intended_amount:
            await message.channel.send("Please do not try to scam the bank")
        else:
            print(f"{intended_payer} sends ${intended_amount} to {intended_payee}")
            payer_wallet = intended_payer_wallet - intended_amount
            payee_wallet = intended_payee_wallet + intended_amount
            await moe.makePayment(intended_payer_id, payer_wallet)
            await moe.makePayment(intended_payee_id, payee_wallet)
            USERS[intended_payee]['wallet'] += intended_amount
            USERS[intended_payer]['wallet'] -= intended_amount
            balances = " ".join([f"{i}: {USERS[i]['wallet']}" for i in USERS.keys()])
            updated_wallets = "New balances: " + balances
            await message.channel.send(updated_wallets)
    except:
        await message.channel.send("I could not parse that transaction.")

@barney_bot.event
async def on_ready():
    print("{} is now online".format(barney_bot.user.name))
    print("Client user id: {}".format(barney_bot.user.id))
    loop = asyncio.get_event_loop()
    #user_task = loop.create_task(sync_users())
    #channel_task = loop.create_task(sync_channels())
    #category_task = loop.create_task(sync_categories())
    loop.create_task(load_users())