import requests
import json

endpoint = 'https://ajimbo-data.hasura.app/v1/graphql'

# Get admin secret
with open("hasura_secret.txt",'r') as f:
    hasura_secret = f.read()

headers = {'x-hasura-admin-secret': hasura_secret}

query = '''
    query AllChannels {
        channels {
            name
        }
    }
'''

r = requests.post(endpoint, json={"query": query}, headers=headers)
print("Debug")