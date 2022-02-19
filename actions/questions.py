# Main handler
async def process_question(client, message):
    query_full = message.content[1:]
    processed_query = query_full.replace(' ','+')
    channel = message.channel
    message = f'https://www.google.ca/search?q={processed_query}'
    await channel.send(message)