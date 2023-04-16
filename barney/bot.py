import os
import openai
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load the API keys from the .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI API
openai.api_key = OPENAI_API_KEY

# Set up the Discord bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def get_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Pretend you are the character Barney Gumble from the Simpsons."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,
        n=1,
        temperature=0.7,
    )

    return response.choices[0].message['content']

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if the message starts with an exclamation mark
    if message.content.startswith('!'):
        prompt = message.content[1:]  # Remove the exclamation mark from the message
        response = await get_gpt_response(prompt)
        await message.channel.send(response)

# Run the bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
