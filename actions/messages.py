from webscraping.scrape import stock_check

async def change_stock_check_timer(client, message):
    channel = message.channel
    if message.author.id == 365628982319906816:
        try:
            new_time = message.content.split(" ")[1]
            check_seconds = int(new_time)
        except:
            msg = f"Could not process number of seconds"
            await channel.send(msg)
        #stock_check.change_interval(check_seconds)
        msg = f'Changed timer to {check_seconds} seconds'
        await channel.send(msg)
    else:
        scallywag = message.author.display_name
        msg = f"Nice try {scallywag}, you're not the Jon"
        await channel.send(msg)

async def it_begins(client, message):
    channel = message.channel
    msg = 'https://www.youtube.com/watch?v=ch8MzYclx5I'
    await channel.send(msg)

async def process_message(client, message):
    query_full = message.content[1:]
    query_keyword = query_full.split(" ")[0]
    try:
        response_function = response_map[query_keyword]
    except:
        error_warning = f"No prompt found for your query"
        await message.channel.send(error_warning)
        return
    
    await response_function(client, message)

response_map = {
    "change_timer": change_stock_check_timer,
    "it_begins": it_begins
}