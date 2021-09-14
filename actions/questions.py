# Main handler
async def process_question(client, message):
    query_full = message.content[1:]
    channel = message.channel
    message = f'https://www.google.ca/search?q={query_full}'
    await channel.send(message)