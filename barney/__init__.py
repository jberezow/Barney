import os
parent_folder = os.curdir
print(parent_folder)

# Get GQL Endpoint
with open("keys/gql_endpoint.txt",'r') as f:
    GQL_ENDPOINT = f.read()

# Get Admin Secret
with open("keys/hasura_secret.txt",'r') as f:
    HASURA_SECRET = f.read()

# Get Discord Token
with open('keys/token.txt', 'r') as file:
    TOKEN = file.read()