from bs4 import BeautifulSoup
import requests
import json
from discord.ext import tasks

def scrape(html_doc):
    soup = BeautifulSoup(html_doc, 'lxml')
    return soup

def something_went_wrong(site_name):
    return(f"Something went wrong on {site_name}")

# Gather Links

f = r"./webscraping/xbox.json"
with open(f) as json_file:
    sites = json.load(json_file)

def komplett():

    site = 'komplett'
    keyword = "Motta Varsel"
    site_url = sites[site]

    headers = {'Accept-Encoding': 'identity'}
    site_source = requests.get(site_url, headers=headers)
    content = scrape(site_source.content)

    try:
        content_body = content.body
        content_button = content_body.find_all("button",class_="btn-large secondary")[0]
        content_span = content_button.find_all("span")[0]
        availability = content_span.contents[0]

        if availability == keyword:
            return(False, f"No restock on {site}: {site_url}")
        else:
            site_message = f"Possible restock on {site}: {site_url}"
            return(True, site_message)

    except:
        with open("error.html", "a") as file:
            file.write(str(content))
        return(True, something_went_wrong(site))

def microsoft():

    site = 'microsoft'
    keyword = "IKKE PÅ LAGER"
    keyword2 = "Forhåndsbestill"
    site_url = sites[site]

    headers = {'Accept-Encoding': 'identity'}
    site_source = requests.get(site_url, headers=headers)
    content = scrape(site_source.content)

    try:
        content_body = content.body
        content_strong = content_body.find_all("strong")[0]
        availability = content_strong.contents[0]

        if availability == keyword or availability == keyword2:
            return(False, f"No restock on {site}: {site_url}")
        else:
            site_message = f"Possible restock on {site}: {site_url}"
            return(True, site_message)

    except:
        with open("error.html", "w", encoding='utf8') as file:
            file.write(str(content))
        return(True, something_went_wrong(site))

def microsoft_halo():
    site = 'microsoft_halo'
    keyword = "Ikke på lager"
    site_url = sites[site]

    headers = {'Accept-Encoding': 'identity'}
    site_source = requests.get(site_url, headers=headers)
    content = scrape(site_source.content)

    try:
        content_body = content.body
        content_div5 = content_body.find_all(
            "button", 
            class_ = "BundleBuilderHeader-module__checkoutButton___3UyEq w-100 bg-light-green btn btn-primary"
        )[0]
        availability = content_div5.contents[0]

        if availability == keyword:
            return(False, f"No restock on {site}: {site_url}")
        else:
            site_message = f"Possible restock on {site}: order button displayed {availability}. URL: {site_url}"
            with open("content.html", "w", encoding='utf8') as file:
                file.write(str(content))
            return(True, site_message)

    except:
        with open("error.html", "a") as file:
                file.write(str(content))
        return(True, something_went_wrong(site))

check_seconds = 600

@tasks.loop(seconds=check_seconds)
async def stock_check(client):
    await client.wait_until_ready()
    channel = client.get_channel(703969989652381718)
    jon_id = "<@365628982319906816>"

    websites = [microsoft, microsoft_halo]
    for site in websites:
        push, notification = site()
        if push:
            await channel.send(f"Alert {jon_id}")
            await channel.send(notification)

async def change_stock_check_timer(client, message):
    channel = message.channel
    if message.author.id == 365628982319906816:
        try:
            new_time = message.content.split(" ")[1]
            check_seconds = int(new_time)
            #stock_check.change_interval(check_seconds)
            msg = f'Changed timer to {check_seconds} seconds'
        except:
            msg = f"Could not process number of seconds"
        await channel.send(msg)
    else:
        scallywag = message.author.display_name
        msg = f"Nice try {scallywag}, you're not the Jon"
        await channel.send(msg)

async def start_stock_check(client, message):
    stock_check.start(client)

async def process_scrape(client, message):
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
    "start": start_stock_check,
    "change_timer": change_stock_check_timer
}