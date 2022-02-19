# Add function definitions between dashed lines
# ---------------------------------------------

async def it_begins(client, message):
    channel = message.channel
    msg = 'https://www.youtube.com/watch?v=ch8MzYclx5I'
    await channel.send(msg)

async def cushy_jobs(client, message):
    channel = message.channel
    msg = "You'll be given cushy jobs"

# ---------------------------------------------

# Main handler
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

# Dictionary of queries and response functions

response_map = {
    "it_begins": it_begins,
    "What_about_us_braindead_slobs?": cushy_jobs
}