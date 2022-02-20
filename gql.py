import requests
import json

# Get GQL Endpoint
with open("gql_endpoint.txt",'r') as f:
    gql_endpoint = f.read()

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

r = requests.post(gql_endpoint, json={"query": query}, headers=headers)
print("Debug")