async def it_begins(message):
    channel = message.channel
    msg = 'https://www.youtube.com/watch?v=ch8MzYclx5I'
    await channel.send(msg)