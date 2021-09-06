from bs4 import BeautifulSoup
import requests
import json

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
        content_div5 = content_body.find_all("button", class_ = "BundleBuilderHeader-module__checkoutButton___3UyEq w-100 bg-light-green btn btn-primary")[0]
        availability = content_div5.contents[0]

        if availability == keyword:
            return(False, f"No restock on {site}: {site_url}")
        else:
            site_message = f"Possible restock on {site}: order button displayed {availability}. URL: {site_url}"
            with open("content.html", "w") as file:
                file.write(str(content))
            return(True, site_message)

    except:
        return(True, something_went_wrong(site))